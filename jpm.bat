@echo off
REM Juno Package Manager (JPM)

REM Get the directory of this batch file
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    exit /b 1
)

REM Run the JPM script
python "%JUNO_HOME%\jpm.py" %*

exit /b %ERRORLEVEL%