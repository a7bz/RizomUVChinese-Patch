#include "gdi_hook.h"

#include <windows.h>
#include <psapi.h>

#include <atomic>
#include <mutex>
#include <string>
#include <vector>

#include "dictionary.h"
#include "log.h"

namespace gdihook {
namespace {

using PFN_ExtTextOutW = BOOL(WINAPI*)(HDC, int, int, UINT, const RECT*, LPCWSTR, UINT, const INT*);
using PFN_TextOutW = BOOL(WINAPI*)(HDC, int, int, LPCWSTR, int);
using PFN_DrawTextW = int (WINAPI*)(HDC, LPCWSTR, int, LPRECT, UINT);
using PFN_GetTextExtentPoint32W = BOOL(WINAPI*)(HDC, LPCWSTR, int, LPSIZE);
using PFN_GetTextExtentExPointW = BOOL(WINAPI*)(HDC, LPCWSTR, int, int, LPINT, LPINT, LPSIZE);
using PFN_DrawStateW = BOOL(WINAPI*)(HDC, HBRUSH, DRAWSTATEPROC, LPARAM, LPCWSTR, int, UINT, int, int, int, int, UINT);

PFN_ExtTextOutW g_real_ExtTextOutW = nullptr;
PFN_TextOutW g_real_TextOutW = nullptr;
PFN_DrawTextW g_real_DrawTextW = nullptr;
PFN_GetTextExtentPoint32W g_real_GetTextExtentPoint32W = nullptr;
PFN_GetTextExtentExPointW g_real_GetTextExtentExPointW = nullptr;
PFN_DrawStateW g_real_DrawStateW = nullptr;

std::atomic<unsigned long long> g_draw{0};
std::atomic<unsigned long long> g_measure{0};
std::atomic<unsigned long long> g_hits{0};
std::atomic<unsigned long long> g_missed{0};
std::atomic<unsigned long long> g_glyph_draws{0};

int g_installed = 0;

// 线程局部缓冲：避免每次绘制都分配。GDI 调用是同步的，可安全复用。
thread_local std::wstring g_buf;

// 诊断模式：把未命中的字符串记录下来，便于补词条。
// 仅在环境变量 RIZOMUV_ZH_DEBUG=1 时启用，正常使用零开销。
bool g_debug = false;
std::mutex g_miss_mutex;
std::wstring g_miss_path;
struct MissEntry {
  std::wstring text;
  unsigned int count;
  const char* tag;
};
std::vector<MissEntry> g_misses;

void note_miss(const char* tag, const wchar_t* s, int n) {
  if (!g_debug || !s || n < 8) return;
  std::lock_guard<std::mutex> lock(g_miss_mutex);
  for (auto& e : g_misses) {
    if ((int)e.text.size() == n && wmemcmp(e.text.c_str(), s, (size_t)n) == 0) {
      e.count++;
      return;
    }
  }
  if (g_misses.size() >= 4000) return;
  g_misses.push_back({std::wstring(s, (size_t)n), 1, tag});
}

int wlen_cap(const wchar_t* s, int cap) {
  if (!s) return 0;
  int n = 0;
  while (n < cap && s[n]) n++;
  return n;
}

// 把译文按原文的行结构重新折行。
//
// 宿主会把长帮助文本预先按行折断后整段交给 GDI（字符串里带 \n），
// 词典里存的是不换行的完整原文，所以整串匹配会失败。这里先把空白
// 归一化再查表，命中后按原文的每行容量把译文重新折行：
// 中文按约两倍宽估算，每行放原文行宽的一半左右。
std::wstring rewrap_like(const std::wstring& zh, const std::wstring& original) {
  if (original.find(L'\n') == std::wstring::npos) return zh;

  std::vector<int> caps;
  size_t start = 0;
  while (true) {
    size_t nl = original.find(L'\n', start);
    size_t end = (nl == std::wstring::npos) ? original.size() : nl;
    int len = 0;
    for (size_t i = start; i < end; i++) {
      if (original[i] != L'\r') len++;
    }
    caps.push_back(len);
    if (nl == std::wstring::npos) break;
    start = nl + 1;
  }

  std::wstring out;
  size_t pos = 0;
  for (size_t li = 0; li < caps.size() && pos < zh.size(); li++) {
    // 中文约占两倍宽，容量取原文行宽的一半；至少留 4 个字
    int cap = (int)(caps[li] * 0.55);
    if (cap < 4) cap = 4;
    if (li + 1 == caps.size()) cap = (int)zh.size();  // 最后一行不限制
    int taken = 0;
    while (pos < zh.size() && taken < cap) {
      out.push_back(zh[pos++]);
      taken++;
    }
    if (pos < zh.size()) out.push_back(L'\n');
  }
  if (pos < zh.size()) out.append(zh, pos, std::wstring::npos);
  return out;
}

// 折叠所有空白（含换行）为单个空格，用于整段匹配
std::wstring collapse_ws(const wchar_t* s, int n) {
  std::wstring out;
  out.reserve((size_t)n);
  bool pending = false;
  for (int i = 0; i < n; i++) {
    wchar_t c = s[i];
    if (c == L' ' || c == L'\t' || c == L'\r' || c == L'\n') {
      if (!out.empty()) pending = true;
      continue;
    }
    if (pending) { out.push_back(L' '); pending = false; }
    out.push_back(c);
  }
  return out;
}

// 查表并复制到线程局部缓冲。返回 nullptr 表示未命中。
const wchar_t* translate(const char* tag, const wchar_t* s, int n, int* out_len) {
  if (!s || n <= 0) return nullptr;

  const wchar_t* zh = dict::lookup(s, n);
  if (zh) {
    g_buf.assign(zh);
    g_hits++;
    *out_len = (int)g_buf.size();
    return g_buf.c_str();
  }

  // 宿主有时用首尾空格做排版（如 " Padding "）。整串查不到时去掉空白
  // 再查一次，命中后把原空白补回去，避免破坏对齐。
  int b = 0, e = n;
  while (b < e && (s[b] == L' ' || s[b] == L'\t')) b++;
  while (e > b && (s[e - 1] == L' ' || s[e - 1] == L'\t')) e--;
  if (e > b && (b > 0 || e < n)) {
    const wchar_t* zh2 = dict::lookup(s + b, e - b);
    if (zh2) {
      g_buf.assign(s, (size_t)b);
      g_buf.append(zh2);
      g_buf.append(s + e, (size_t)(n - e));
      g_hits++;
      *out_len = (int)g_buf.size();
      return g_buf.c_str();
    }
  }

  // 长帮助文本带换行：归一化空白后再查，命中则按原文行宽重新折行。
  if (n >= 24) {
    std::wstring flat = collapse_ws(s, n);
    if (flat.size() != (size_t)n) {
      const wchar_t* zh3 = dict::lookup(flat.c_str(), (int)flat.size());
      if (zh3) {
        g_buf = rewrap_like(std::wstring(zh3), std::wstring(s, (size_t)n));
        g_hits++;
        *out_len = (int)g_buf.size();
        return g_buf.c_str();
      }
    }
  }

  // 宿主把长段落按行拆开后逐行绘制，单行匹配不到整段词条。
  // 按比例从整段译文里切出对应片段，拼起来仍是通顺的整段中文。
  if (n >= 12) {
    const wchar_t* zh4 = dict::lookup_fragment(s, n);
    if (zh4) {
      g_buf.assign(zh4);
      g_hits++;
      *out_len = (int)g_buf.size();
      return g_buf.c_str();
    }
  }

  g_missed++;
  note_miss(tag, s, n);
  return nullptr;
}

// ---------------- 钩子实现 ----------------

BOOL WINAPI hook_ExtTextOutW(HDC hdc, int x, int y, UINT flags, const RECT* rc,
                             LPCWSTR s, UINT cb, const INT* dx) {
  g_draw++;
  // 字形索引模式传的是字形号而不是文字，绝不能替换
  if (!(flags & ETO_GLYPH_INDEX) && s && cb) {
    int len = 0;
    const wchar_t* zh = translate("ExtTextOutW", s, (int)cb, &len);
    if (zh) {
      // dx 是原文字符的字距数组，长度不匹配时必须丢弃，否则 GDI 会读越界
      return g_real_ExtTextOutW(hdc, x, y, flags, rc, zh, (UINT)len, nullptr);
    }
  } else if ((flags & ETO_GLYPH_INDEX) && s && cb) {
    // 诊断：宿主有部分文字走预排版字形路径，这类文本无法按字符串替换。
    g_glyph_draws++;
  }
  return g_real_ExtTextOutW(hdc, x, y, flags, rc, s, cb, dx);
}

BOOL WINAPI hook_TextOutW(HDC hdc, int x, int y, LPCWSTR s, int cb) {
  g_draw++;
  if (s && cb > 0) {
    int len = 0;
    const wchar_t* zh = translate("TextOutW", s, cb, &len);
    if (zh) return g_real_TextOutW(hdc, x, y, zh, len);
  }
  return g_real_TextOutW(hdc, x, y, s, cb);
}

int WINAPI hook_DrawTextW(HDC hdc, LPCWSTR s, int cb, LPRECT rc, UINT fmt) {
  g_draw++;
  if (s && cb != 0) {
    int n = (cb < 0) ? wlen_cap(s, 8192) : cb;
    int len = 0;
    const wchar_t* zh = translate("DrawTextW", s, n, &len);
    if (zh) return g_real_DrawTextW(hdc, zh, -1, rc, fmt);
  }
  return g_real_DrawTextW(hdc, s, cb, rc, fmt);
}

BOOL WINAPI hook_GetTextExtentPoint32W(HDC hdc, LPCWSTR s, int cb, LPSIZE sz) {
  g_measure++;
  if (s && cb > 0) {
    int len = 0;
    const wchar_t* zh = translate("GetTextExtentPoint32W", s, cb, &len);
    if (zh) return g_real_GetTextExtentPoint32W(hdc, zh, len, sz);
  }
  return g_real_GetTextExtentPoint32W(hdc, s, cb, sz);
}

BOOL WINAPI hook_GetTextExtentExPointW(HDC hdc, LPCWSTR s, int cb, int maxExt,
                                       LPINT fit, LPINT dxs, LPSIZE sz) {
  g_measure++;
  if (s && cb > 0) {
    int len = 0;
    const wchar_t* zh = translate("GetTextExtentExPointW", s, cb, &len);
    if (zh) {
      // dxs 是按字符的字距数组，译文长度不同时必须丢弃，否则调用方读到垃圾
      return g_real_GetTextExtentExPointW(hdc, zh, len, maxExt, fit, nullptr, sz);
    }
  }
  return g_real_GetTextExtentExPointW(hdc, s, cb, maxExt, fit, dxs, sz);
}

BOOL WINAPI hook_DrawStateW(HDC hdc, HBRUSH br, DRAWSTATEPROC proc, LPARAM data,
                            LPCWSTR s, int cb, UINT flags, int cx, int cy,
                            int x, int y, UINT fmt) {
  g_draw++;
  if (s && cb > 0) {
    int len = 0;
    const wchar_t* zh = translate("DrawStateW", s, cb, &len);
    if (zh) return g_real_DrawStateW(hdc, br, proc, data, zh, len, flags, cx, cy, x, y, fmt);
  }
  return g_real_DrawStateW(hdc, br, proc, data, s, cb, flags, cx, cy, x, y, fmt);
}

// ---------------- IAT 改写 ----------------

struct Slot {
  const char* name;
  void* hook;
  void** real;
};

Slot g_slots[] = {
    {"ExtTextOutW", (void*)hook_ExtTextOutW, (void**)&g_real_ExtTextOutW},
    {"TextOutW", (void*)hook_TextOutW, (void**)&g_real_TextOutW},
    {"DrawTextW", (void*)hook_DrawTextW, (void**)&g_real_DrawTextW},
    {"GetTextExtentPoint32W", (void*)hook_GetTextExtentPoint32W, (void**)&g_real_GetTextExtentPoint32W},
    {"GetTextExtentExPointW", (void*)hook_GetTextExtentExPointW, (void**)&g_real_GetTextExtentExPointW},
    {"DrawStateW", (void*)hook_DrawStateW, (void**)&g_real_DrawStateW},
};
constexpr int kSlotCount = (int)(sizeof(g_slots) / sizeof(g_slots[0]));

bool name_eq(const char* a, const char* b) {
  while (*a && *a == *b) { a++; b++; }
  return *a == *b;
}

// 记录被改写的槽位，卸载时还原
struct Patched {
  ULONG_PTR* slot;
  ULONG_PTR original;
};
Patched g_patched[64];
int g_patched_count = 0;
std::mutex g_patch_mutex;

bool host_dir_matches(HMODULE mod) {
  wchar_t mod_path[MAX_PATH], exe_path[MAX_PATH];
  if (!GetModuleFileNameW(mod, mod_path, MAX_PATH)) return false;
  if (!GetModuleFileNameW(nullptr, exe_path, MAX_PATH)) return false;
  const wchar_t* a = wcsrchr(mod_path, L'\\');
  const wchar_t* b = wcsrchr(exe_path, L'\\');
  if (!a || !b) return false;
  size_t n = (size_t)(a - mod_path);
  if (n != (size_t)(b - exe_path)) return false;
  return _wcsnicmp(mod_path, exe_path, n) == 0;
}

int patch_module(HMODULE mod) {
  if (!mod) return 0;
  auto dos = (PIMAGE_DOS_HEADER)mod;
  if (dos->e_magic != IMAGE_DOS_SIGNATURE) return 0;
  auto nt = (PIMAGE_NT_HEADERS)((BYTE*)mod + dos->e_lfanew);
  if (nt->Signature != IMAGE_NT_SIGNATURE) return 0;

  auto& dir = nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT];
  if (!dir.VirtualAddress) return 0;

  int hits = 0;
  auto imp = (PIMAGE_IMPORT_DESCRIPTOR)((BYTE*)mod + dir.VirtualAddress);
  for (; imp->Name; imp++) {
    // 没有名称表时无法按名字识别，跳过（延迟导入也不处理，避免误读）
    if (!imp->OriginalFirstThunk) continue;

    auto thunk = (PIMAGE_THUNK_DATA)((BYTE*)mod + imp->OriginalFirstThunk);
    auto iat = (PIMAGE_THUNK_DATA)((BYTE*)mod + imp->FirstThunk);

    for (; thunk->u1.AddressOfData; thunk++, iat++) {
      if (thunk->u1.Ordinal & IMAGE_ORDINAL_FLAG) continue;
      auto ibn = (PIMAGE_IMPORT_BY_NAME)((BYTE*)mod + thunk->u1.AddressOfData);

      for (int i = 0; i < kSlotCount; i++) {
        if (!name_eq(g_slots[i].name, (const char*)ibn->Name)) continue;

        void* current = (void*)iat->u1.Function;
        if (current == g_slots[i].hook) break;   // 已安装

        if (!*g_slots[i].real) *g_slots[i].real = current;

        DWORD old_protect = 0;
        if (!VirtualProtect(&iat->u1.Function, sizeof(void*), PAGE_READWRITE, &old_protect)) break;

        {
          std::lock_guard<std::mutex> lock(g_patch_mutex);
          if (g_patched_count < (int)(sizeof(g_patched) / sizeof(g_patched[0]))) {
            g_patched[g_patched_count].slot = &iat->u1.Function;
            g_patched[g_patched_count].original = (ULONG_PTR)current;
            g_patched_count++;
          }
        }

        iat->u1.Function = (ULONG_PTR)g_slots[i].hook;
        VirtualProtect(&iat->u1.Function, sizeof(void*), old_protect, &old_protect);
        hits++;
        break;
      }
    }
  }
  return hits;
}

}  // namespace

int install() {
  // 只处理宿主同目录的模块：主 exe 与自带 DLL。
  // 系统 DLL 里的导入属于系统实现，改写它们会影响整个进程的其它组件。
  HMODULE mods[512];
  DWORD needed = 0;
  if (!EnumProcessModules(GetCurrentProcess(), mods, sizeof(mods), &needed)) {
    rzlog::write("[钩子] EnumProcessModules 失败");
    return 0;
  }

  int n = (int)(needed / sizeof(HMODULE));
  int total = 0;
  for (int i = 0; i < n; i++) {
    if (!host_dir_matches(mods[i])) continue;
    total += patch_module(mods[i]);
  }

  g_installed = total;
  rzlog::printf("[钩子] 已改写 %d 个 IAT 槽位", total);
  return total;
}

void uninstall() {
  std::lock_guard<std::mutex> lock(g_patch_mutex);
  for (int i = 0; i < g_patched_count; i++) {
    DWORD old = 0;
    if (VirtualProtect(g_patched[i].slot, sizeof(void*), PAGE_READWRITE, &old)) {
      *g_patched[i].slot = g_patched[i].original;
      VirtualProtect(g_patched[i].slot, sizeof(void*), old, &old);
    }
  }
  g_patched_count = 0;
  g_installed = 0;
}

int installed() { return g_installed; }

Stats stats() {
  Stats s;
  s.draw = g_draw.load();
  s.measure = g_measure.load();
  s.hits = g_hits.load();
  s.missed = g_missed.load();
  s.glyph = g_glyph_draws.load();
  return s;
}

bool debug_enabled() {
  wchar_t v[8];
  DWORD n = GetEnvironmentVariableW(L"RIZOMUV_ZH_DEBUG", v, 8);
  return n > 0 && v[0] == L'1';
}

void set_debug(bool on) { g_debug = on; }

int dump_misses(const wchar_t* path) {
  std::lock_guard<std::mutex> lock(g_miss_mutex);
  if (g_misses.empty()) return 0;

  HANDLE f = CreateFileW(path, GENERIC_WRITE, 0, nullptr, CREATE_ALWAYS,
                         FILE_ATTRIBUTE_NORMAL, nullptr);
  if (f == INVALID_HANDLE_VALUE) return 0;

  std::wstring out;
  out.reserve(g_misses.size() * 60);
  for (auto& e : g_misses) {
    out += e.tag ? std::wstring(e.tag, e.tag + strlen(e.tag)) : std::wstring(L"?");
    out += L'\t';
    out += std::to_wstring(e.count);
    out += L'\t';
    out += e.text;
    out += L"\r\n";
  }

  // 以 UTF-16LE + BOM 写入，方便用编辑器直接打开
  const unsigned short bom = 0xFEFF;
  DWORD written = 0;
  WriteFile(f, &bom, sizeof(bom), &written, nullptr);
  WriteFile(f, out.data(), (DWORD)(out.size() * sizeof(wchar_t)), &written, nullptr);
  CloseHandle(f);
  return (int)g_misses.size();
}

}  // namespace gdihook
