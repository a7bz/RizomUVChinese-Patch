// RizomUVChineseRuntime.dll 入口。
//
// 生命周期：
//   1. 启动器以挂起方式创建 rizomuv.exe，注入本 DLL，再恢复运行；
//   2. DllMain 里只做最小初始化（日志 + 启动工作线程）；
//   3. 工作线程等宿主把 gdi32/user32 加载好，再安装 IAT 钩子；
//   4. 同时启动菜单汉化线程。
//
// 为什么不在 DllMain 里做实事：
//   DllMain 处于 loader lock 内，此时调用 LoadLibrary / 枚举模块 / 创建 GDI 对象
//   都可能死锁或破坏宿主的加载器状态（实测会导致宿主启动致命错误）。
#include <windows.h>
#include <stdio.h>
#include <wchar.h>

#include <vector>

#include "dictionary.h"
#include "gdi_hook.h"
#include "log.h"
#include "menu.h"

namespace {

HMODULE g_self = nullptr;
HANDLE g_worker = nullptr;

// 取得本 DLL 所在目录
void self_dir(wchar_t* out, DWORD cap) {
  out[0] = 0;
  GetModuleFileNameW(g_self, out, cap);
  wchar_t* slash = wcsrchr(out, L'\\');
  if (slash) *slash = 0;
}

// 宿主的部分面板（如帮助面板）在启动早期就把文字画进离屏位图，
// 之后只做位图拷贝，因此那些文字永远不会再经过我们的钩子。
// 钩子装好后主动让所有窗口（含子窗口）失效一次，迫使它们重画。
void refresh_windows() {
  struct Ctx { DWORD pid; int count; } ctx = {GetCurrentProcessId(), 0};

  std::vector<HWND> tops;
  EnumWindows([](HWND hwnd, LPARAM lp) -> BOOL {
    ((std::vector<HWND>*)lp)->push_back(hwnd);
    return TRUE;
  }, (LPARAM)&tops);

  for (HWND top : tops) {
    DWORD pid = 0;
    GetWindowThreadProcessId(top, &pid);
    if (pid != ctx.pid) continue;

    InvalidateRect(top, nullptr, TRUE);
    UpdateWindow(top);
    ctx.count++;

    // EnumChildWindows 已经枚举全部后代，不需要再自己递归。
    EnumChildWindows(top, [](HWND child, LPARAM lp) -> BOOL {
      Ctx* c = (Ctx*)lp;
      InvalidateRect(child, nullptr, TRUE);
      UpdateWindow(child);
      c->count++;
      return TRUE;
    }, (LPARAM)&ctx);
  }

  if (ctx.count > 0) rzlog::printf("[刷新] 已请求 %d 个窗口重绘", ctx.count);
}

// 等宿主把文字绘制所需的系统 DLL 加载进来。
// 绝不主动 LoadLibrary：在注入早期强行加载会与宿主的加载器状态冲突。
bool wait_for_gdi() {
  for (int i = 0; i < 600; i++) {
    if (GetModuleHandleW(L"gdi32.dll") && GetModuleHandleW(L"user32.dll")) return true;
    Sleep(50);
  }
  return false;
}

DWORD WINAPI worker(LPVOID) {
  wchar_t dir[MAX_PATH];
  self_dir(dir, MAX_PATH);

  rzlog::open(dir);
  rzlog::write("=== RizomUV 中文补丁运行时 ===");
  rzlog::printf("DLL 目录: %ls", dir);

  if (!dict::load(dir)) {
    rzlog::printf("词典加载失败: %ls", dict::status());
    rzlog::write("界面保持英文。请检查 dictionary_zh.json 是否存在且格式正确。");
    return 0;
  }
  rzlog::printf("词典状态: %ls", dict::status());

  // 诊断模式：记录未命中的界面字符串，退出时写成 UTF-16 文本，
  // 供维护者补词条。正常使用不启用。
  if (gdihook::debug_enabled()) {
    gdihook::set_debug(true);
    rzlog::write("[诊断] 已启用未命中记录（RIZOMUV_ZH_DEBUG=1）");
  }

  if (!wait_for_gdi()) {
    rzlog::write("[钩子] 等待 gdi32/user32 超时，放弃安装");
    return 0;
  }

  // 钩子需要在宿主已加载文字绘制模块后安装。
  // 先立刻试一次，再在启动阶段反复补装（宿主可能稍后加载新模块）。
  int total = 0;
  for (int i = 0; i < 120; i++) {
    total += gdihook::install();
    if (total > 0 && i > 4) break;
    Sleep(500);
  }
  rzlog::printf("[钩子] 累计改写 %d 个槽位", total);

  menubar::start();

  // 让已经画好的面板重画一次，走上新装好的钩子。
  // 间隔几次，覆盖宿主启动后期的自身重绘。
  for (int i = 0; i < 3; i++) {
    Sleep(1200);
    refresh_windows();
  }

  return 0;
}

}  // namespace

BOOL WINAPI DllMain(HINSTANCE inst, DWORD reason, LPVOID) {
  if (reason == DLL_PROCESS_ATTACH) {
    g_self = inst;
    DisableThreadLibraryCalls(inst);
    // DllMain 内只创建线程，其余全部延后到线程里执行
    g_worker = CreateThread(nullptr, 0, worker, nullptr, 0, nullptr);
  } else if (reason == DLL_PROCESS_DETACH) {
    // 进程退出时把未命中的字符串写出来（仅诊断模式）。
    // 这里不能再创建线程或加载 DLL，只做一次文件写入。
    if (gdihook::debug_enabled()) {
      wchar_t dir[MAX_PATH];
      self_dir(dir, MAX_PATH);
      wchar_t path[MAX_PATH];
      _snwprintf_s(path, MAX_PATH, _TRUNCATE, L"%s\\missing_strings.txt", dir);
      int n = gdihook::dump_misses(path);
      rzlog::printf("[诊断] 已写出 %d 条未命中字符串", n);
    }
  }
  return TRUE;
}
