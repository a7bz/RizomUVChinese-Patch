@echo off
rem Remove the RizomUV Simplified Chinese patch and restore the English UI.
rem Runs patch.ps1 in this folder with the "uninstall" action.
setlocal
set HERE=%~dp0

powershell -NoProfile -ExecutionPolicy Bypass -File "%HERE%patch.ps1" -Action uninstall
if errorlevel 1 (
  echo.
  echo Uninstall failed. See the message above.
  pause
)
exit /b %errorlevel%
