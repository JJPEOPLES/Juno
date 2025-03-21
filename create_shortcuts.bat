@echo off
setlocal enabledelayedexpansion

REM Create Juno Shortcuts
REM This script creates shortcuts for Juno without modifying PATH

REM Get the directory of this script
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

echo Creating Juno shortcuts...

REM Create a shortcut in the user's Start Menu
echo Creating shortcut in Start Menu...
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if not exist "%STARTMENU%\Juno" mkdir "%STARTMENU%\Juno"

REM Create shortcut using PowerShell
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\Juno\Juno Programming Language.lnk'); $Shortcut.TargetPath = '%JUNO_HOME%\juno2.bat'; $Shortcut.WorkingDirectory = '%JUNO_HOME%'; $Shortcut.Description = 'Juno Programming Language'; $Shortcut.IconLocation = '%JUNO_HOME%\installer\icon.ico'; $Shortcut.Save()"

REM Create a desktop shortcut
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Juno.lnk'); $Shortcut.TargetPath = '%JUNO_HOME%\juno2.bat'; $Shortcut.WorkingDirectory = '%JUNO_HOME%'; $Shortcut.Description = 'Juno Programming Language'; $Shortcut.IconLocation = '%JUNO_HOME%\installer\icon.ico'; $Shortcut.Save()"

REM Create a command prompt shortcut that opens in the Juno directory
echo Creating command prompt shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\Juno\Juno Command Prompt.lnk'); $Shortcut.TargetPath = 'cmd.exe'; $Shortcut.Arguments = '/K CD /D %JUNO_HOME%'; $Shortcut.WorkingDirectory = '%JUNO_HOME%'; $Shortcut.Description = 'Command Prompt with Juno'; $Shortcut.Save()"

REM Create a file association for .juno files
echo Creating file association for .juno files...

REM Check if we have permission to modify registry
reg add "HKCU\Software\Classes\.juno" /ve /t REG_SZ /d "JunoFile" /f >nul 2>&1
if !errorLevel! neq 0 (
    echo Warning: Could not create file association. You may need administrator privileges.
) else (
    reg add "HKCU\Software\Classes\JunoFile" /ve /t REG_SZ /d "Juno Source File" /f >nul
    reg add "HKCU\Software\Classes\JunoFile\DefaultIcon" /ve /t REG_SZ /d "%JUNO_HOME%\installer\icon.ico" /f >nul
    reg add "HKCU\Software\Classes\JunoFile\shell\open\command" /ve /t REG_SZ /d "\"%JUNO_HOME%\juno2.bat\" \"%%1\"" /f >nul
    
    echo File association created successfully.
)

REM Create a simple batch file that users can copy to any folder
echo Creating portable juno2.bat...
echo @echo off > "%JUNO_HOME%\portable_juno2.bat"
echo REM Portable Juno launcher - Copy this file to any folder where you want to use Juno >> "%JUNO_HOME%\portable_juno2.bat"
echo call "%JUNO_HOME%\juno2.bat" %%* >> "%JUNO_HOME%\portable_juno2.bat"

echo.
echo Shortcuts have been created in your Start Menu and Desktop.
echo A portable launcher has been created as portable_juno2.bat.
echo You can copy this file to any folder where you want to use Juno.
echo.
echo To run Juno:
echo 1. Use the desktop or Start Menu shortcuts
echo 2. Open the Juno Command Prompt and type: juno2
echo 3. Copy portable_juno2.bat to any folder and run it there
echo.

pause