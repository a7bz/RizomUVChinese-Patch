// 字符串采集器：只记录宿主调用过的界面文本，不翻译。
//
// 用途：当 RizomUV 发布新版本、或需要检查汉化遗漏时，用它跑一遍界面，
// 得到一份完整的「宿主实际使用过的字符串清单」，再交给
// tools/check_coverage.py 统计覆盖率、找出未翻译条目。
//
// 与运行时 DLL 的关系：
//   两者都靠 IAT 改写拦截同一组 GDI 入口，但本采集器只写日志、不改文本，
//   因此可以在英文界面上安全运行，不会影响宿主的排版。
//
// 输出：%TEMP%\rizomuv_collect_<pid>.log，每行 `标签<TAB>原文`（UTF-8）。
//
// 编译：source/build.bat 会一并编译到 build/out/RizomUVChineseCollector.dll，
//      再用 build/out/RizomUVChineseLauncher.exe 注入（启动器会把同目录的
//      Runtime DLL 换成本 DLL 时请用 --dll 参数指定）。
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <psapi.h>

#include <stdio.h>
#include <string.h>

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

CRITICAL_SECTION g_cs;
HANDLE g_log = INVALID_HANDLE_VALUE;

// 去重表：按 (标签, 原文) 组合做哈希，避免同一字符串被反复写入。
// 只用哈希会有极小概率碰撞，但这里只为采集清单，可接受。
constexpr unsigned kHashSize = 1u << 18;
unsigned long long g_seen[kHashSize] = {0};

// 单条字符串的最大采集长度。超长的帮助文本会被截断，
// check_coverage.py 会把截断片段按「长段落片段」归类。
constexpr int kMaxLen = 600;

unsigned long long key_hash(const char* tag, const wchar_t* s, int n) {
  unsigned long long h = 1469598103934665603ULL;
  for (const char* p = tag; *p; p++) {
    h ^= (unsigned char)*p;
    h *= 1099511628211ULL;
  }
  h ^= 0xFF;
  h *= 1099511628211ULL;
  for (int i = 0; i < n; i++) {
    h ^= (unsigned long long)(unsigned short)s[i];
    h *= 1099511628211ULL;
  }
  return h ? h : 1;
}

void utf8_append(char* out, int* len, int cap, unsigned int cp) {
  if (cp < 0x80) {
    if (*len < cap) out[(*len)++] = (char)cp;
  } else if (cp < 0x800) {
    if (*len + 2 <= cap) {
      out[(*len)++] = (char)(0xC0 | (cp >> 6));
      out[(*len)++] = (char)(0x80 | (cp & 0x3F));
    }
  } else if (cp < 0x10000) {
    if (*len + 3 <= cap) {
      out[(*len)++] = (char)(0xE0 | (cp >> 12));
      out[(*len)++] = (char)(0x80 | ((cp >> 6) & 0x3F));
      out[(*len)++] = (char)(0x80 | (cp & 0x3F));
    }
  } else {
    if (*len + 4 <= cap) {
      out[(*len)++] = (char)(0xF0 | (cp >> 18));
      out[(*len)++] = (char)(0x80 | ((cp >> 12) & 0x3F));
      out[(*len)++] = (char)(0x80 | ((cp >> 6) & 0x3F));
      out[(*len)++] = (char)(0x80 | (cp & 0x3F));
    }
  }
}

int wlen_cap(const wchar_t* s, int cap) {
  if (!s) return 0;
  int n = 0;
  while (n < cap && s[n]) n++;
  return n;
}

void log_line(const char* tag, const wchar_t* s, int n) {
  if (g_log == INVALID_HANDLE_VALUE || !s || n <= 0) return;
  if (n > kMaxLen) n = kMaxLen;

  // 过滤掉纯控制字符的调用（有些调用传的是字形数组）
  int printable = 0;
  for (int i = 0; i < n; i++) {
    if ((unsigned short)s[i] >= 32) printable++;
  }
  if (!printable) return;

  unsigned long long h = key_hash(tag, s, n);
  unsigned int idx = (unsigned int)(h & (kHashSize - 1));

  EnterCriticalSection(&g_cs);
  bool fresh = false;
  for (unsigned int probe = 0; probe < 8; probe++) {
    unsigned int k = (idx + probe) & (kHashSize - 1);
    if (g_seen[k] == h) break;
    if (g_seen[k] == 0) {
      g_seen[k] = h;
      fresh = true;
      break;
    }
  }

  if (fresh) {
    char buf[8192];
    int len = 0;
    for (const char* p = tag; *p && len < 24; p++) buf[len++] = *p;
    buf[len++] = '\t';
    for (int i = 0; i < n && len < (int)sizeof(buf) - 8; i++) {
      utf8_append(buf, &len, (int)sizeof(buf) - 4, (unsigned int)(unsigned short)s[i]);
    }
    buf[len++] = '\n';
    DWORD written = 0;
    WriteFile(g_log, buf, (DWORD)len, &written, nullptr);
  }
  LeaveCriticalSection(&g_cs);
}

// ---------------- 钩子 ----------------

BOOL WINAPI hook_ExtTextOutW(HDC hdc, int x, int y, UINT flags, const RECT* rc,
                             LPCWSTR s, UINT cb, const INT* dx) {
  // 字形索引模式传的是字形号，不是文本
  if (!(flags & ETO_GLYPH_INDEX) && s && cb) {
    log_line("ExtTextOutW", s, (int)cb);
  }
  return g_real_ExtTextOutW(hdc, x, y, flags, rc, s, cb, dx);
}

BOOL WINAPI hook_TextOutW(HDC hdc, int x, int y, LPCWSTR s, int cb) {
  if (s && cb > 0) log_line("TextOutW", s, cb);
  return g_real_TextOutW(hdc, x, y, s, cb);
}

int WINAPI hook_DrawTextW(HDC hdc, LPCWSTR s, int cb, LPRECT rc, UINT fmt) {
  if (s && cb != 0) {
    int n = (cb < 0) ? wlen_cap(s, kMaxLen) : cb;
    log_line("DrawTextW", s, n);
  }
  return g_real_DrawTextW(hdc, s, cb, rc, fmt);
}

BOOL WINAPI hook_GetTextExtentPoint32W(HDC hdc, LPCWSTR s, int cb, LPSIZE sz) {
  if (s && cb > 0) log_line("GetTextExtentPoint32W", s, cb);
  return g_real_GetTextExtentPoint32W(hdc, s, cb, sz);
}

BOOL WINAPI hook_GetTextExtentExPointW(HDC hdc, LPCWSTR s, int cb, int maxExt,
                                       LPINT fit, LPINT dxs, LPSIZE sz) {
  if (s && cb > 0) log_line("GetTextExtentExPointW", s, cb);
  return g_real_GetTextExtentExPointW(hdc, s, cb, maxExt, fit, dxs, sz);
}

BOOL WINAPI hook_DrawStateW(HDC hdc, HBRUSH br, DRAWSTATEPROC proc, LPARAM data,
                            LPCWSTR s, int cb, UINT flags, int cx, int cy,
                            int x, int y, UINT fmt) {
  if (s && cb > 0) log_line("DrawStateW", s, cb);
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
        iat->u1.Function = (ULONG_PTR)g_slots[i].hook;
        VirtualProtect(&iat->u1.Function, sizeof(void*), old_protect, &old_protect);
        hits++;
        break;
      }
    }
  }
  return hits;
}

int install_all() {
  HMODULE mods[512];
  DWORD needed = 0;
  if (!EnumProcessModules(GetCurrentProcess(), mods, sizeof(mods), &needed)) return 0;

  int n = (int)(needed / sizeof(HMODULE));
  int total = 0;
  for (int i = 0; i < n; i++) {
    if (!host_dir_matches(mods[i])) continue;
    total += patch_module(mods[i]);
  }
  return total;
}

// ---------------- 生命周期 ----------------

void log_msg(const char* m) {
  if (g_log == INVALID_HANDLE_VALUE) return;
  DWORD written = 0;
  WriteFile(g_log, m, (DWORD)strlen(m), &written, nullptr);
}

DWORD WINAPI worker(LPVOID) {
  // 等宿主把 gdi32/user32 加载好。绝不主动 LoadLibrary。
  for (int i = 0; i < 600; i++) {
    if (GetModuleHandleW(L"gdi32.dll") && GetModuleHandleW(L"user32.dll")) break;
    Sleep(50);
  }

  HMODULE gdi = GetModuleHandleW(L"gdi32.dll");
  HMODULE user = GetModuleHandleW(L"user32.dll");
  if (!gdi || !user) {
    log_msg("gdi32/user32 not loaded\r\n");
    return 0;
  }

  g_real_ExtTextOutW = (PFN_ExtTextOutW)GetProcAddress(gdi, "ExtTextOutW");
  g_real_TextOutW = (PFN_TextOutW)GetProcAddress(gdi, "TextOutW");
  g_real_GetTextExtentPoint32W = (PFN_GetTextExtentPoint32W)GetProcAddress(gdi, "GetTextExtentPoint32W");
  g_real_GetTextExtentExPointW = (PFN_GetTextExtentExPointW)GetProcAddress(gdi, "GetTextExtentExPointW");
  g_real_DrawTextW = (PFN_DrawTextW)GetProcAddress(user, "DrawTextW");
  g_real_DrawStateW = (PFN_DrawStateW)GetProcAddress(user, "DrawStateW");

  // 宿主会在启动阶段陆续加载模块，装两分钟以覆盖全部。
  int total = 0;
  for (int i = 0; i < 240; i++) {
    total += install_all();
    Sleep(500);
  }

  char buf[64];
  int n = wsprintfA(buf, "IAT patched: %d\r\n", total);
  DWORD written = 0;
  WriteFile(g_log, buf, (DWORD)n, &written, nullptr);
  return 0;
}

}  // namespace

BOOL WINAPI DllMain(HINSTANCE inst, DWORD reason, LPVOID) {
  if (reason == DLL_PROCESS_ATTACH) {
    DisableThreadLibraryCalls(inst);
    InitializeCriticalSection(&g_cs);

    wchar_t tmp[MAX_PATH];
    if (GetTempPathW(MAX_PATH, tmp)) {
      wchar_t path[MAX_PATH];
      wsprintfW(path, L"%srizomuv_collect_%lu.log", tmp, GetCurrentProcessId());
      g_log = CreateFileW(path, GENERIC_WRITE, FILE_SHARE_READ, nullptr,
                          CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
    }

    CreateThread(nullptr, 0, worker, nullptr, 0, nullptr);
  }
  return TRUE;
}
