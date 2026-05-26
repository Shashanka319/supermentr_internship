<#
.\run_app.ps1

Launches the Streamlit auth app in a new PowerShell window, binds to localhost (127.0.0.1:8501),
and opens the browser. If a virtual environment exists at ./.venv, it will be activated.

Usage:
  - Double-click this file in Explorer, or
  - From PowerShell in project root: .\run_app.ps1
  - In VS Code: Run the task "Run Streamlit Auth App" (see .vscode/tasks.json)
#>

param(
    [int]$Port = 8501
)

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$venvActivate = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"

if (Test-Path $venvActivate) {
    $activateCmd = "& `"$venvActivate`""
} else {
    $activateCmd = ""
}

$streamlitCmd = "streamlit run streamlit_app_auth.py --server.address 127.0.0.1 --server.port $Port"

$fullCmd = if ($activateCmd -ne "") { "$activateCmd; $streamlitCmd" } else { $streamlitCmd }

Write-Output "Launching Streamlit with command:`n$fullCmd"

# Start Streamlit in a new PowerShell window so this script can return immediately
Start-Process powershell -ArgumentList @('-NoExit', '-Command', $fullCmd)

# Wait a short moment for server to start, then open browser
Start-Sleep -Seconds 2
$localUrl = "http://127.0.0.1:$Port"
try {
    Start-Process $localUrl
    Write-Output "Opened browser to $localUrl"
} catch {
    Write-Output "Could not open browser automatically. Open $localUrl manually once Streamlit starts."
}