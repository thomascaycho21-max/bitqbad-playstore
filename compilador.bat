@echo off
chcp 65001 >nul
title BitQbad PlayStore - Compilador
cd /d "%~dp0"

echo.
echo ============================================
echo   BitQbad PlayStore - COMPILADOR
echo   (compilacion MANUAL - tu decides cuando)
echo ============================================
echo.
echo   [1] Windows (.exe)
echo   [2] Linux
echo   [3] Android (.apk)
echo   [4] Android (.aab - Play Store)
echo   [5] iOS (.ipa)   - REQUIERE MAC
echo   [6] macOS (.app) - REQUIERE MAC
echo   [7] Web (build para Render)
echo   [8] Volver
echo.
set /p OPC="Elige [1-8]: "

if "%OPC%"=="1" (
    echo [INFO] Compilando Windows...
    flet build windows --project "BitQbadPlayStore" --product "BitQbad PlayStore" --org "com.bitqbad" --output copilacion\windows
    pause
) else if "%OPC%"=="2" (
    echo [INFO] Compilando Linux...
    flet build linux --project "BitQbadPlayStore" --product "BitQbad PlayStore" --org "com.bitqbad" --output copilacion\linux
    pause
) else if "%OPC%"=="3" (
    echo [INFO] Compilando Android APK...
    flet build apk --project "BitQbadPlayStore" --product "BitQbad PlayStore" --org "com.bitqbad" --output copilacion\android
    pause
) else if "%OPC%"=="4" (
    echo [INFO] Compilando Android AAB...
    flet build aab --project "BitQbadPlayStore" --product "BitQbad PlayStore" --org "com.bitqbad" --output copilacion\android
    pause
) else if "%OPC%"=="5" (
    echo [INFO] Compilando iOS... (solo funciona en Mac)
    flet build ipa --project "BitQbadPlayStore" --product "BitQbad PlayStore" --org "com.bitqbad" --output copilacion\ios
    pause
) else if "%OPC%"=="6" (
    echo [INFO] Compilando macOS... (solo funciona en Mac)
    flet build macos --project "BitQbadPlayStore" --product "BitQbad PlayStore" --org "com.bitqbad" --output copilacion\macos
    pause
) else if "%OPC%"=="7" (
    echo [INFO] Build web (para subir a Render)...
    flet build web --project "BitQbadPlayStore" --product "BitQbad PlayStore" --org "com.bitqbad" --output copilacion\web
    pause
) else (
    exit /b 0
)
