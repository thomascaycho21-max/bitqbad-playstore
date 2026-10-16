@echo off
chcp 65001 >nul
title BitQbad PlayStore - Limpiar Cache
cd /d "%~dp0"

echo Limpiando cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc >nul 2>nul
if exist "%USERPROFILE%\.flet\cache" rd /s /q "%USERPROFILE%\.flet\cache"
if exist "cache" rd /s /q "cache"
if exist "temp" rd /s /q "temp"
if exist "logs\*.log" del /q "logs\*.log"
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"
if exist ".pytest_cache" rd /s /q ".pytest_cache"
if exist ".mypy_cache" rd /s /q ".mypy_cache"
mkdir cache 2>nul
mkdir temp 2>nul
mkdir logs 2>nul
echo [OK] Cache limpiada.
pause
