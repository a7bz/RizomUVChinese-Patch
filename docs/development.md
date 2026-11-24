# 开发文档

面向维护者：说明补丁的运行机制、如何刷新字符串清单、如何改词典、如何验证改动。

## 一、整体架构

```
用户双击快捷方式
      │
      ▼
RizomUVChineseLauncher.exe
      │  1. 解析同目录的 rizomuv.exe 与 RizomUVChineseRuntime.dll
      │  2. CreateProcessW(..., CREATE_SUSPENDED)
      │  3. 在宿主里远程 LoadLibraryW 注入运行时
      │  4. ResumeThread
      ▼
rizomuv.exe（已注入）
      │
      ├─ RizomUVChineseRuntime.dll
      │     ├─ 读 dictionary_zh.json（UTF-8 JSON → UTF-16 哈希表）
      │     ├─ 改写宿主模块的 IAT，接管 GDI 文字入口
      │     └─ 周期性扫描 HMENU，替换菜单项文字
      │
      └─ 正常启动，界面文字在绘制/测量时被换成中文
```

关键约束：**绘制与测量必须命中同一份译文**。GDI 的排版逻辑是「先测量宽度、再按宽度绘制」，两侧译文不一致会让控件按英文宽度排版却画中文，出现溢出或截断。因此六个入口共用同一个 `translate()`。

## 二、为什么用 IAT 钩子而不是改文件

早期方案是等长字节替换（和 `MarmosetToolbag5-Chinese` 类似），但在这个程序上不可行：

| 问题 | 说明 |
| --- | --- |
| 槽位长度限制 | 英文槽位按编译期长度分配，`Cut` 只够放一个汉字。要放长译文就得改长度常量，而调用点分散、部分无法静态确认 |
| 代码页依赖 | 塞进槽位的 GBK 字节要靠系统 ACP=936 才能正确解释。英文 Windows（437/1252）直接乱码，启用 UTF-8 测试版也一样 |
| 修改原程序 | 改 `rizomuv.exe` 意味着要处理备份、校验、版本匹配，且用户会怀疑完整性 |

IAT 钩子把这三个问题一起解决了：译文以 UTF-16 交给 GDI（无长度上限、与代码页无关），原程序文件一个字节都不动。

## 三、IAT 改写细节

### 只处理宿主同目录的模块

`gdi_hook.cpp` 的 `host_dir_matches()` 会比对模块路径与主程序路径的目录部分。只改写 `rizomuv.exe` 与它自带的 DLL，**绝不动系统 DLL**——系统 DLL 里的导入属于系统实现，改写它们会影响进程里其它组件（包括我们自己的日志、文件读写）。

### 为什么需要反复安装

宿主在启动阶段陆续加载模块，每次新加载的模块都带着自己的 IAT。因此 `install()` 会在启动后循环调用（约 60 秒窗口），每次扫描全部已加载模块，已改写的槽位会被跳过（比较当前值是否已经是钩子地址）。

### 槽位还原表

每次改写都记录 `(槽位地址, 原函数地址)` 到 `g_patched[]`。`uninstall()` 按表写回。正常退出时不需要显式调用——进程结束，内存自然消失——但保留这个能力便于调试。

### `dx` / `dxs` 数组必须丢弃

`ExtTextOutW` 的 `dx` 参数是「每个字符的间距数组」，`GetTextExtentExPointW` 的 `dxs` 同理。译文长度与原文不同时，这些数组长度对不上，继续传给 GDI 会读越界。所以只要发生替换，就传 `nullptr`，让 GDI 用字体默认间距。

### 字形索引模式必须跳过

`ExtTextOutW` 带 `ETO_GLYPH_INDEX` 标志时，`lpString` 里装的是字形号而不是文字。替换它会把界面画成乱码方块。代码里显式排除。

## 四、词典

### 格式

```json
{
  "version": 1,
  "translations": {
    "Files": "文件",
    "Unwrap": "展开"
  }
}
```

UTF-8（可带 BOM）。运行时用手写的 JSON 解析器读取（不依赖第三方库），转成 UTF-16 的 `unordered_map`。

### 匹配规则

整串精确匹配，区分大小写，保留空格与标点。**不做子串替换**——否则 `Enable` 会污染 `Enable Grid Snap`。

命中失败后有两级回退（见 `gdi_hook.cpp` 的 `translate()`）：

1. **去首尾空白再查**：宿主常写 `" Padding "` 这类带空格做对齐的文本。命中后把原空白补回去。
2. **长段落按比例切片**：宿主把帮助文本按行拆开逐行绘制，单行匹配不到整段词条。`dict::lookup_fragment()` 在长词条里找到包含该行的那条，按字符比例把原文区间映射到译文区间。

### 生成流程

```
tools/gen_dictionary.py    结构化词表（按界面区域分组）+ 生成逻辑
tools/dict_extra.py        长句、按钮提示（体积最大的部分）
        │
        ▼
translations/dictionary_zh.json
        │
        ▼
tools/check_dictionary.py  校验编码、格式、空值、异常字符
```

改完词表后必须重新生成，不要手改 JSON。

`gen_dictionary.py` 里的处理包括：

- 剥掉菜单助记符 `&`（`&Files` → `Files`）；
- 按 `\t` 拆出快捷键后缀单独保留；
- 对 `&` 与空白做归一化，保证与运行时收到的字符串一致。

### 校验脚本做什么

`check_dictionary.py`：

- 检查 BOM、`version == 1`、`translations` 是对象；
- 拒绝空译文、`\ufffd`（编码损坏）、内嵌 `\t` `\r` `\n`（会破坏 GDI 单行绘制）；
- 把「译文与原文相同」「首尾有空白」作为提示而非错误列出。

`check_coverage.py` 除了统计覆盖率，还会做一次**跳过清单审计**：

`KEEP_AS_IS` 里的条目是刻意保留的（品牌名、单位符号、坐标轴缩写、快捷键动作标识）。
但这份清单曾经把 `enable` 也放进去了，导致变换面板关闭状态绘制的小写 `enable`
被算作「已覆盖」，覆盖率虚高。现在脚本会用 `SUSPECT_WORDS` 反向检查：
只要是普通英文单词、又出现在采集清单里、且词典里没有对应译文，就报错退出。

```bash
python tools/check_coverage.py
# ...
# -- 被跳过清单掩盖、需要补译（1 条）--
#   'enable'
```

规则是：**大写的是动作标识可以保留，小写的是界面文字必须翻译**。
`Enable` 与 `enable` 在词典里是两条独立条目，运行时的匹配区分大小写。

## 五、覆盖率检查

`check_coverage.py` 需要一份「宿主实际用过的全部字符串」清单。

### 采集

```bash
# 1. 编译（会同时产出采集器）
cmd /c source\build.bat

# 2. 用采集器启动：界面保持英文，只记录
RizomUVChineseLauncher.exe --dll=RizomUVChineseCollector.dll
```

正常操作一遍界面（切换面板、开菜单、悬停按钮），然后正常关闭。日志写到 `%TEMP%\rizomuv_collect_<pid>.log`，每行 `标签<TAB>原文`（UTF-8）。

采集器与运行时共用同一套 IAT 钩子，但只写日志不改文本，所以可以在英文界面上安全跑，不影响排版。

### 统计

```bash
python tools/check_coverage.py
```

输出把未命中项分成三类：

| 类别 | 含义 |
| --- | --- |
| 长段落片段 | 长帮助文本被按行拆开，运行时按比例切译文，不算缺失 |
| 自绘文本 | 只在测量路径出现、从不经过绘制路径。宿主用自带字形图集渲染，钩子层无法介入 |
| 真正缺失 | 需要补词条 |

「自绘文本」是架构限制，不是遗漏。这类文本替换了也画不出来，强行替换反而让测量宽度与实际绘制不一致。

### 运行时诊断（另一种数据源）

设置环境变量 `RIZOMUV_ZH_DEBUG=1` 启动，运行时会在进程正常退出时把**未命中**的字符串写到安装目录的 `missing_strings.txt`（UTF-16LE，`标签<TAB>次数<TAB>原文`）。

这个文件只记录未命中项，无法据此算覆盖率，但很适合快速确认「刚才界面上那句英文到底是什么」。

## 六、菜单栏

菜单是真正的 Win32 `HMENU`，不是自绘控件。`menu.cpp` 的做法：

1. 枚举本进程所有顶层窗口，用 `GetMenu()` 取菜单句柄；
2. 递归遍历子菜单，对每一项调 `GetMenuItemInfoW` 取文字；
3. 剥掉 `&` 助记符、按 `\t` 拆出快捷键后缀，只翻译前半部分；
4. `SetMenuItemInfoW(MIIM_STRING)` 写回，再 `DrawMenuBar` 重画。

菜单 ID、快捷键、勾选状态、子菜单结构都不动，所以行为完全一致。

宿主会在运行中重建菜单（例如切换模式时），因此 `menubar::start()` 起了一个 100 ms 间隔的扫描线程，持续 60 秒。已经翻译过的项会被跳过（写回前比对当前文字）。

## 七、调试

### 日志

运行时日志在 DLL 同目录的 `RizomUVChineseRuntime.log`；若目录不可写（安装在 Program Files 且未提权），回退到 `%LOCALAPPDATA%\RizomUVChinese\`。上限 256 KiB。

正常启动的日志长这样：

```
=== RizomUV 中文补丁运行时 ===
DLL 目录: E:\Program Files\Rizom Lab\RizomUV 2020.1
[词典] 已加载 1723 条词条
[钩子] 已改写 5 个 IAT 槽位
[钩子] 已改写 0 个 IAT 槽位
[钩子] 累计改写 5 个槽位
```

`已改写 5 个`说明宿主主模块导入了 5 个我们关心的 GDI 入口（第 6 个 `DrawStateW` 在这个版本没被导入）。后续几行是启动期补装，出现 0 是正常的。

### 常见问题

**界面全英文，日志显示词典已加载**

说明钩子没装上。检查日志里有没有 `[钩子] 已改写 N 个 IAT 槽位` 且 N > 0。若 N = 0，通常是宿主版本变了、模块布局不同，需要重新确认导入表。

**日志显示词典加载失败**

`dictionary_zh.json` 缺失或格式错误。日志会写明具体原因（根节点不是对象、translations 条目无效等）。

**中文显示成方块**

系统缺少中文字体。RizomUV 用系统字体渲染，中文 Windows 默认有微软雅黑；精简版系统可能缺字体。

**编译时报 `LNK1104: 无法打开文件 RizomUVChineseRuntime.dll`**

RizomUV 正在运行，DLL 被锁。先 `Get-Process rizomuv | Stop-Process -Force`。

**`cmd` 批处理解析出错**

`source/build.bat` 必须保持纯 ASCII。中文注释会被按 GBK 解析并截断命令。

## 八、发布

```bash
python tools/build_release.py --version 1.0.0
```

步骤：

1. `cmd /c source\build.bat` —— 编译运行时、启动器、采集器；
2. `csc` 编译 `installer/Setup.cs`，把三个载荷文件作为嵌入资源打进 `Setup.exe`（所以安装包是单文件）；
3. 打包 `release/`：安装包、绿色版 zip、`README-zh.txt`、`manifest.json`。

CI 见 `.github/workflows/release.yml`：push `v*` 标签或手动触发，`windows-latest` 自带 MSVC 与 .NET，直接构建并上传。

采集器**不**打进发布产物——它只是维护工具。

## 九、代码地图

| 文件 | 职责 |
| --- | --- |
| `source/dllmain.cpp` | 生命周期：等 gdi32 → 加载词典 → 装钩子 → 起菜单线程 → 刷新窗口 |
| `source/gdi_hook.cpp` | 六个 IAT 钩子、查表与回退、诊断记录 |
| `source/dictionary.cpp` | UTF-8→UTF-16、手写 JSON 解析、哈希查表、长段落切片 |
| `source/menu.cpp` | HMENU 遍历与替换 |
| `source/log.cpp` | 日志（带大小上限与回退路径） |
| `source/launcher.cpp` | 挂起创建 + 远程注入，支持 `--dll=` 指定注入目标 |
| `source/collector.cpp` | 采集器（只记录不翻译） |
| `installer/Setup.cs` | WinForms 安装器，`/S`、`/uninstall`、`/dir=` |
| `green/patch.ps1` | 绿色版 install/uninstall/status/shortcut |
| `tools/gen_dictionary.py` | 词表 → 词典 |
| `tools/check_dictionary.py` | 词典质量闸门（CI 用） |
| `tools/check_coverage.py` | 覆盖率统计 |
| `tools/build_release.py` | 编译 + 打包发布产物 |

## 十、改动时的注意事项

- **不要在 `DllMain` 里做实事。** 它处于 loader lock 内，此时 `LoadLibrary`、枚举模块、创建 GDI 对象都可能死锁。实测会让宿主启动致命错误。所有工作都在 `CreateThread` 出来的线程里做。
- **不要主动 `LoadLibrary("gdi32")`。** 注入发生在宿主加载器还没跑完时，强行加载会冲突。只轮询 `GetModuleHandleW`。
- **`DrawTextW` 在 user32，不在 gdi32。** 找错模块会拿到空指针。
- **`ExtTextOutW` 的 `dx` 只在未替换时传递。** 见上文。
- **`source/build.bat` 保持纯 ASCII。**
- **`kMaxLen` 与采集器的截断长度要一致。** 否则覆盖率统计会把同一句算成两个不同片段。
