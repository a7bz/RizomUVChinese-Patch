#include "log.h"

#include <windows.h>
#include <stdarg.h>
#include <stdio.h>

namespace rzlog {
namespace {

HANDLE g_file = INVALID_HANDLE_VALUE;
CRITICAL_SECTION g_cs;
bool g_cs_init = false;
wchar_t g_path[MAX_PATH] = {0};
constexpr DWORD kMaxSize = 256 * 1024;

void write_raw(const char* data, int len) {
  if (g_file == INVALID_HANDLE_VALUE || len <= 0) return;
  DWORD written = 0;
  WriteFile(g_file, data, (DWORD)len, &written, nullptr);
}

}  // namespace

void open(const wchar_t* dir) {
  if (!g_cs_init) {
    InitializeCriticalSection(&g_cs);
    g_cs_init = true;
  }

  wchar_t candidate[MAX_PATH];
  // 首选：DLL 同目录（绿色版，便于用户自查）
  _snwprintf_s(candidate, MAX_PATH, _TRUNCATE, L"%s\\RizomUVChineseRuntime.log", dir);
  g_file = CreateFileW(candidate, GENERIC_WRITE, FILE_SHARE_READ, nullptr,
                       CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
  if (g_file != INVALID_HANDLE_VALUE) {
    wcscpy_s(g_path, MAX_PATH, candidate);
    return;
  }

  // 回退到 %LOCALAPPDATA% 下的用户目录
  wchar_t base[MAX_PATH];
  DWORD n = GetEnvironmentVariableW(L"LOCALAPPDATA", base, MAX_PATH);
  if (n > 0 && n < MAX_PATH) {
    wchar_t folder[MAX_PATH];
    _snwprintf_s(folder, MAX_PATH, _TRUNCATE, L"%s\\RizomUVChinese", base);
    CreateDirectoryW(folder, nullptr);
    _snwprintf_s(candidate, MAX_PATH, _TRUNCATE, L"%s\\RizomUVChineseRuntime.log", folder);
    g_file = CreateFileW(candidate, GENERIC_WRITE, FILE_SHARE_READ, nullptr,
                         CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
    if (g_file != INVALID_HANDLE_VALUE) {
      wcscpy_s(g_path, MAX_PATH, candidate);
    }
  }
}

void close() {
  if (g_file != INVALID_HANDLE_VALUE) {
    CloseHandle(g_file);
    g_file = INVALID_HANDLE_VALUE;
  }
}

void write(const char* line) {
  if (g_file == INVALID_HANDLE_VALUE || !line) return;
  if (g_cs_init) EnterCriticalSection(&g_cs);
  LARGE_INTEGER size = {0};
  if (GetFileSizeEx(g_file, &size) && size.QuadPart < kMaxSize) {
    int len = 0;
    while (line[len]) len++;
    write_raw(line, len);
    write_raw("\r\n", 2);
  }
  if (g_cs_init) LeaveCriticalSection(&g_cs);
}

void printf(const char* fmt, ...) {
  char buf[1024];
  va_list ap;
  va_start(ap, fmt);
  int n = _vsnprintf_s(buf, sizeof(buf), _TRUNCATE, fmt, ap);
  va_end(ap);
  if (n > 0) write(buf);
}

const wchar_t* path() { return g_path; }

}  // namespace rzlog
