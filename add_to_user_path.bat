@echo off
setlocal enabledelayedexpansion

REM Add Juno to User PATH - No admin privileges required
REM This script adds the Juno directory to the user's PATH environment variable

REM Get the directory of this script
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

echo Adding Juno to your user PATH...

REM Get the current user PATH
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%b"

REM If user PATH doesn't exist, create it
if "!USER_PATH!"=="" (
    set "USER_PATH=%JUNO_HOME%"
) else (
    REM Check if Juno is already in PATH
    echo !USER_PATH! | findstr /C:"%JUNO_HOME%" >nul
    if !errorLevel! equ 0 (
        echo Juno is already in your PATH.
        goto :create_shortcut
    ) else (
        REM Add Juno to PATH
        set "USER_PATH=%JUNO_HOME%;!USER_PATH!"
    )
)

REM Set the user PATH
setx PATH "!USER_PATH!"
if !errorLevel! neq 0 (
    echo Error: Failed to add Juno to PATH.
    echo Trying alternative method...
    
    REM Try alternative method using PowerShell
    powershell -Command "[Environment]::SetEnvironmentVariable('PATH', '%JUNO_HOME%;' + [Environment]::GetEnvironmentVariable('PATH', 'User'), 'User')"
    if !errorLevel! neq 0 (
        echo Error: Failed to add Juno to PATH using PowerShell.
        echo Please manually add the following directory to your PATH:
        echo %JUNO_HOME%
    ) else (
        echo Successfully added Juno to PATH using PowerShell.
    )
) else (
    echo Successfully added Juno to PATH.
)

:create_shortcut
REM Create a shortcut in the user's Start Menu
echo Creating shortcut in Start Menu...
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if not exist "%STARTMENU%\Juno" mkdir "%STARTMENU%\Juno"

REM Create shortcut using PowerShell
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\Juno\Juno Programming Language.lnk'); $Shortcut.TargetPath = '%JUNO_HOME%\juno2.bat'; $Shortcut.WorkingDirectory = '%JUNO_HOME%'; $Shortcut.Description = 'Juno Programming Language'; $Shortcut.IconLocation = '%JUNO_HOME%\installer\icon.ico'; $Shortcut.Save()"

REM Create a desktop shortcut
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Juno.lnk'); $Shortcut.TargetPath = '%JUNO_HOME%\juno2.bat'; $Shortcut.WorkingDirectory = '%JUNO_HOME%'; $Shortcut.Description = 'Juno Programming Language'; $Shortcut.IconLocation = '%JUNO_HOME%\installer\icon.ico'; $Shortcut.Save()"

REM Create a batch file in the user's profile that can be used to run Juno
echo Creating juno2.bat in your user profile...
set "USER_BIN=%USERPROFILE%\bin"
if not exist "%USER_BIN%" mkdir "%USER_BIN%"

echo @echo off > "%USER_BIN%\juno2.bat"
echo REM Juno wrapper script >> "%USER_BIN%\juno2.bat"
echo call "%JUNO_HOME%\juno2.bat" %%* >> "%USER_BIN%\juno2.bat"

REM Add the user bin directory to PATH if it's not already there
echo !USER_PATH! | findstr /C:"%USER_BIN%" >nul
if !errorLevel! neq 0 (
    setx PATH "%USER_BIN%;!USER_PATH!"
)

echo.
echo Juno has been added to your user PATH.
echo Shortcuts have been created in your Start Menu and Desktop.
echo.
echo You may need to restart your command prompt for the changes to take effect.
echo.
echo You can now run Juno from any directory by typing:
echo   juno2 [filename.juno]
echo.

pause@echo off
setlocal enabledelayedexpansion

REM Add Juno to User PATH - No admin privileges required
REM This script adds the Juno directory to the user's PATH environment variable

REM Get the directory of this script
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

echo Adding Juno to your user PATH...

REM Get the current user PATH
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%b"

REM If user PATH doesn't exist, create it
if "!USER_PATH!"=="" (
    set "USER_PATH=%JUNO_HOME%"
) else (
    REM Check if Juno is already in PATH
    echo !USER_PATH! | findstr /C:"%JUNO_HOME%" >nul
    if !errorLevel! equ 0 (
        echo Juno is already in your PATH.
        goto :create_shortcut
    ) else (
        REM Add Juno to PATH
        set "USER_PATH=%JUNO_HOME%;!USER_PATH!"
    )
)

REM Set the user PATH
setx PATH "!USER_PATH!"
if !errorLevel! neq 0 (
    echo Error: Failed to add Juno to PATH.
    echo Trying alternative method...
    
    REM Try alternative method using PowerShell
    powershell -Command "[Environment]::SetEnvironmentVariable('PATH', '%JUNO_HOME%;' + [Environment]::GetEnvironmentVariable('PATH', 'User'), 'User')"
    if !errorLevel! neq 0 (
        echo Error: Failed to add Juno to PATH using PowerShell.
        echo Please manually add the following directory to your PATH:
        echo %JUNO_HOME%
    ) else (
        echo Successfully added Juno to PATH using PowerShell.
    )
) else (
    echo Successfully added Juno to PATH.
)

:create_shortcut
REM Create a shortcut in the user's Start Menu
echo Creating shortcut in Start Menu...
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if not exist "%STARTMENU%\Juno" mkdir "%STARTMENU%\Juno"

REM Create shortcut using PowerShell
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\Juno\Juno Programming Language.lnk'); $Shortcut.TargetPath = '%JUNO_HOME%\juno2.bat'; $Shortcut.WorkingDirectory = '%JUNO_HOME%'; $Shortcut.Description = 'Juno Programming Language'; $Shortcut.IconLocation = '%JUNO_HOME%\installer\icon.ico'; $Shortcut.Save()"

REM Create a desktop shortcut
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Juno.lnk'); $Shortcut.TargetPath = '%JUNO_HOME%\juno2.bat'; $Shortcut.WorkingDirectory = '%JUNO_HOME%'; $Shortcut.Description = 'Juno Programming Language'; $Shortcut.IconLocation = '%JUNO_HOME%\installer\icon.ico'; $Shortcut.Save()"

REM Create a batch file in the user's profile that can be used to run Juno
echo Creating juno2.bat in your user profile...
set "USER_BIN=%USERPROFILE%\bin"
if not exist "%USER_BIN%" mkdir "%USER_BIN%"

echo @echo off > "%USER_BIN%\juno2.bat"
echo REM Juno wrapper script >> "%USER_BIN%\juno2.bat"
echo call "%JUNO_HOME%\juno2.bat" %%* >> "%USER_BIN%\juno2.bat"

REM Add the user bin directory to PATH if it's not already there
echo !USER_PATH! | findstr /C:"%USER_BIN%" >nul
if !errorLevel! neq 0 (
    setx PATH "%USER_BIN%;!USER_PATH!"
)

echo.
echo Juno has been added to your user PATH.
echo Shortcuts have been created in your Start Menu and Desktop.
echo.
echo You may need to restart your command prompt for the changes to take effect.
echo.
echo You can now run Juno from any directory by typing:
echo   juno2 [filename.juno]
echo.

pause