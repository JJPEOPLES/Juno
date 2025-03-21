# Juno Programming Language Setup for Windows (PowerShell)
# This script sets up the Juno programming language without installation

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Juno Programming Language Setup" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

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

Write-Host "Python requirements satisfied. Setting up Juno..." -ForegroundColor Green
Write-Host ""

# Get the directory of this script
$junoHome = Split-Path -Parent $MyInvocation.MyCommand.Path

# Create Juno directory in user's home
$junoDir = Join-Path $env:USERPROFILE ".juno"
$packagesDir = Join-Path $junoDir "packages"
New-Item -ItemType Directory -Path $junoDir -Force | Out-Null
New-Item -ItemType Directory -Path $packagesDir -Force | Out-Null

# Create a simple configuration file
Write-Host "Creating configuration file..." -ForegroundColor Cyan
$configPath = Join-Path $junoDir "config.json"
$configContent = @"
{
    "version": "0.1.0",
    "registry_url": "https://juno-lang.org/registry",
    "packages_dir": "$($packagesDir.Replace('\', '\\'))",
    "juno_home": "$($junoHome.Replace('\', '\\'))"
}
"@
Set-Content -Path $configPath -Value $configContent

# Create a PowerShell script to run Juno
Write-Host "Creating juno.ps1..." -ForegroundColor Cyan
$junoScriptPath = Join-Path $junoDir "juno.ps1"
$junoScriptContent = @"
# Run Juno
`$env:JUNO_HOME = "$junoHome"
`$env:PYTHONPATH = "`$env:JUNO_HOME;`$env:PYTHONPATH"
python "`$env:JUNO_HOME\juno\__main__.py" `$args
"@
Set-Content -Path $junoScriptPath -Value $junoScriptContent

# Create a batch file to run Juno (for compatibility)
Write-Host "Creating juno.bat..." -ForegroundColor Cyan
$junoBatPath = Join-Path $junoDir "juno.bat"
$junoBatContent = @"
@echo off
set JUNO_HOME=$junoHome
set PYTHONPATH=%JUNO_HOME%;%PYTHONPATH%
python "%JUNO_HOME%\juno\__main__.py" %*
"@
Set-Content -Path $junoBatPath -Value $junoBatContent

# Add Juno to PATH (optional)
$addToPath = Read-Host "Do you want to add Juno to your PATH? (y/n) [default: n]"
if ($addToPath -eq "y" -or $addToPath -eq "Y") {
    Write-Host "Adding Juno to PATH..." -ForegroundColor Cyan
    
    # Add to PATH
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if (-not $currentPath.Contains($junoDir)) {
        [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$junoDir", "User")
        Write-Host "Juno added to PATH." -ForegroundColor Green
    } else {
        Write-Host "Juno is already in PATH." -ForegroundColor Green
    }
}

# Create desktop shortcut (optional)
$createShortcut = Read-Host "Do you want to create a desktop shortcut for Juno REPL? (y/n) [default: n]"
if ($createShortcut -eq "y" -or $createShortcut -eq "Y") {
    Write-Host "Creating desktop shortcut..." -ForegroundColor Cyan
    
    # Create shortcut
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Juno REPL.lnk")
    $Shortcut.TargetPath = $junoBatPath
    $Shortcut.Save()
    
    Write-Host "Desktop shortcut created." -ForegroundColor Green
}

# Setup complete
Write-Host ""
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Juno has been successfully set up!" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now run Juno programs with:" -ForegroundColor White
Write-Host "  $junoBatPath yourfile.juno" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or start the interactive REPL with:" -ForegroundColor White
Write-Host "  $junoBatPath" -ForegroundColor Yellow
Write-Host ""

if ($addToPath -eq "y" -or $addToPath -eq "Y") {
    Write-Host "Since you added Juno to PATH, you can also use:" -ForegroundColor White
    Write-Host "  juno yourfile.juno" -ForegroundColor Yellow
    Write-Host "  juno" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "For quick access, you can also use the run_juno.ps1 script:" -ForegroundColor White
Write-Host "  .\run_juno.ps1 yourfile.juno" -ForegroundColor Yellow
Write-Host "  .\run_juno.ps1" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to exit"