@echo off
REM Juno Version Command
REM This script displays the version information for Juno

REM Get the directory of this script
set "JUNO_HOME=%~dp0"
set "JUNO_HOME=%JUNO_HOME:~0,-1%"

REM Run Juno with the version flag
call "%JUNO_HOME%\juno2.bat" --version