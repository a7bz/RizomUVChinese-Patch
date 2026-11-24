@echo off
rem Show whether the patch is installed, and where.
setlocal
set HERE=%~dp0

powershell -NoProfile -ExecutionPolicy Bypass -File "%HERE%patch.ps1" -Action status
exit /b %errorlevel%
