@echo off
setlocal enabledelayedexpansion

REM Test Juno Installation
REM This script tests if Juno is installed correctly and can be run from the command line

echo Testing Juno installation...
echo.

REM Get the directory of this script
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

REM Test 1: Check if Python is installed
echo Test 1: Checking if Python is installed...
where python >nul 2>nul
if %errorLevel% neq 0 (
    echo FAILED: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    exit /b 1
) else (
    echo PASSED: Python is installed.
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo Python version: !PYTHON_VERSION!
)
echo.

REM Test 2: Check if juno2.bat exists
echo Test 2: Checking if juno2.bat exists...
if not exist "%JUNO_HOME%\juno2.bat" (
    echo FAILED: juno2.bat not found in "%JUNO_HOME%".
    exit /b 1
) else (
    echo PASSED: juno2.bat exists.
)
echo.

REM Test 3: Check if __main__.py exists
echo Test 3: Checking if __main__.py exists...
if not exist "%JUNO_HOME%\__main__.py" (
    echo FAILED: __main__.py not found in "%JUNO_HOME%".
    exit /b 1
) else (
    echo PASSED: __main__.py exists.
)
echo.

REM Test 4: Check if juno directory exists
echo Test 4: Checking if juno directory exists...
if not exist "%JUNO_HOME%\juno" (
    echo FAILED: juno directory not found in "%JUNO_HOME%".
    exit /b 1
) else (
    echo PASSED: juno directory exists.
)
echo.

REM Test 5: Try running juno2 --version
echo Test 5: Running juno2 --version...
call "%JUNO_HOME%\juno2.bat" --version >nul 2>nul
if %errorLevel% neq 0 (
    echo FAILED: Could not run juno2 --version.
    exit /b 1
) else (
    echo PASSED: juno2 --version ran successfully.
    for /f "tokens=*" %%i in ('call "%JUNO_HOME%\juno2.bat" --version 2^>^&1') do set JUNO_VERSION=%%i
    echo Juno version: !JUNO_VERSION!
)
echo.

REM Test 6: Check if Juno is in PATH
echo Test 6: Checking if Juno is in PATH...
where juno2 >nul 2>nul
if %errorLevel% neq 0 (
    echo WARNING: juno2 is not in PATH.
    echo You may want to run add_to_path.bat as administrator to add Juno to PATH.
) else (
    echo PASSED: juno2 is in PATH.
)
echo.

echo All tests completed.
echo If any tests failed, please fix the issues before using Juno.
echo If all tests passed, Juno is installed correctly.
echo.

pause