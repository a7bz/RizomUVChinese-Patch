# RizomUV VS/RS 2020.1 简体中文汉化

RizomUV的简体中文界面补丁。汉化覆盖菜单栏、面板标题、按钮、下拉选项、工具提示与说明文字。

- 适用版本：**2020.1**（单文件 `rizomuv.exe`，实测 `2020.1.107.g6f7cd53.master`）
- **不修改 `rizomuv.exe`**，不写注册表，不接管文件关联
- 不需要改系统区域设置或代码页，英文 Windows 与 UTF-8 测试版都能正常显示中文
- 支持安装、卸载，卸载后完整还原英文

## 下载

到 [Releases](../../releases) 页面下载最新版本：

| 文件                                       | 说明                                         |
| ------------------------------------------ | -------------------------------------------- |
| `RizomUVChinese-Patch-v1.0.0.exe`          | 单文件安装包，自动检测安装目录，支持静默安装 |
| `RizomUVChinese-Patch-v1.0.0-Portable.zip` | 免安装绿色版，解压后运行 `安装.bat`          |
| `README-zh.txt`                            | 使用说明                                     |

> 发布资产使用 ASCII 文件名（GitHub 会清空中文文件名），下载后可按需自行改名。

## 使用

### 安装包版

双击安装包，按提示选择 RizomUV 安装目录。静默安装：

```
RizomUVChinese-Patch-v1.0.0.exe /S
RizomUVChinese-Patch-v1.0.0.exe /S /dir="E:\Program Files\Rizom Lab\RizomUV 2020.1"
RizomUVChinese-Patch-v1.0.0.exe /uninstall
```

安装后会创建桌面快捷方式「RizomUV 中文版」。

> **请用这个快捷方式启动。** 直接双击 `rizomuv.exe` 仍然是英文界面——补丁不会改动原程序。

### 绿色版

解压后双击 `安装.bat`，脚本会自动查找 RizomUV 安装目录（找不到时可手动粘贴路径）。其余脚本：

| 脚本               | 作用                                 |
| ------------------ | ------------------------------------ |
| `卸载.bat`         | 移除补丁并还原英文                   |
| `查看状态.bat`     | 显示安装位置、已安装文件与词典词条数 |
| `创建快捷方式.bat` | 重建桌面快捷方式                     |

绿色版不写注册表，整个文件夹可以拷到别的机器使用。

### 安装位置

补丁只往 RizomUV 安装目录新增三个文件：

```
RizomUVChineseLauncher.exe    启动器（注入运行时后启动 rizomuv.exe）
RizomUVChineseRuntime.dll     运行时（负责替换界面文字）
dictionary_zh.json            词典（1,722 条译文，UTF-8 JSON）
```

外加一个记录安装状态的 `chinese_patch.json`。若安装目录里本来就有同名文件，安装前会备份到 `chinese_patch_backup\`，卸载时还原。

## 实现原理

汉化不是改文件字节，而是**运行时接管文字绘制**。

启动器以挂起方式创建 `rizomuv.exe`，在它执行第一条指令之前注入 `RizomUVChineseRuntime.dll`，然后恢复运行。运行时在宿主进程里改写 IAT（导入地址表），把 GDI 的文字入口指向自己的实现：

| 入口                                                    | 作用                 |
| ------------------------------------------------------- | -------------------- |
| `ExtTextOutW` / `TextOutW` / `DrawTextW` / `DrawStateW` | 绘制                 |
| `GetTextExtentPoint32W` / `GetTextExtentExPointW`       | 测量（决定控件宽度） |

**绘制与测量必须用同一份译文**，否则控件会按英文宽度排版却画中文，造成文字溢出或截断。

之所以能显示中文而不改代码页：运行时交给 GDI 的是 UTF-16 字符串，GDI 直接从系统字体里取字形，与系统的 ANSI 代码页无关。这也是它比「把 GBK 字节塞进英文槽位」更可靠的原因——后者在英文系统（代码页 437/1252）上会直接乱码。

菜单栏是真正的 Win32 `HMENU`，运行时用 `SetMenuItemInfoW` 逐项替换文字再 `DrawMenuBar`，菜单 ID、快捷键、子菜单结构全部保持不变。宿主会在运行中重建菜单，所以这个扫描是周期性的，不是只做一次。

词典是**整串精确匹配**：不做子串替换，避免把 `Enable` 误伤到 `Enable Grid Snap` 之类的长句里。匹配不到时还有两级回退：

1. 去掉首尾空白再查一次（宿主常用空格做排版）；
2. 长段落按行拆分的情况，按字符比例从整段译文里切出对应片段。

## 已知限制

帮助面板里的少数长段落仍是英文。这类文本宿主只在**测量**路径调用 GDI、绘制时用自己的字形图集直接渲染，不经过任何可钩子的文字输出函数。在钩子层替换它只会让测量宽度与实际绘制不一致，反而破坏排版，因此保持原样。

品牌名（`RizomUV`、`Maya`、`Blender` 等）、单位符号（`px`、`cm`、`tu/cm`）、坐标轴标记（`Tu`/`Tv`/`Su`/`Sv`）、鼠标组合键（`LMB-Ctrl`）保持原样，这是刻意的。

## 仓库结构

```
installer/      C# 安装器源码（Setup.cs、app.manifest）
green/          绿色版脚本（.bat + PowerShell）
source/         运行时、启动器、采集器的 C++ 源码
translations/   词典（dictionary_zh.json）
tools/          词典生成、校验与打包脚本（Python）
docs/           开发文档
```

`translations/dictionary_zh.json` 是**编译产物**，由 `tools/gen_dictionary.py` 从词表生成，但它只是纯文本译文，不含 RizomUV 的任何程序文件，所以 CI 不需要安装游戏本体就能打包。

## 构建

需要 Visual Studio 2022 的 C++ 工具链（`vcvars64.bat`）与 Roslyn `csc.exe`。

```
python tools/build_release.py
```

产出到 `release/`：单文件安装包、绿色版 zip、使用说明、`manifest.json`（体积与 SHA-256）。

脚本会先调用 `source/build.bat` 编译 DLL 与启动器，再用 `csc` 把三个文件作为嵌入资源打进 `Setup.exe`。找不到编译器时可用环境变量 `CSC_PATH` / `VCVARS_PATH` 指定。

构建前可先自检：

```
python tools/check_dictionary.py     # 词典编码与格式
python tools/check_coverage.py       # 覆盖率（需要先采集一次字符串）
```

### 只改词典

```
python tools/gen_dictionary.py       # 重新生成 dictionary_zh.json
python tools/check_dictionary.py     # 校验
```

词表分两部分：`tools/gen_dictionary.py` 里的结构化词表（按界面区域分组），以及 `tools/dict_extra.py` 里的长句与工具提示。两者都不含中文以外的构建依赖。

### 刷新字符串清单

RizomUV 换版本、或要检查汉化遗漏时：

```
# 编译采集器
cmd /c source\build.bat

# 用采集器启动（界面保持英文，只记录不翻译）
RizomUVChineseLauncher.exe --dll=RizomUVChineseCollector.dll

# 正常操作一遍界面后退出，日志在 %TEMP%\rizomuv_collect_<pid>.log
python tools/check_coverage.py
```

采集器与运行时共用同一套 IAT 钩子，但它只写日志、不改文本，因此不会影响宿主排版。详见 [docs/development.md](docs/development.md)。

## 说明

本项目只分发界面翻译与加载工具，**不包含 RizomUV 的任何程序文件**。请先自行安装正版软件，再使用本补丁。

补丁通过 DLL 注入实现，部分安全软件可能提示风险。这是汉化工具的正常行为——它不联网、不修改系统设置、不持久驻留，退出 RizomUV 后即消失。若不放心，可自行审阅 `source/` 下的全部源码并从源码构建。

RizomUV 是 Rizom-Lab 的商标。本项目与 Rizom-Lab 无关联，未获其背书。
