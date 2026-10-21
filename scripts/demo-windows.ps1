$ErrorActionPreference='Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$env:NETGUARD_APPROVAL_SECRET = 'REPLACE-WITH-A-STRONG-UNIQUE-LAB-SECRET-ONLY'
& .\.venv\Scripts\python.exe -m netguard.cli scan
& .\.venv\Scripts\python.exe -m netguard.cli plan --device CORE-SW1
Write-Host 'For a manual approval demonstration, run approve then simulate using the returned token.'
