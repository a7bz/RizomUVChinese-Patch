@echo off
rem Build RizomUV Chinese runtime DLL, launcher and string collector.
rem Requires a Visual Studio C++ x64 toolchain (2022, 2026 or Build Tools).
rem Output: build\out
setlocal enabledelayedexpansion

set ROOT=%~dp0..
set OUT=%ROOT%\build\out
set OBJ=%ROOT%\build\obj

if not exist "%OUT%" mkdir "%OUT%"
if not exist "%OBJ%" mkdir "%OBJ%"
rem Each translation unit gets its own object directory; the collector needs its own.
if not exist "%OBJ%\collector" mkdir "%OBJ%\collector"

rem --- Locate vcvars64.bat -------------------------------------------------
rem vswhere.exe ships with every VS 2017+ installer and knows the real install
rem path, so it survives Visual Studio version bumps (2022 -> 2026) that would
rem break hardcoded "Microsoft Visual Studio\2022" paths.
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
set VCVARS=

if not exist "%VSWHERE%" goto try_known

rem Kept outside an if-block on purpose: a for /f whose command is quoted
rem mis-parses when nested inside parentheses.
for /f "usebackq delims=" %%I in (`"%VSWHERE%" -latest -prerelease -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do (
  if exist "%%I\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%%I\VC\Auxiliary\Build\vcvars64.bat"
)

:try_known
rem Fallback: known layouts, including the VS 2026 (18) directory.
if not defined VCVARS (
  for %%P in (
    "%ProgramFiles%\Microsoft Visual Studio\18\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
    "%ProgramFiles%\Microsoft Visual Studio\18\Professional\VC\Auxiliary\Build\vcvars64.bat"
    "%ProgramFiles%\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
    "%ProgramFiles%\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
    "%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
    "%ProgramFiles%\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
    "%ProgramFiles%\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
    "%ProgramFiles%\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
    "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
  ) do (
    if not defined VCVARS if exist %%P set "VCVARS=%%~P"
  )
)

if not defined VCVARS (
  echo [ERROR] vcvars64.bat not found.
  echo         Install Visual Studio with the "Desktop development with C++" workload,
  echo         or run this script from a "x64 Native Tools Command Prompt".
  exit /b 1
)

echo Using %VCVARS%
call "%VCVARS%" >nul
if errorlevel 1 exit /b 1

set CFLAGS=/nologo /utf-8 /std:c++20 /EHsc /O2 /W4 /MT /DUNICODE /D_UNICODE /D_WIN32_WINNT=0x0601
set LIBS=user32.lib gdi32.lib psapi.lib shell32.lib

echo [1/3] Building RizomUVChineseRuntime.dll
cl %CFLAGS% /LD "%ROOT%\source\dllmain.cpp" "%ROOT%\source\dictionary.cpp" "%ROOT%\source\gdi_hook.cpp" "%ROOT%\source\menu.cpp" "%ROOT%\source\log.cpp" /Fo"%OBJ%\\" /Fe"%OUT%\RizomUVChineseRuntime.dll" /link %LIBS% /DLL
if errorlevel 1 goto fail

echo [2/3] Building RizomUVChineseLauncher.exe
cl %CFLAGS% "%ROOT%\source\launcher.cpp" /Fo"%OBJ%\\" /Fe"%OUT%\RizomUVChineseLauncher.exe" /link %LIBS%
if errorlevel 1 goto fail

rem The collector is a developer tool: it only logs strings, never translates.
echo [3/3] Building RizomUVChineseCollector.dll
cl %CFLAGS% /LD "%ROOT%\source\collector.cpp" /Fo"%OBJ%\\collector\\" /Fe"%OUT%\RizomUVChineseCollector.dll" /link %LIBS% /DLL
if errorlevel 1 goto fail

echo.
echo Build OK: %OUT%
dir /b "%OUT%"
exit /b 0

:fail
echo.
echo [FAILED]
exit /b 1
