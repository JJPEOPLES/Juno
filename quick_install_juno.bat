@echo off
REM Juno Programming Language Quick Installer for Windows
REM This batch file provides a simple one-click installation for Juno

echo ===================================================
echo Juno Programming Language Quick Installer
echo ===================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%I in ('python --version 2^>^&1') do set PYTHON_VERSION=%%I
echo Found Python %PYTHON_VERSION%

REM Extract major and minor version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

REM Check if Python version is at least 3.7
if %PYTHON_MAJOR% LSS 3 (
    echo Python 3.7 or higher is required.
    echo Please install a newer version of Python.
    pause
    exit /b 1
)
if %PYTHON_MAJOR% EQU 3 (
    if %PYTHON_MINOR% LSS 7 (
        echo Python 3.7 or higher is required.
        echo Please install a newer version of Python.
        pause
        exit /b 1
    )
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo pip is not installed or not in PATH.
    echo Please make sure pip is installed with Python.
    pause
    exit /b 1
)

echo Python requirements satisfied. Installing Juno...
echo.

REM Install Juno
echo Installing Juno...
cd /d "%~dp0"

REM Install from source only
echo Installing from source...
pip install -e .

REM Check if installation was successful
juno --version >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo Installation failed. Please check the error messages above.
    pause
    exit /b 1
)

REM Create Juno directory in user's home
set JUNO_DIR=%USERPROFILE%\.juno
mkdir "%JUNO_DIR%\packages" 2>nul

REM Create a simple configuration file
echo Creating configuration file...
echo {
    "version": "0.1.0",
    "registry_url": "https://juno-lang.org/registry",
    "packages_dir": "%JUNO_DIR:\=\\%\\packages"
} > "%JUNO_DIR%\config.json"

REM Installation complete
echo.
echo ===================================================
echo Juno has been successfully installed!
echo ===================================================
echo.
echo You can now run Juno programs with:
echo   juno yourfile.juno
echo.
echo Or start the interactive REPL with:
echo   juno
echo.
echo For more information, run:
echo   juno --help
echo.

pause