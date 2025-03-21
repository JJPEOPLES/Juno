# Run Juno without installing it

# Get the directory of this script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Set PYTHONPATH to include the Juno directory
$env:PYTHONPATH = "$scriptDir;$env:PYTHONPATH"

# Run Juno with the provided arguments
python "$scriptDir\juno\__main__.py" $args

# If no arguments were provided, display a message
if ($args.Count -eq 0) {
    Write-Host ""
    Write-Host "Juno REPL has exited."
    Write-Host "To run a Juno file, use: .\run_juno.ps1 yourfile.juno"
    Write-Host ""
    Read-Host "Press Enter to continue"
}