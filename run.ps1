# Run Expense Tracker — no Docker, no Swagger needed
# Just open http://localhost:8000 in your browser

Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    Write-Host "Setting up (first time only)..."
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
}

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

Write-Host "Checking dependencies..."
& $python -m pip install -r requirements-dev.txt --disable-pip-version-check --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

function Test-PortInUse([int]$Port) {
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return $null -ne $conn
}

$port = 8000
if (Test-PortInUse $port) {
    Write-Host ""
    Write-Host "  Port $port is already in use (old server still running)." -ForegroundColor Yellow
    $pids = (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue).OwningProcess | Select-Object -Unique
    foreach ($procId in $pids) {
        $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
        if ($proc -and $proc.ProcessName -eq "python") {
            Write-Host "  Stopping old server (PID $procId)..."
            Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
        }
    }
    Start-Sleep -Seconds 2
    if (Test-PortInUse $port) {
        $port = 8001
        Write-Host "  Port 8000 still busy. Using port $port instead." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "  Expense Tracker is starting..."
Write-Host ""
Write-Host "  Open in your browser:  http://localhost:$port"
Write-Host ""
Write-Host "  Press Ctrl+C to stop"
Write-Host ""

Start-Process "http://localhost:$port"
& $python -m uvicorn app.main:app --reload --host 0.0.0.0 --port $port
