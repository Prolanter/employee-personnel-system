@echo off
cd /d "%~dp0"
title Building Personnel System Installer...

echo ============================================================
echo   نظام ملفات الموظفين  -  Build + Installer
echo ============================================================
echo.

:: ── Check Python ─────────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo Install from https://python.org  and tick "Add to PATH".
    pause & exit /b 1
)
echo [OK] & python --version

:: ── Install dependencies ──────────────────────────────────────────────────────
echo.
echo [1/3] Installing dependencies...
python -m pip install --upgrade pip --quiet
python -m pip install cryptography Pillow pyinstaller --quiet
if errorlevel 1 ( echo [ERROR] pip install failed. & pause & exit /b 1 )
echo [OK] Dependencies ready.

:: ── Check logo files ─────────────────────────────────────────────────────────
echo.
echo Checking for logo files...
set HAS_PNG=0
set HAS_ICO=0
if exist "company_logo.png" ( set HAS_PNG=1 & echo [OK] company_logo.png found. )
if exist "company_logo.ico" ( set HAS_ICO=1 & echo [OK] company_logo.ico found. )
if %HAS_PNG%==0 echo [INFO] company_logo.png not found - app will use default icon.
if %HAS_ICO%==0 echo [INFO] company_logo.ico not found - taskbar will use default icon.

:: ── Clean previous build ──────────────────────────────────────────────────────
echo.
echo [2/3] Building EXE with PyInstaller...
if exist "dist"  rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "PersonnelSystem.spec" del /q "PersonnelSystem.spec"

:: ── Build icon flag ───────────────────────────────────────────────────────────
set ICON_FLAG=
if %HAS_ICO%==1 set ICON_FLAG=--icon="company_logo.ico"

:: ── Build add-data flags ──────────────────────────────────────────────────────
:: --add-data tells PyInstaller to bundle these files INSIDE the dist folder.
:: Format is "source;destination_folder" (use . for same folder as exe)
set DATA_FLAGS=
if %HAS_PNG%==1 set DATA_FLAGS=%DATA_FLAGS% --add-data "company_logo.png;."
if %HAS_ICO%==1 set DATA_FLAGS=%DATA_FLAGS% --add-data "company_logo.ico;."

:: ── Run PyInstaller ───────────────────────────────────────────────────────────
python -m PyInstaller ^
    --onedir ^
    --windowed ^
    --name "PersonnelSystem" ^
    %ICON_FLAG% ^
    %DATA_FLAGS% ^
    --hidden-import cryptography ^
    --hidden-import cryptography.fernet ^
    --hidden-import cryptography.hazmat.primitives.kdf.pbkdf2 ^
    --hidden-import PIL ^
    --hidden-import PIL.Image ^
    --hidden-import PIL.ImageTk ^
    --collect-all cryptography ^
    --noconfirm ^
    main.py

if not exist "dist\PersonnelSystem\PersonnelSystem.exe" (
    echo [ERROR] PyInstaller build failed. Read the output above.
    pause & exit /b 1
)
echo [OK] App built successfully.

:: ── Verify logo files are inside dist ────────────────────────────────────────
echo.
echo Verifying logo files in dist folder...
if %HAS_PNG%==1 (
    if exist "dist\PersonnelSystem\company_logo.png" (
        echo [OK] company_logo.png is bundled in dist.
    ) else (
        echo [WARN] company_logo.png was NOT bundled - copying manually...
        copy /y "company_logo.png" "dist\PersonnelSystem\company_logo.png" >nul
    )
)
if %HAS_ICO%==1 (
    if exist "dist\PersonnelSystem\company_logo.ico" (
        echo [OK] company_logo.ico is bundled in dist.
    ) else (
        echo [WARN] company_logo.ico was NOT bundled - copying manually...
        copy /y "company_logo.ico" "dist\PersonnelSystem\company_logo.ico" >nul
    )
)

:: ── Create installer with Inno Setup ─────────────────────────────────────────
echo.
echo [3/3] Creating installer...

set ISCC=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist "C:\Program Files\Inno Setup 6\ISCC.exe"       set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"
if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" set "ISCC=C:\Program Files (x86)\Inno Setup 5\ISCC.exe"

if "%ISCC%"=="" (
    echo.
    echo [WARNING] Inno Setup not found.
    echo Your app is ready at: dist\PersonnelSystem\PersonnelSystem.exe
    echo For a proper installer, install Inno Setup from:
    echo   https://jrsoftware.org/isdl.php
    echo Then run this script again.
    pause & exit /b 0
)

if not exist "installer_output" mkdir "installer_output"
"%ISCC%" "installer.iss"

if not exist "installer_output\PersonnelSystem_Setup_v1.0.exe" (
    echo [ERROR] Inno Setup failed.
    pause & exit /b 1
)

:: ── Done ─────────────────────────────────────────────────────────────────────
echo.
echo ============================================================
echo   SUCCESS!
echo ============================================================
echo.
echo   Installer file:
echo   %CD%\installer_output\PersonnelSystem_Setup_v1.0.exe
echo.
echo   This file can be copied to ANY Windows laptop and run
echo   to install the app with no Python required.
echo ============================================================
echo.
set /p OPEN="Open the installer folder now? (Y/N): "
if /i "%OPEN%"=="Y" explorer "%CD%\installer_output"
pause
