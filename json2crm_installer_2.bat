@echo off
chcp 1251 >nul
cd /d "%~dp0"

echo.
echo ====================================================
echo =               JSON2CRM Installer                 =
echo ====================================================
echo.

echo Installing dependencies...
pip install --default-timeout=100 requests
pip install --default-timeout=100 customtkinter
pip install --default-timeout=100 pyinstaller

echo.
echo Checking tkinter...
python -c "import tkinter" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: tkinter not found!
    pause
    exit /b 1
)

echo.
echo Compiling EXE...

python -m PyInstaller --clean --noconfirm ^
    --distpath=. ^
    --name="JSON2CRM" ^
    --onefile ^
    --windowed ^
    --icon="brand-json.ico" ^
    --hidden-import=tkinter ^
    --hidden-import=customtkinter ^
    --hidden-import=requests ^
    main.py

if not exist "JSON2CRM.exe" (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo Cleaning up...
if exist "build" rmdir /s /q "build"
if exist "*.spec" del *.spec

echo.
echo Creating desktop shortcut...

set "DESKTOP=%USERPROFILE%\Desktop"
set "EXE_PATH=%CD%\JSON2CRM.exe"
set "ICON_PATH=%CD%\brand-json.ico"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$WshShell = New-Object -ComObject WScript.Shell; ^
$Shortcut = $WshShell.CreateShortcut('%DESKTOP%\JSON2CRM.lnk'); ^
$Shortcut.TargetPath = '%EXE_PATH%'; ^
$Shortcut.WorkingDirectory = '%CD%'; ^
if (Test-Path '%ICON_PATH%') { $Shortcut.IconLocation = '%ICON_PATH%'; } ^
$Shortcut.Save();"

echo.
echo ====================================================
echo Build complete!
echo EXE: %EXE_PATH%
echo ====================================================
pause
