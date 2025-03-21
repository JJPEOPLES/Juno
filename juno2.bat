@echo off
setlocal enabledelayedexpansion

REM Juno2 - Launcher for Juno Programming Language
REM Usage: juno2 [filename.juno]

REM Get the directory of this script
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Set PYTHONPATH to include the Juno directory
set "PYTHONPATH=%JUNO_HOME%;%PYTHONPATH%"

REM Check if the main script exists
if not exist "%JUNO_HOME%\__main__.py" (
    echo Error: Juno main script not found at "%JUNO_HOME%\__main__.py"
    echo Please make sure you're running this from the Juno directory.
    pause
    exit /b 1
)

REM Process arguments
set "FILE_ARG="
set "VERSION_FLAG="

REM Check for version flag
if "%~1"=="--version" (
    set "VERSION_FLAG=1"
) else if "%~1"=="-v" (
    set "VERSION_FLAG=1"
) else if not "%~1"=="" (
    REM Process file argument
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

REM Check if we should show version info
if defined VERSION_FLAG (
    REM Use the dedicated version script if available
    if exist "%JUNO_HOME%\juno_version.py" (
        python "%JUNO_HOME%\juno_version.py"
    ) else (
        REM Fall back to the standalone script with version flag
        python "%JUNO_HOME%\juno_standalone.py" --version
    )
) else (
    REM Use the direct executor for files
    if not "%FILE_ARG%"=="" (
        python "%JUNO_HOME%\juno_direct.py" "%FILE_ARG%" %2 %3 %4 %5 %6 %7 %8 %9
    ) else (
        REM Use the regular interpreter for REPL
        if exist "%JUNO_HOME%\juno_standalone.py" (
            python "%JUNO_HOME%\juno_standalone.py" %*
        ) else (
            python "%JUNO_HOME%\__main__.py" %*
        )
    )
)
set JUNO_EXIT_CODE=%ERRORLEVEL%

REM If no arguments were provided and we didn't show version, show usage
if "%~1"=="" (
    if not defined VERSION_FLAG (
        echo.
        echo Juno REPL has exited.
        echo To run a Juno file, use: juno2 yourfile.juno
        echo To check version, use: juno2 --version
        echo.
    )
)

exit /b %JUNO_EXIT_CODE%