param([string]$Godot = 'C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe')
$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$evidence=Join-Path $repo ('output/ocean-floor-checks-'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $evidence | Out-Null
$previousAppData=$env:APPDATA
$previousLocalData=$env:LOCALAPPDATA
python (Join-Path $repo 'tools/fingerprint_marsh_profile.py') (Join-Path $evidence 'owner-before.json')
try {
    $env:APPDATA=Join-Path $evidence 'scratch-appdata'
    $env:LOCALAPPDATA=Join-Path $evidence 'scratch-localdata'
    New-Item -ItemType Directory -Path $env:APPDATA,$env:LOCALAPPDATA | Out-Null
    . (Join-Path $repo 'tools/wait_environment_process.ps1')
    foreach($fixture in @('review_ocean_floor_expansion','test_wreck_clearance','test_runtime_environment_art')) {
        $log=Join-Path $evidence ($fixture+'.log')
        $process=Start-Process -FilePath $Godot -ArgumentList @('--path',('"'+$repo+'"'),'--windowed','--resolution','1600x900','--script',('res://tests/'+$fixture+'.gd'),'--log-file',('"'+$log+'"')) -WindowStyle Hidden -PassThru
        Wait-EnvironmentProcess -Process $process -ExpectedExecutable $Godot -LogPath $log -TimeoutSeconds 240
        Get-Content -LiteralPath $log | Select-String -Pattern 'PASS|failures|checks|textures|REVIEW' | Select-Object -Last 3
    }
} finally {
    $env:APPDATA=$previousAppData
    $env:LOCALAPPDATA=$previousLocalData
    python (Join-Path $repo 'tools/fingerprint_marsh_profile.py') (Join-Path $evidence 'owner-after.json')
    python -c "import json; from pathlib import Path; p=Path(r'$evidence'); a=json.loads((p/'owner-before.json').read_text()); b=json.loads((p/'owner-after.json').read_text()); d=[k for k in set(a)|set(b) if a.get(k)!=b.get(k)]; (p/'owner-delta.json').write_text(json.dumps(d,indent=2)); print('Owner profile:',len(a),'files;',len(d),'changed paths')"
    Write-Output ('Evidence: '+$evidence)
}
