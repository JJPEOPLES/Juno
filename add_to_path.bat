@echo off
setlocal enabledelayedexpansion

REM Add Juno to PATH - Run as administrator
REM This script adds the Juno directory to the system PATH

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: This script requires administrator privileges.
    echo Please right-click on this script and select "Run as administrator".
    pause
    exit /b 1
)

REM Get the directory of this script
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

echo Adding Juno to system PATH...

REM Create registry key for Juno
reg add "HKLM\SOFTWARE\Juno" /v "InstallDir" /t REG_SZ /d "%JUNO_HOME%" /f
if %errorLevel% neq 0 (
    echo Warning: Could not create registry key. Continuing anyway.
)

REM Get the current PATH
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH') do set "CURRENT_PATH=%%b"

REM Check if Juno is already in PATH
echo !CURRENT_PATH! | findstr /C:"%JUNO_HOME%" >nul
if %errorLevel% equ 0 (
    echo Juno is already in PATH.
) else (
    REM Add Juno to PATH
    setx PATH "%JUNO_HOME%;%CURRENT_PATH%" /M
    if %errorLevel% neq 0 (
        echo Error: Failed to add Juno to PATH.
        pause
        exit /b 1
    ) else (
        echo Successfully added Juno to PATH.
    )
)

REM Create a copy of juno2.bat in Windows directory for direct access
echo Creating juno2.bat in Windows directory...
copy "%JUNO_HOME%\juno2_wrapper.bat" "%SystemRoot%\juno2.bat" >nul
if %errorLevel% neq 0 (
    echo Warning: Could not create juno2.bat in Windows directory.
    echo You may need to manually add Juno to your PATH.
) else (
    echo Successfully created juno2.bat in Windows directory.
)

echo.
echo Juno has been added to the system PATH.
echo You may need to restart your command prompt or computer for the changes to take effect.
echo.
echo You can now run Juno from any directory by typing:
echo   juno2 [filename.juno]
echo.

pause