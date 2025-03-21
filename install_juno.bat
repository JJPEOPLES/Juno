@echo off
REM Juno Programming Language Installer for Windows
REM This batch file installs the Juno programming language

echo ===================================================
echo Juno Programming Language Installer
echo ===================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This installer requires administrator privileges.
    echo Please right-click on this file and select "Run as administrator".
    echo.
    pause
    exit /b 1
)

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

REM Create a virtual environment (optional)
set INSTALL_VENV=n
set /p INSTALL_VENV=Do you want to install Juno in a virtual environment? (y/n) [default: n]: 

if /i "%INSTALL_VENV%"=="y" (
    echo Creating virtual environment...
    python -m venv juno_venv
    
    echo Activating virtual environment...
    call juno_venv\Scripts\activate.bat
    
    echo Virtual environment activated.
)

REM Install Juno
echo Installing Juno...
cd /d "%~dp0"

REM No installation needed, just set up the environment
echo Setting up Juno environment...

REM Create a batch file to run Juno
echo @echo off > "%JUNO_DIR%\juno.bat"
echo set JUNO_HOME=%SCRIPT_DIR% >> "%JUNO_DIR%\juno.bat"
echo set PYTHONPATH=%%JUNO_HOME%%;%%PYTHONPATH%% >> "%JUNO_DIR%\juno.bat"
echo python "%%JUNO_HOME%%\juno\__main__.py" %%* >> "%JUNO_DIR%\juno.bat"

REM Add to PATH if requested
set ADD_TO_PATH=n
set /p ADD_TO_PATH=Do you want to add Juno to your PATH? (y/n) [default: n]:

if /i "%%ADD_TO_PATH%%"=="y" (
    echo Adding Juno to PATH...
    setx PATH "%%PATH%%;%%JUNO_DIR%%" /M
    echo Juno added to PATH.
)

REM ChInstall from source only
eck if installation was successful
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

REM Add Juno to PATH (optional)
set ADD_TO_PATH=n
set /p ADD_TO_PATH=Do you want to add Juno to your PATH? (y/n) [default: n]: 

if /i "%ADD_TO_PATH%"=="y" (
    echo Adding Juno to PATH...
    
    REM Get the Scripts directory where juno.exe is located
    for /f "tokens=*" %%i in ('where juno') do set JUNO_EXE=%%i
    for %%i in ("%JUNO_EXE%") do set SCRIPTS_DIR=%%~dpi
    
    REM Add to PATH using setx
    setx PATH "%PATH%;%SCRIPTS_DIR%" /M
    
    echo Juno added to PATH.
)

REM Create desktop shortcut (optional)
set CREATE_SHORTCUT=n
set /p CREATE_SHORTCUT=Do you want to create a desktop shortcut for Juno REPL? (y/n) [default: n]: 

if /i "%CREATE_SHORTCUT%"=="y" (
    echo Creating desktop shortcut...
    
    REM Get the path to juno.exe
    for /f "tokens=*" %%i in ('where juno') do set JUNO_EXE=%%i
    
    REM Create shortcut
    powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Juno REPL.lnk'); $Shortcut.TargetPath = '%JUNO_EXE%'; $Shortcut.Save()"
    
    echo Desktop shortcut created.
)

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

if /i "%INSTALL_VENV%"=="y" (
    echo Note: Juno is installed in a virtual environment.
    echo To use Juno, you need to activate the environment first:
    echo   call juno_venv\Scripts\activate.bat
    echo.
)

pause