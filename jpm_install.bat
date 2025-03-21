@echo off
REM Juno Package Manager Installer
REM This script installs the Juno Package Manager (JPM)

echo ===================================================
echo Juno Package Manager (JPM) Installer
echo ===================================================
echo.

REM Get the directory of this script
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Create the .juno directory structure
echo Creating Juno package directories...
set "JUNO_DIR=%USERPROFILE%\.juno"
set "PACKAGES_DIR=%JUNO_DIR%\packages"
set "REGISTRY_DIR=%JUNO_DIR%\registry"

if not exist "%JUNO_DIR%" mkdir "%JUNO_DIR%"
if not exist "%PACKAGES_DIR%" mkdir "%PACKAGES_DIR%"
if not exist "%REGISTRY_DIR%" mkdir "%REGISTRY_DIR%"

REM Create a simple configuration file
echo Creating configuration file...
echo {
echo     "version": "2.0.0",
echo     "registry_url": "https://juno-lang.org/registry",
echo     "packages_dir": "%PACKAGES_DIR:\=\\%",
echo     "juno_home": "%JUNO_HOME:\=\\%"
echo } > "%JUNO_DIR%\config.json"

REM Copy the JPM script to the Juno directory
echo Installing JPM...
copy "%JUNO_HOME%\jpm.bat" "%JUNO_HOME%\jpm.bat" >nul

REM Create a shortcut to JPM in the PATH
echo @echo off > "%JUNO_HOME%\bin\jpm.bat"
echo call "%JUNO_HOME%\jpm.bat" %%* >> "%JUNO_HOME%\bin\jpm.bat"

REM Create bin directory if it doesn't exist
if not exist "%JUNO_HOME%\bin" mkdir "%JUNO_HOME%\bin"

echo.
echo ===================================================
echo Juno Package Manager (JPM) has been installed!
echo ===================================================
echo.
echo You can now use JPM with the following commands:
echo.
echo   jpm install [package]    - Install a package
echo   jpm uninstall [package]  - Uninstall a package
echo   jpm list                 - List installed packages
echo   jpm update [package]     - Update a package
echo   jpm help                 - Show help information
echo.
echo Make sure the Juno bin directory is in your PATH:
echo   %JUNO_HOME%\bin
echo.

pause