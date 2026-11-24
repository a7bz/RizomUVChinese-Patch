@echo off
rem Re-create the "RizomUV 中文版" desktop shortcut for the installed patch.
setlocal
set HERE=%~dp0

powershell -NoProfile -ExecutionPolicy Bypass -File "%HERE%patch.ps1" -Action shortcut
exit /b %errorlevel%
