@echo off
REM Simple Juno Interpreter - Shows only program output

REM Get the directory of this batch file
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    exit /b 1
)

REM Process arguments
set "FILE_ARG="

REM Process file argument
if not "%~1"=="" (
    REM Check if the file exists
    if exist "%~1" (
        REM Get absolute path to the file
        set "FILE_ARG=%~f1"
    ) else if exist "%CD%\%~1" (
        REM Try current directory
        set "FILE_ARG=%CD%\%~1"
    ) else (
        REM Pass as-is and let Python handle it
        set "FILE_ARG=%~1"
    )
)

REM Run the file with the simple interpreter
if not "%FILE_ARG%"=="" (
    python "%JUNO_HOME%\simple_juno.py" "%FILE_ARG%"
) else (
    echo Usage: simple_juno filename.juno
)

exit /b %ERRORLEVEL%