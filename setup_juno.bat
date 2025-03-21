@echo off
REM Juno Programming Language Setup for Windows
REM This batch file sets up the Juno programming language without installation

echo ===================================================
echo Juno Programming Language Setup
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

echo Python requirements satisfied. Setting up Juno...
echo.

REM Get the directory of this script
set JUNO_HOME=%~dp0
set JUNO_HOME=%JUNO_HOME:~0,-1%

REM Create Juno directory in user's home
set JUNO_DIR=%USERPROFILE%\.juno
mkdir "%JUNO_DIR%" 2>nul
mkdir "%JUNO_DIR%\packages" 2>nul

REM Create a simple configuration file
echo Creating configuration file...
echo {
    "version": "0.1.0",
    "registry_url": "https://juno-lang.org/registry",
    "packages_dir": "%JUNO_DIR:\=\\%\\packages",
    "juno_home": "%JUNO_HOME:\=\\%"
} > "%JUNO_DIR%\config.json"

REM Create a batch file to run Juno
echo Creating juno.bat...
echo @echo off > "%JUNO_DIR%\juno.bat"
echo set JUNO_HOME=%JUNO_HOME% >> "%JUNO_DIR%\juno.bat"
echo set PYTHONPATH=%%JUNO_HOME%%;%%PYTHONPATH%% >> "%JUNO_DIR%\juno.bat"
echo python "%%JUNO_HOME%%\juno\__main__.py" %%* >> "%JUNO_DIR%\juno.bat"

REM Add Juno to PATH (optional)
set ADD_TO_PATH=n
set /p ADD_TO_PATH=Do you want to add Juno to your PATH? (y/n) [default: n]: 

if /i "%ADD_TO_PATH%"=="y" (
    echo Adding Juno to PATH...
    setx PATH "%PATH%;%JUNO_DIR%" /M
    echo Juno added to PATH.
)

REM Create desktop shortcut (optional)
set CREATE_SHORTCUT=n
set /p CREATE_SHORTCUT=Do you want to create a desktop shortcut for Juno REPL? (y/n) [default: n]: 

if /i "%CREATE_SHORTCUT%"=="y" (
    echo Creating desktop shortcut...
    
    REM Create shortcut
    powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Juno REPL.lnk'); $Shortcut.TargetPath = '%JUNO_DIR%\juno.bat'; $Shortcut.Save()"
    
    echo Desktop shortcut created.
)

REM Setup complete
echo.
echo ===================================================
echo Juno has been successfully set up!
echo ===================================================
echo.
echo You can now run Juno programs with:
echo   %JUNO_DIR%\juno.bat yourfile.juno
echo.
echo Or start the interactive REPL with:
echo   %JUNO_DIR%\juno.bat
echo.

if /i "%ADD_TO_PATH%"=="y" (
    echo Since you added Juno to PATH, you can also use:
    echo   juno yourfile.juno
    echo   juno
    echo.
)

echo For quick access, you can also use the run_juno.bat script:
echo   run_juno.bat yourfile.juno
echo   run_juno.bat
echo.

pause