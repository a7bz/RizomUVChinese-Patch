@echo off
rem Install the RizomUV Simplified Chinese patch (green/portable edition).
rem Runs patch.ps1 in this folder with the "install" action.
setlocal
set HERE=%~dp0

powershell -NoProfile -ExecutionPolicy Bypass -File "%HERE%patch.ps1" -Action install
if errorlevel 1 (
  echo.
  echo Install failed. See the message above.
  pause
)
exit /b %errorlevel%
