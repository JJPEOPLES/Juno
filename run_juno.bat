@echo off
REM Simple batch file to run Juno programs with minimal output

REM Get the directory of this batch file
set "JUNO_HOME=%~dp0"

REM Run the Python script
python "%JUNO_HOME%\run_juno.py" %*