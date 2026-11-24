// RizomUVChineseLauncher.exe
//
// 职责：以挂起方式启动 rizomuv.exe，注入同目录的 RizomUVChineseRuntime.dll，
// 再恢复运行。不修改原程序、不接管文件关联。
//
// 失败处理：注入失败时给出明确提示，并询问是否直接启动原版（保持英文），
// 而不是静默启动一个没有汉化的程序让用户困惑。
#include <windows.h>
#include <shellapi.h>
#include <stdio.h>

#include <string>

namespace {

constexpr wchar_t kHostExe[] = L"rizomuv.exe";
constexpr wchar_t kRuntimeDll[] = L"RizomUVChineseRuntime.dll";

struct Options {
  bool ok = false;
  wchar_t exe[MAX_PATH] = {0};
  wchar_t dll[MAX_PATH] = {0};
  wchar_t workdir[MAX_PATH] = {0};
  std::wstring args;
};

void fail(const wchar_t* msg, DWORD err) {
  wchar_t buf[1024];
  if (err) {
    _snwprintf_s(buf, 1024, _TRUNCATE, L"%s\n\n错误代码: %lu", msg, err);
  } else {
    wcscpy_s(buf, 1024, msg);
  }
  MessageBoxW(nullptr, buf, L"RizomUV 中文版 启动失败", MB_ICONERROR | MB_OK);
}

// 从本程序所在目录解析宿主与运行时路径
Options resolve() {
  Options o;
  wchar_t self[MAX_PATH];
  if (!GetModuleFileNameW(nullptr, self, MAX_PATH)) return o;

  wchar_t* slash = wcsrchr(self, L'\\');
  if (!slash) return o;
  *slash = 0;
  wcscpy_s(o.workdir, MAX_PATH, self);

  // 支持两种布局：
  //   A. 与 rizomuv.exe 同目录（常见安装方式）
  //   B. ChineseLauncher\ 子目录，宿主在上一级
  wchar_t candidate[MAX_PATH];
  _snwprintf_s(candidate, MAX_PATH, _TRUNCATE, L"%s\\%s", self, kHostExe);
  if (GetFileAttributesW(candidate) != INVALID_FILE_ATTRIBUTES) {
    wcscpy_s(o.exe, MAX_PATH, candidate);
    wcscpy_s(o.workdir, MAX_PATH, self);
  } else {
    wchar_t parent[MAX_PATH];
    wcscpy_s(parent, MAX_PATH, self);
    wchar_t* p = wcsrchr(parent, L'\\');
    if (p) *p = 0;
    _snwprintf_s(candidate, MAX_PATH, _TRUNCATE, L"%s\\%s", parent, kHostExe);
    if (GetFileAttributesW(candidate) == INVALID_FILE_ATTRIBUTES) return o;
    wcscpy_s(o.exe, MAX_PATH, candidate);
    wcscpy_s(o.workdir, MAX_PATH, parent);
  }

  // 转交命令行参数（跳过 argv[0]）。
  // --dll=<路径> 供维护者指定别的注入目标（如字符串采集器），
  // 这个参数不会传给宿主。
  const wchar_t* dll_override = nullptr;
  std::wstring passthrough;

  int argc = 0;
  LPWSTR* argv = CommandLineToArgvW(GetCommandLineW(), &argc);
  if (argv) {
    for (int i = 1; i < argc; i++) {
      const wchar_t* a = argv[i];
      if (wcsncmp(a, L"--dll=", 6) == 0) {
        dll_override = a + 6;
        continue;
      }
      if (!passthrough.empty()) passthrough += L' ';
      bool need_quote = wcschr(a, L' ') != nullptr;
      if (need_quote) passthrough += L'"';
      passthrough += a;
      if (need_quote) passthrough += L'"';
    }
    o.args = passthrough;
    if (dll_override) {
      wcscpy_s(o.dll, MAX_PATH, dll_override);
    }
    LocalFree(argv);
  }

  if (!o.dll[0]) {
    _snwprintf_s(o.dll, MAX_PATH, _TRUNCATE, L"%s\\%s", self, kRuntimeDll);
  }
  if (GetFileAttributesW(o.dll) == INVALID_FILE_ATTRIBUTES) return o;

  o.ok = true;
  return o;
}

// 注入：远程线程调用 LoadLibraryW
bool inject(HANDLE proc, const wchar_t* dll, DWORD* out_hmod) {
  SIZE_T bytes = (wcslen(dll) + 1) * sizeof(wchar_t);
  void* remote = VirtualAllocEx(proc, nullptr, bytes, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
  if (!remote) return false;

  bool ok = false;
  if (WriteProcessMemory(proc, remote, dll, bytes, nullptr)) {
    HMODULE k32 = GetModuleHandleW(L"kernel32.dll");
    auto load = (LPTHREAD_START_ROUTINE)GetProcAddress(k32, "LoadLibraryW");
    HANDLE th = CreateRemoteThread(proc, nullptr, 0, load, remote, 0, nullptr);
    if (th) {
      WaitForSingleObject(th, 20000);
      DWORD code = 0;
      GetExitCodeThread(th, &code);
      CloseHandle(th);
      if (out_hmod) *out_hmod = code;
      ok = code != 0;
    }
  }
  VirtualFreeEx(proc, remote, 0, MEM_RELEASE);
  return ok;
}

}  // namespace

int wmain() {
  Options o = resolve();
  if (!o.ok) {
    fail(L"找不到 rizomuv.exe 或 RizomUVChineseRuntime.dll。\n\n"
         L"请把本程序放在 RizomUV 安装目录中（与 rizomuv.exe 同目录），"
         L"或放在该目录的 ChineseLauncher 子目录里。", 0);
    return 2;
  }

  std::wstring cmd = L"\"";
  cmd += o.exe;
  cmd += L"\"";
  if (!o.args.empty()) {
    cmd += L' ';
    cmd += o.args;
  }

  STARTUPINFOW si = {sizeof(si)};
  PROCESS_INFORMATION pi = {0};

  // CREATE_SUSPENDED 保证宿主还没执行任何指令就被注入，
  // 这样能赶上最早的界面初始化。
  if (!CreateProcessW(o.exe, &cmd[0], nullptr, nullptr, FALSE,
                      CREATE_SUSPENDED, nullptr, o.workdir, &si, &pi)) {
    fail(L"无法启动 rizomuv.exe。请确认已正常安装 RizomUV，"
         L"并检查安全软件是否拦截。", GetLastError());
    return 1;
  }

  DWORD hmod = 0;
  if (!inject(pi.hProcess, o.dll, &hmod)) {
    // 注入失败：不静默继续，交给用户决定
    int choice = MessageBoxW(nullptr,
        L"汉化运行时加载失败，界面将以英文启动。\n\n"
        L"可能原因：\n"
        L"  · 安全软件拦截了 RizomUVChineseRuntime.dll\n"
        L"  · 文件缺失或损坏\n\n"
        L"是否仍要启动 RizomUV？",
        L"RizomUV 中文版", MB_ICONWARNING | MB_YESNO);
    if (choice != IDYES) {
      TerminateProcess(pi.hProcess, 1);
      CloseHandle(pi.hThread);
      CloseHandle(pi.hProcess);
      return 1;
    }
  }

  ResumeThread(pi.hThread);
  CloseHandle(pi.hThread);
  CloseHandle(pi.hProcess);
  return 0;
}
