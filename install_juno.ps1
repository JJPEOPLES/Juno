# Juno Programming Language Installer for Windows (PowerShell)
# This script installs the Juno programming language

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Juno Programming Language Installer" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "This installer requires administrator privileges." -ForegroundColor Yellow
    Write-Host "Please right-click on this file and select 'Run with PowerShell as administrator'." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        Write-Host "Found Python $major.$minor.$($Matches[3])"
        
        # Check if Python version is at least 3.7
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 7)) {
            Write-Host "Python 3.7 or higher is required." -ForegroundColor Red
            Write-Host "Please install a newer version of Python." -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
} catch {
    Write-Host "Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.7 or higher from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is installed
try {
    $pipVersion = pip --version 2>&1
    Write-Host "Found pip: $pipVersion"
} catch {
    Write-Host "pip is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please make sure pip is installed with Python." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Python requirements satisfied. Installing Juno..." -ForegroundColor Green
Write-Host ""

# Create a virtual environment (optional)
$installVenv = Read-Host "Do you want to install Juno in a virtual environment? (y/n) [default: n]"
if ($installVenv -eq "y" -or $installVenv -eq "Y") {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv juno_venv
    
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & .\juno_venv\Scripts\Activate.ps1
    
    Write-Host "Virtual environment activated." -ForegroundColor Green
}

# Install Juno
Write-Host "Installing Juno..." -ForegroundColor Cyan
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $scriptPath

# Install from source only
Write-Host "Installing from source..." -ForegroundColor Cyan
pip install -e .

# Check if installation was successful
try {
    $junoVersion = juno --version 2>&1
    Write-Host "Juno installed successfully: $junoVersion" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "Installation failed. Please check the error messages above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create Juno directory in user's home
$junoDir = Join-Path $env:USERPROFILE ".juno"
$packagesDir = Join-Path $junoDir "packages"
New-Item -ItemType Directory -Path $packagesDir -Force | Out-Null

# Create a simple configuration file
Write-Host "Creating configuration file..." -ForegroundColor Cyan
$configPath = Join-Path $junoDir "config.json"
$configContent = @"
{
    "version": "0.1.0",
    "registry_url": "https://juno-lang.org/registry",
    "packages_dir": "$($packagesDir.Replace('\', '\\'))"
}
"@
Set-Content -Path $configPath -Value $configContent

# Add Juno to PATH (optional)
$addToPath = Read-Host "Do you want to add Juno to your PATH? (y/n) [default: n]"
if ($addToPath -eq "y" -or $addToPath -eq "Y") {
    Write-Host "Adding Juno to PATH..." -ForegroundColor Cyan
    
    # Get the Scripts directory where juno.exe is located
    $junoExe = (Get-Command juno).Source
    $scriptsDir = Split-Path -Parent $junoExe
    
    # Add to PATH
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
    if (-not $currentPath.Contains($scriptsDir)) {
        [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$scriptsDir", "Machine")
        Write-Host "Juno added to PATH." -ForegroundColor Green
    } else {
        Write-Host "Juno is already in PATH." -ForegroundColor Green
    }
}

# Create desktop shortcut (optional)
$createShortcut = Read-Host "Do you want to create a desktop shortcut for Juno REPL? (y/n) [default: n]"
if ($createShortcut -eq "y" -or $createShortcut -eq "Y") {
    Write-Host "Creating desktop shortcut..." -ForegroundColor Cyan
    
    # Get the path to juno.exe
    $junoExe = (Get-Command juno).Source
    
    # Create shortcut
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Juno REPL.lnk")
    $Shortcut.TargetPath = $junoExe
    $Shortcut.Save()
    
    Write-Host "Desktop shortcut created." -ForegroundColor Green
}

# Installation complete
Write-Host ""
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Juno has been successfully installed!" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now run Juno programs with:" -ForegroundColor White
Write-Host "  juno yourfile.juno" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or start the interactive REPL with:" -ForegroundColor White
Write-Host "  juno" -ForegroundColor Yellow
Write-Host ""
Write-Host "For more information, run:" -ForegroundColor White
Write-Host "  juno --help" -ForegroundColor Yellow
Write-Host ""

if ($installVenv -eq "y" -or $installVenv -eq "Y") {
    Write-Host "Note: Juno is installed in a virtual environment." -ForegroundColor Yellow
    Write-Host "To use Juno, you need to activate the environment first:" -ForegroundColor Yellow
    Write-Host "  .\juno_venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host ""
}

Read-Host "Press Enter to exit"