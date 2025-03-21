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
    echo Usage: juno filename.juno
)

exit /b %ERRORLEVEL%@echo off
setlocal

REM Simple Juno Launcher
REM This script runs the standalone Juno interpreter

REM Get the directory of this script
set "SCRIPT_DIR=%~dp0"

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check if the standalone script exists
if not exist "%SCRIPT_DIR%juno_standalone.py" (
    echo Error: Standalone Juno script not found.
    echo Please make sure juno_standalone.py is in the same directory as this batch file.
    pause
    exit /b 1
)

REM Process file argument
set "FILE_ARG="
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

echo Running Juno...
if not "%FILE_ARG%"=="" echo File: %FILE_ARG%

REM Run the standalone script with all arguments
if not "%FILE_ARG%"=="" (
    python "%SCRIPT_DIR%juno_standalone.py" "%FILE_ARG%" %2 %3 %4 %5 %6 %7 %8 %9
) else (
    python "%SCRIPT_DIR%juno_standalone.py" %*
)

REM Pause if no arguments were provided (REPL mode)
if "%~1"=="" pause

exit /b %ERRORLEVEL%