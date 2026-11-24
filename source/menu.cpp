#include "menu.h"

#include <windows.h>

#include <atomic>
#include <string>

#include "dictionary.h"
#include "log.h"

namespace menubar {
namespace {

std::atomic<int> g_translated{0};
std::atomic<bool> g_stop{false};
HANDLE g_thread = nullptr;

constexpr UINT kMiimString = 0x40;
constexpr UINT kMiimSubmenu = 0x04;
constexpr UINT kMiimFtype = 0x100;
constexpr UINT kMftSeparator = 0x800;

struct MenuItemInfoW {
  UINT cbSize;
  UINT fMask;
  UINT fType;
  UINT fState;
  UINT wID;
  HMENU hSubMenu;
  HBITMAP hbmpChecked;
  HBITMAP hbmpUnchecked;
  ULONG_PTR dwItemData;
  LPWSTR dwTypeData;
  UINT cch;
  HBITMAP hbmpItem;
};

// 去掉助记符 &，返回显示文本
std::wstring strip_amp(const std::wstring& s) {
  std::wstring out;
  out.reserve(s.size());
  for (wchar_t c : s) {
    if (c != L'&') out.push_back(c);
  }
  return out;
}

// 读取菜单项文字。返回 false 表示读取失败（含分隔符）。
bool get_text(HMENU menu, UINT pos, std::wstring& out, bool& is_separator, HMENU& sub) {
  MenuItemInfoW mii = {};
  mii.cbSize = sizeof(mii);
  mii.fMask = kMiimString | kMiimFtype | kMiimSubmenu;
  mii.dwTypeData = nullptr;
  mii.cch = 0;
  if (!GetMenuItemInfoW(menu, pos, TRUE, (MENUITEMINFOW*)&mii)) return false;

  is_separator = (mii.fType & kMftSeparator) != 0;
  sub = mii.hSubMenu;
  if (is_separator) { out.clear(); return true; }

  mii.cch += 1;
  std::wstring buf(mii.cch, L'\0');
  mii.dwTypeData = &buf[0];
  if (!GetMenuItemInfoW(menu, pos, TRUE, (MENUITEMINFOW*)&mii)) return false;
  buf.resize(mii.cch);
  // 去掉尾部 NUL
  while (!buf.empty() && buf.back() == L'\0') buf.pop_back();
  out = buf;
  return true;
}

// 只替换文字，保留 ID / 快捷键 / 图标 / 子菜单。
bool set_text(HMENU menu, UINT pos, const wchar_t* text) {
  MenuItemInfoW mii = {};
  mii.cbSize = sizeof(mii);
  mii.fMask = kMiimString;
  mii.dwTypeData = const_cast<LPWSTR>(text);
  mii.cch = (UINT)wcslen(text);
  return SetMenuItemInfoW(menu, pos, TRUE, (MENUITEMINFOW*)&mii) != FALSE;
}

struct Result {
  int changed = 0;
  int visited = 0;
};

// 递归处理一个菜单层级
Result walk(HMENU menu, int depth) {
  Result r;
  if (!menu || depth > 3) return r;

  int count = GetMenuItemCount(menu);
  if (count <= 0) return r;

  bool any_changed = false;
  for (int i = 0; i < count; i++) {
    std::wstring text;
    bool sep = false;
    HMENU sub = nullptr;
    if (!get_text(menu, (UINT)i, text, sep, sub)) continue;
    r.visited++;

    if (!sep && !text.empty()) {
      std::wstring plain = strip_amp(text);
      // 去掉快捷键后缀（"\tCtrl-O"）再查表
      size_t tab = plain.find(L'\t');
      std::wstring label = (tab == std::wstring::npos) ? plain : plain.substr(0, tab);

      // 去掉首尾空白
      size_t b = label.find_first_not_of(L" \t");
      size_t e = label.find_last_not_of(L" \t");
      if (b != std::wstring::npos && e != std::wstring::npos) {
        label = label.substr(b, e - b + 1);
      }

      if (!label.empty()) {
        const wchar_t* zh = dict::lookup(label.c_str(), (int)label.size());
        if (zh) {
          // 保留原有的快捷键文本
          std::wstring merged = zh;
          if (tab != std::wstring::npos) merged += plain.substr(tab);
          if (set_text(menu, (UINT)i, merged.c_str())) {
            r.changed++;
            any_changed = true;
            g_translated++;
          }
        }
      }
    }

    if (sub) {
      Result child = walk(sub, depth + 1);
      r.changed += child.changed;
      r.visited += child.visited;
    }
  }

  if (any_changed) {
    // 让宿主重画菜单栏（DrawMenuBar 需要顶层窗口句柄）
    // 这里不直接调用，由调用方在整轮结束后统一处理
  }
  return r;
}

HWND find_main_window(DWORD pid) {
  struct Ctx {
    DWORD pid;
    HWND best;
    LONG best_area;
  } ctx = {pid, nullptr, 0};

  EnumWindows([](HWND hwnd, LPARAM lp) -> BOOL {
    Ctx* c = (Ctx*)lp;
    DWORD wpid = 0;
    GetWindowThreadProcessId(hwnd, &wpid);
    if (wpid != c->pid) return TRUE;
    if (!IsWindowVisible(hwnd)) return TRUE;

    // 必须有菜单，且尺寸足够大（排除启动画面与浮动面板）
    if (!GetMenu(hwnd)) return TRUE;
    RECT rc;
    if (!GetWindowRect(hwnd, &rc)) return TRUE;
    LONG area = (rc.right - rc.left) * (rc.bottom - rc.top);
    if (area > c->best_area) {
      c->best_area = area;
      c->best = hwnd;
    }
    return TRUE;
  }, (LPARAM)&ctx);

  return ctx.best;
}

DWORD WINAPI worker(LPVOID) {
  DWORD pid = GetCurrentProcessId();

  // 宿主会在启动阶段反复重建菜单，持续扫描一段时间。
  // 60 秒足够覆盖启动、加载工程、切换编辑模式等场景。
  for (int tick = 0; tick < 600 && !g_stop.load(); tick++) {
    HWND hwnd = find_main_window(pid);
    if (hwnd) {
      HMENU menu = GetMenu(hwnd);
      if (menu) {
        Result r = walk(menu, 0);
        if (r.changed > 0) {
          DrawMenuBar(hwnd);
        }
      }
    }
    Sleep(100);
  }

  rzlog::printf("[菜单] 共翻译 %d 个菜单项", g_translated.load());
  return 0;
}

}  // namespace

void start() {
  g_stop = false;
  g_thread = CreateThread(nullptr, 0, worker, nullptr, 0, nullptr);
}

void stop() {
  g_stop = true;
  if (g_thread) {
    WaitForSingleObject(g_thread, 3000);
    CloseHandle(g_thread);
    g_thread = nullptr;
  }
}

int translated() { return g_translated.load(); }

}  // namespace menubar
