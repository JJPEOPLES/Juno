# Run Juno examples

# Get the directory of this script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Set PYTHONPATH to include the Juno directory
$env:PYTHONPATH = "$scriptDir;$env:PYTHONPATH"

Write-Host "Juno Programming Language Examples" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available examples:"
Write-Host "1. Hello World"
Write-Host "2. Fibonacci"
Write-Host "3. Java Interop"
Write-Host "4. AI Example"
Write-Host "5. React Example"
Write-Host "6. AI + React Example"
Write-Host ""

$choice = Read-Host "Enter the number of the example to run (1-6)"

switch ($choice) {
    "1" {
        Write-Host "Running Hello World example..." -ForegroundColor Green
        python "$scriptDir\juno\__main__.py" "$scriptDir\examples\hello.juno"
    }
    "2" {
        Write-Host "Running Fibonacci example..." -ForegroundColor Green
        python "$scriptDir\juno\__main__.py" "$scriptDir\examples\fibonacci.juno"
    }
    "3" {
        Write-Host "Running Java Interop example..." -ForegroundColor Green
        python "$scriptDir\juno\__main__.py" "$scriptDir\examples\java_interop.juno"
    }
    "4" {
        Write-Host "Running AI Example..." -ForegroundColor Green
        python "$scriptDir\juno\__main__.py" "$scriptDir\examples\ai_example.juno"
    }
    "5" {
        Write-Host "Running React Example..." -ForegroundColor Green
        python "$scriptDir\juno\__main__.py" "$scriptDir\examples\react_example.juno"
    }
    "6" {
        Write-Host "Running AI + React Example..." -ForegroundColor Green
        python "$scriptDir\juno\__main__.py" "$scriptDir\examples\ai_react_example.juno"
    }
    default {
        Write-Host "Invalid choice. Please enter a number between 1 and 6." -ForegroundColor Red
    }
}

Write-Host ""
Read-Host "Press Enter to continue"