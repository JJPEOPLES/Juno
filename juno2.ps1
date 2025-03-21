# Juno2 - PowerShell launcher for Juno Programming Language
# Usage: .\juno2.ps1 [filename.juno]

# Get the directory of this script
$JUNO_HOME = Split-Path -Parent $MyInvocation.MyCommand.Path

# Set PYTHONPATH to include the Juno directory
$env:PYTHONPATH = "$JUNO_HOME;$env:PYTHONPATH"

# Change to the directory of the input file if provided
if ($args.Count -gt 0) {
    $filePath = $args[0]
    if (Test-Path $filePath) {
        $FILE_DIR = Split-Path -Parent $filePath
        Set-Location $FILE_DIR
    }
}

# Run Juno with the provided arguments
python "$JUNO_HOME\__main__.py" $args

# If no arguments were provided and not in interactive mode, show usage
if ($args.Count -eq 0) {
    Write-Host ""
    Write-Host "Juno REPL has exited."
    Write-Host "To run a Juno file, use: .\juno2.ps1 yourfile.juno"
    Write-Host ""
}