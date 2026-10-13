param([string]$Godot='C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe')
$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot -Parent
$evidence=Join-Path $repo ('output/seep-geology-checks-'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $evidence | Out-Null
$oldAppData=$env:APPDATA;$oldLocalData=$env:LOCALAPPDATA
python (Join-Path $repo 'tools/fingerprint_marsh_profile.py') (Join-Path $evidence 'owner-before.json')
try {
    $env:APPDATA=Join-Path $evidence 'scratch-appdata';$env:LOCALAPPDATA=Join-Path $evidence 'scratch-localdata'
    New-Item -ItemType Directory -Path $env:APPDATA,$env:LOCALAPPDATA | Out-Null
    . (Join-Path $repo 'tools/wait_environment_process.ps1')
    foreach($fixture in @('review_seep_geology','test_runtime_environment_art')) {
        $log=Join-Path $evidence ($fixture+'.log')
        $process=Start-Process -FilePath $Godot -ArgumentList @('--path',('"'+$repo+'"'),'--windowed','--resolution','1600x900','--script',('res://tests/'+$fixture+'.gd'),'--log-file',('"'+$log+'"'),'--',('--out="'+(Join-Path $evidence 'captures')+'"')) -WindowStyle Hidden -PassThru
        Wait-EnvironmentProcess -Process $process -ExpectedExecutable $Godot -LogPath $log -TimeoutSeconds 180
        Get-Content -LiteralPath $log | Select-String -Pattern 'PASS|failures|REVIEW|checks' | Select-Object -Last 2
    }
} finally {
    $env:APPDATA=$oldAppData;$env:LOCALAPPDATA=$oldLocalData
    python (Join-Path $repo 'tools/fingerprint_marsh_profile.py') (Join-Path $evidence 'owner-after.json')
    python -c "import json; from pathlib import Path; p=Path(r'$evidence'); a=json.loads((p/'owner-before.json').read_text()); b=json.loads((p/'owner-after.json').read_text()); d=[k for k in set(a)|set(b) if a.get(k)!=b.get(k)]; (p/'owner-delta.json').write_text(json.dumps(d)); print('Owner profile:',len(a),'files;',len(d),'changed')"
    Write-Output ('Evidence: '+$evidence)
}
