@echo off
REM Add juno2 to PATH - Run as administrator

echo ===================================================
echo Add Juno2 to PATH
echo ===================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrator privileges.
    echo Please right-click on this file and select "Run as administrator".
    echo.
    pause
    exit /b 1
)

REM Get the directory of this script
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

REM Check if juno2.bat exists
if not exist "%JUNO_HOME%\juno2.bat" (
    echo Error: juno2.bat not found in %JUNO_HOME%
    echo Please run this script from the Juno directory.
    pause
    exit /b 1
)

REM Add to system PATH
echo Adding %JUNO_HOME% to PATH...
setx PATH "%PATH%;%JUNO_HOME%" /M

if %errorLevel% neq 0 (
    echo Failed to add to PATH. Please check your permissions.
    pause
    exit /b 1
)

echo.
echo Juno2 has been successfully added to PATH!
echo You can now run 'juno2' from any directory.
echo.
echo Note: You may need to restart your command prompt or terminal
echo for the changes to take effect.
echo.

pause