@echo off
REM Run Juno examples

REM Get the directory of this script
set SCRIPT_DIR=%~dp0

REM Set PYTHONPATH to include the Juno directory
set PYTHONPATH=%SCRIPT_DIR%;%PYTHONPATH%

echo Juno Programming Language Examples
echo ===================================================
echo.
echo Available examples:
echo 1. Hello World
echo 2. Fibonacci
echo 3. Java Interop
echo 4. AI Example
echo 5. React Example
echo 6. AI + React Example
echo.

set /p CHOICE=Enter the number of the example to run (1-6): 

if "%CHOICE%"=="1" (
    echo Running Hello World example...
    python "%SCRIPT_DIR%\juno\__main__.py" "%SCRIPT_DIR%\examples\hello.juno"
) else if "%CHOICE%"=="2" (
    echo Running Fibonacci example...
    python "%SCRIPT_DIR%\juno\__main__.py" "%SCRIPT_DIR%\examples\fibonacci.juno"
) else if "%CHOICE%"=="3" (
    echo Running Java Interop example...
    python "%SCRIPT_DIR%\juno\__main__.py" "%SCRIPT_DIR%\examples\java_interop.juno"
) else if "%CHOICE%"=="4" (
    echo Running AI Example...
    python "%SCRIPT_DIR%\juno\__main__.py" "%SCRIPT_DIR%\examples\ai_example.juno"
) else if "%CHOICE%"=="5" (
    echo Running React Example...
    python "%SCRIPT_DIR%\juno\__main__.py" "%SCRIPT_DIR%\examples\react_example.juno"
) else if "%CHOICE%"=="6" (
    echo Running AI + React Example...
    python "%SCRIPT_DIR%\juno\__main__.py" "%SCRIPT_DIR%\examples\ai_react_example.juno"
) else (
    echo Invalid choice. Please enter a number between 1 and 6.
)

echo.
pause