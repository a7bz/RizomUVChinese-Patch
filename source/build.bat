@echo off
rem Build RizomUV Chinese runtime DLL and launcher.
rem Requires Visual Studio 2022 C++ x64 toolchain (or Build Tools).
rem Output: build\out
setlocal enabledelayedexpansion

set ROOT=%~dp0..
set OUT=%ROOT%\build\out
set OBJ=%ROOT%\build\obj

if not exist "%OUT%" mkdir "%OUT%"
if not exist "%OBJ%" mkdir "%OBJ%"
rem Each translation unit gets its own object directory; the collector needs its own.
if not exist "%OBJ%\collector" mkdir "%OBJ%\collector"

set VCVARS=
for %%P in (
  "%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
  "%ProgramFiles%\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
  "%ProgramFiles%\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
  "%ProgramFiles%\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
  "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
) do (
  if not defined VCVARS if exist %%P set VCVARS=%%~P
)

if not defined VCVARS (
  echo [ERROR] vcvars64.bat not found. Install "Desktop development with C++".
  exit /b 1
)

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
