param([string]$Script='res://character/brine-slim-v14-2026-10-03/production_preview.gd', [switch]$CheckOnly, [string[]]$UserArgs=@(), [string]$Expected='BRINE FLOAT: 200 native frames', [string]$Checkpoint='')
$ErrorActionPreference='Stop'
$projectRoot=(Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$scratchRoot=Join-Path $projectRoot ('output/brine-slim-v14/session-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $scratchRoot | Out-Null
$ownerRoot=Join-Path $env:APPDATA 'Godot/app_userdata/BrineSpace'
function Save-Fingerprint([string]$destination) {
    $record=@{}
    Get-ChildItem -LiteralPath $ownerRoot -File -Recurse | Where-Object { $_.FullName -notmatch '[\\/]logs[\\/]' } | ForEach-Object {
        $record[$_.FullName.Substring($ownerRoot.Length)]=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
    }
    $record | ConvertTo-Json | Set-Content -LiteralPath $destination
    return $record
}
$before=Save-Fingerprint (Join-Path $scratchRoot 'owner-before.json')
$scratchUser=Join-Path $scratchRoot 'roaming/Godot/app_userdata/BrineSpace'
New-Item -ItemType Directory -Force -Path $scratchUser | Out-Null
$layouts=Join-Path $ownerRoot 'room_layouts.json'
if(Test-Path -LiteralPath $layouts){Copy-Item -LiteralPath $layouts -Destination (Join-Path $scratchUser 'room_layouts.json')}
if($Checkpoint){Copy-Item -LiteralPath $Checkpoint -Destination (Join-Path $scratchUser 'brine_v12_continue.loop')}
$priorAppData=$env:APPDATA
$priorLocal=$env:LOCALAPPDATA
$priorMarker=$env:BRINE_RISER_PREVIEW
try {
    $env:APPDATA=Join-Path $scratchRoot 'roaming'
    $env:LOCALAPPDATA=Join-Path $scratchRoot 'local'
    $env:BRINE_RISER_PREVIEW='isolated'
    New-Item -ItemType Directory -Force -Path $env:LOCALAPPDATA | Out-Null
    $arguments=@('--path',('"'+$projectRoot+'"'),'--script',$Script)
    if($CheckOnly){$arguments+=@('--headless','--check-only')}else{$arguments+=@('--')+$UserArgs}
    $process=Start-Process -FilePath 'C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe' -ArgumentList $arguments -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $scratchRoot 'stdout.log') -RedirectStandardError (Join-Path $scratchRoot 'stderr.log')
    if(-not $process.WaitForExit(60000)){Stop-Process -Id $process.Id;throw 'Candidate preview exceeded 60 seconds.'}
    $process.Refresh()
    $exitCode=$process.ExitCode
} finally {
    $env:APPDATA=$priorAppData
    $env:LOCALAPPDATA=$priorLocal
    $env:BRINE_RISER_PREVIEW=$priorMarker
    $after=Save-Fingerprint (Join-Path $scratchRoot 'owner-after.json')
    $changes=@(($before.Keys+$after.Keys | Sort-Object -Unique) | Where-Object {$before[$_] -ne $after[$_]})
    @{unchanged=($changes.Count -eq 0);files=$before.Count;changes=$changes;exit_code=$exitCode} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $scratchRoot 'guard.json')
    $scratchRoot | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'latest-session.txt')
    Write-Output ('Owner profile unchanged: '+($changes.Count -eq 0)+'; files: '+$before.Count+'; changes: '+($changes -join ', '))
    Write-Output ('Evidence: '+$scratchRoot)
}
$errors=Get-Content -LiteralPath (Join-Path $scratchRoot 'stderr.log') -Raw
$results=Get-Content -LiteralPath (Join-Path $scratchRoot 'stdout.log') -Raw
if($errors -match 'SCRIPT ERROR|ERROR:|Parse Error'){throw 'Preview errors: see saved stderr.log.'}
if($exitCode -ne 0 -or (-not $CheckOnly -and $results -notmatch $Expected)){throw 'Verification did not complete.'}
Write-Output ('Verification passed: '+$Script)
