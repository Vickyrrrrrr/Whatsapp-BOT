# ngrok Setup Helper
# Run this after getting your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken

Write-Host "=== University of Lucknow WhatsApp Bot - ngrok Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if ngrok is installed
if (-not (Get-Command ngrok -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: ngrok is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Download from: https://ngrok.com/download" -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 1: Get your ngrok authtoken" -ForegroundColor Green
Write-Host "  1. Go to: https://dashboard.ngrok.com/signup" -ForegroundColor Yellow
Write-Host "  2. After login, go to: https://dashboard.ngrok.com/get-started/your-authtoken" -ForegroundColor Yellow
Write-Host "  3. Copy your authtoken" -ForegroundColor Yellow
Write-Host ""

$token = Read-Host "Paste your ngrok authtoken here (or press Enter to skip)"

if ($token) {
    Write-Host "Adding authtoken to ngrok..." -ForegroundColor Green
    ngrok config add-authtoken $token
    Write-Host ""
}

Write-Host "Step 2: Starting ngrok tunnel on port 5000..." -ForegroundColor Green
Write-Host "Make sure your Flask app is running in another window!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop ngrok" -ForegroundColor Yellow
Write-Host ""

ngrok http 5000
