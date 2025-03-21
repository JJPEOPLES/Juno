@echo off
REM Juno2 Wrapper - This file should be placed in a directory that's in the PATH
REM It will find and execute the actual juno2.bat script

REM Get the directory where Juno is installed
REM This assumes the wrapper is in the same directory as the registry key
for /f "tokens=2*" %%a in ('reg query "HKLM\SOFTWARE\Juno" /v "InstallDir" 2^>nul') do set "JUNO_DIR=%%b"

REM If registry key not found, try environment variable
if "%JUNO_DIR%"=="" (
    if not "%JUNO_HOME%"=="" (
        set "JUNO_DIR=%JUNO_HOME%"
    )
)

REM If still not found, try to find it in common locations
if "%JUNO_DIR%"=="" (
    if exist "C:\Program Files\Juno\juno2.bat" (
        set "JUNO_DIR=C:\Program Files\Juno"
    ) else if exist "C:\Program Files (x86)\Juno\juno2.bat" (
        set "JUNO_DIR=C:\Program Files (x86)\Juno"
    ) else if exist "%USERPROFILE%\Juno\juno2.bat" (
        set "JUNO_DIR=%USERPROFILE%\Juno"
    )
)

REM Check if we found the Juno directory
if "%JUNO_DIR%"=="" (
    echo Error: Could not find Juno installation.
    echo Please make sure Juno is installed correctly.
    echo You can set the JUNO_HOME environment variable to the Juno installation directory.
    exit /b 1
)

REM Check if the juno2.bat file exists
if not exist "%JUNO_DIR%\juno2.bat" (
    echo Error: juno2.bat not found in "%JUNO_DIR%".
    echo Please make sure Juno is installed correctly.
    exit /b 1
)

REM Execute the actual juno2.bat script with all arguments
call "%JUNO_DIR%\juno2.bat" %*
exit /b %ERRORLEVEL%