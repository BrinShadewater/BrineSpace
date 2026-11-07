param([switch]$Verify, [switch]$Variations, [string]$Room = '')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$previewRoot = Join-Path $projectRoot 'output/riser-room-preview'
$scratchRoot = Join-Path $previewRoot ('session-' + [Guid]::NewGuid().ToString('N'))
$ownerRoot = Join-Path $env:APPDATA 'Godot/app_userdata/BrineSpace'
function Get-SaveFingerprint {
    if (Test-Path -LiteralPath $ownerRoot) {
        Get-ChildItem -LiteralPath $ownerRoot -File -Recurse | Sort-Object FullName | ForEach-Object {
            [PSCustomObject]@{ Path = $_.FullName.Substring($ownerRoot.Length); Hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
        } | ConvertTo-Json -Compress
    }
}
New-Item -ItemType Directory -Force -Path $scratchRoot | Out-Null
$before = Get-SaveFingerprint
$before | Set-Content -LiteralPath (Join-Path $scratchRoot 'owner-before.json')
$scratchUser = Join-Path $scratchRoot 'roaming/Godot/app_userdata/BrineSpace'
New-Item -ItemType Directory -Force -Path $scratchUser | Out-Null
$ownerLayouts = Join-Path $ownerRoot 'room_layouts.json'
if (Test-Path -LiteralPath $ownerLayouts) { Copy-Item -LiteralPath $ownerLayouts -Destination (Join-Path $scratchUser 'room_layouts.json') }
$priorAppData = $env:APPDATA
$priorLocal = $env:LOCALAPPDATA
$priorMarker = $env:BRINE_RISER_PREVIEW
try {
    $env:APPDATA = Join-Path $scratchRoot 'roaming'
    $env:LOCALAPPDATA = Join-Path $scratchRoot 'local'
    $env:BRINE_RISER_PREVIEW = 'isolated'
    New-Item -ItemType Directory -Force -Path $env:LOCALAPPDATA | Out-Null
    $scriptPath = if ($Variations) { 'res://tools/preview_riser_variations.gd' } else { 'res://tools/preview_riser_room.gd' }
    $arguments = @('--path',('"' + $projectRoot + '"'),'--script',$scriptPath)
    if ($Verify -or $Room) { $arguments += '--' }
    if ($Verify) { $arguments += '--verify' }
    if ($Room) { $arguments += ('--room=' + $Room) }
    $process = Start-Process -FilePath 'C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe' -ArgumentList $arguments -WorkingDirectory $projectRoot -PassThru -RedirectStandardOutput (Join-Path $scratchRoot 'stdout.log') -RedirectStandardError (Join-Path $scratchRoot 'stderr.log')
    $process.Id | Set-Content -LiteralPath (Join-Path $scratchRoot 'pid.txt')
    $scratchRoot | Set-Content -LiteralPath (Join-Path $previewRoot 'latest-session.txt')
    $process.WaitForExit()
    $after = Get-SaveFingerprint
    $after | Set-Content -LiteralPath (Join-Path $scratchRoot 'owner-after.json')
    if ($before -cne $after) { throw 'Owner save folder changed during preview; inspect before/after fingerprints.' }
    'Owner save fingerprint unchanged.' | Set-Content -LiteralPath (Join-Path $scratchRoot 'save-check.txt')
    Write-Output "Preview exited. Owner save fingerprint unchanged. Logs: $scratchRoot"
    if ($process.ExitCode -ne 0) { throw "Preview exited with code $($process.ExitCode)" }
    $errors = Get-Content -LiteralPath (Join-Path $scratchRoot 'stderr.log') -Raw
    if ($errors -match 'SCRIPT ERROR|ERROR:|Parse Error') { throw "Preview logged errors. See $scratchRoot/stderr.log" }
    if ($Verify) {
        $result = Get-Content -LiteralPath (Join-Path $scratchRoot 'stdout.log') -Raw
        if ($result -notmatch 'RISER PREVIEW PASS:') { throw 'Preview did not finish its verification.' }
    }
} finally {
    $env:APPDATA = $priorAppData
    $env:LOCALAPPDATA = $priorLocal
    $env:BRINE_RISER_PREVIEW = $priorMarker
}
