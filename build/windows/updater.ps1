# updater.ps1
$owner = "BakiAbaad"
$repo = "wasel-agent"

try {
    $rel = Invoke-RestMethod -Uri "https://api.github.com/repos/$owner/$repo/releases/latest" -UseBasicParsing
} catch {
    Write-Error "Failed to fetch latest release."
    exit 1
}

$asset = $rel.assets | Where-Object { $_.name -match "setup|wasel-agent.*\.exe" } | Select-Object -First 1
if ($null -eq $asset) {
    Write-Host "No installer asset found in latest release."
    exit 0
}

$tmp = "$env:TEMP\wasel-agent-setup.exe"
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $tmp -UseBasicParsing
Start-Process -FilePath $tmp -ArgumentList "/VERYSILENT /NORESTART" -Wait

$nssm = "C:\Program Files\WaselAgent\nssm.exe"
if (-Not (Test-Path $nssm)) {
    $nssm = "$env:PROGRAMFILES\WaselAgent\nssm.exe"
}

if (Test-Path $nssm) {
    & $nssm restart wasel-agent
} else {
    Write-Host "nssm not found. Please restart wasel-agent manually."
}
