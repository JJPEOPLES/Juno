# Add juno2 to PATH - Run as administrator

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Add Juno2 to PATH" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "This script requires administrator privileges." -ForegroundColor Yellow
    Write-Host "Please right-click on this file and select 'Run with PowerShell as administrator'." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Get the directory of this script
$junoHome = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if juno2.ps1 exists
if (-not (Test-Path "$junoHome\juno2.ps1")) {
    Write-Host "Error: juno2.ps1 not found in $junoHome" -ForegroundColor Red
    Write-Host "Please run this script from the Juno directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Add to system PATH
Write-Host "Adding $junoHome to PATH..." -ForegroundColor Cyan

try {
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
    
    # Check if already in PATH
    if ($currentPath -like "*$junoHome*") {
        Write-Host "Juno2 is already in your PATH." -ForegroundColor Green
    } else {
        [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$junoHome", "Machine")
        Write-Host "Juno2 has been successfully added to PATH!" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "You can now run 'juno2' from any directory." -ForegroundColor White
    Write-Host ""
    Write-Host "Note: You may need to restart your PowerShell or command prompt" -ForegroundColor Yellow
    Write-Host "for the changes to take effect." -ForegroundColor Yellow
    Write-Host ""
} catch {
    Write-Host "Failed to add to PATH. Please check your permissions." -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
}

Read-Host "Press Enter to exit"