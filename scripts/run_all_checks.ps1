$ErrorActionPreference = "Stop"

Write-Host "== CROPIC: Running end-to-end checks =="

$backendProcess = $null
$backendLog = "docs/execution/backend_start.log"
$backendErr = "docs/execution/backend_start.err.log"

function Test-BackendHealth {
    try {
        $health = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get -TimeoutSec 2
        return ($health.status -eq "ok")
    }
    catch {
        return $false
    }
}

function Start-BackendIfNeeded {
    if (Test-BackendHealth) {
        Write-Host "Backend already running."
        return
    }

    Write-Host "Starting backend..."
    Write-Host "Installing backend dependencies..."
    python -m pip install -r backend/requirements.txt | Out-Host

    New-Item -ItemType Directory -Force -Path "docs/execution" | Out-Null
    if (Test-Path $backendLog) {
        Remove-Item $backendLog -Force
    }
    if (Test-Path $backendErr) {
        Remove-Item $backendErr -Force
    }

    $script:backendProcess = Start-Process `
        -FilePath "python" `
        -ArgumentList @("-m", "uvicorn", "app.main:app", "--app-dir", "backend", "--host", "127.0.0.1", "--port", "8000") `
        -PassThru `
        -RedirectStandardOutput $backendLog `
        -RedirectStandardError $backendErr `
        -WindowStyle Hidden

    $maxTries = 30
    for ($i = 0; $i -lt $maxTries; $i++) {
        Start-Sleep -Milliseconds 500
        if (Test-BackendHealth) {
            Write-Host "Backend is healthy."
            return
        }
    }

    $logOut = if (Test-Path $backendLog) { Get-Content -Raw $backendLog } else { "No stdout log found." }
    $logErr = if (Test-Path $backendErr) { Get-Content -Raw $backendErr } else { "No stderr log found." }
    throw "Backend failed to start.`nSTDOUT:`n$logOut`nSTDERR:`n$logErr"
}

function Stop-BackendIfStarted {
    if ($null -ne $script:backendProcess -and -not $script:backendProcess.HasExited) {
        Write-Host "Stopping backend process..."
        Stop-Process -Id $script:backendProcess.Id -Force
    }
}

function Run-Step {
    param(
        [string]$Name,
        [scriptblock]$Command
    )
    Write-Host ("`n-- {0}" -f $Name)
    & $Command
    if ($null -ne $LASTEXITCODE -and $LASTEXITCODE -ne 0) {
        throw "Step failed: $Name (exit code $LASTEXITCODE)"
    }
}

try {
    Start-BackendIfNeeded

    Run-Step -Name "Backend health check" -Command {
        if (-not (Test-BackendHealth)) {
            throw "Backend health is not ok"
        }
        Write-Host "health: ok"
    }

    Run-Step -Name "Smoke backend flow" -Command {
        python scripts/smoke_backend_flow.py
    }

    Run-Step -Name "Build dataset manifest" -Command {
        python data/scripts/build_manifest.py
    }

    Run-Step -Name "Split dataset manifest" -Command {
        python data/scripts/split_manifest.py
    }

    Run-Step -Name "Train baseline classifier artifact" -Command {
        python ai-services/src/train_baseline_classifier.py
    }

    Run-Step -Name "Train baseline segmentation artifact" -Command {
        python ai-services/src/train_segmentation_baseline.py
    }

    Run-Step -Name "Concurrent load test" -Command {
        python scripts/load_test_backend.py
    }

    Run-Step -Name "Latency gate (<2s p95)" -Command {
        python scripts/latency_gate.py
    }

    Run-Step -Name "Seed demo metric data (if empty)" -Command {
        python scripts/generate_demo_metrics_data.py
    }

    Run-Step -Name "Evaluate success metrics" -Command {
        python scripts/evaluate_success_metrics.py
    }

    Run-Step -Name "Drift monitor" -Command {
        python scripts/drift_monitor.py
    }

    Run-Step -Name "Validate multilingual voice reports" -Command {
        python scripts/validate_multilingual_voice.py
    }

    Run-Step -Name "Demo reliability run" -Command {
        python scripts/demo_reliability.py
    }

    Run-Step -Name "TRL gate" -Command {
        python scripts/trl_gate.py
    }

    Write-Host "`n== All checks completed =="
}
finally {
    Stop-BackendIfStarted
}
