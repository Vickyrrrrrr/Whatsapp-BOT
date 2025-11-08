# PowerShell helper to run the app and tests
# Usage: .\run_test.ps1 -mode run|test
param(
    [string]$mode = 'run'
)

if ($mode -eq 'run') {
    Write-Host "Activating venv and running app..."
    if (Test-Path .venv) {
        . .\.venv\Scripts\Activate.ps1
    } else {
        Write-Host "No .venv found. Create one with: python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1"
    }
    python app.py
} elseif ($mode -eq 'test') {
    if (Test-Path .venv) { . .\.venv\Scripts\Activate.ps1 }
    python -m pytest -q
} else {
    Write-Host "Unknown mode: $mode. Use run or test."
}
