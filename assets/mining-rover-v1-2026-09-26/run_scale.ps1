$ErrorActionPreference='Stop'
$projectRoot=(Get-Location).Path
$reviewRoot=Join-Path $projectRoot 'assets/mining-rover-v1-2026-09-26/review'
$ownerRoot=Join-Path $env:APPDATA 'Godot/app_userdata/BrineSpace'
function Fingerprint { if(Test-Path -LiteralPath $ownerRoot){ Get-ChildItem -LiteralPath $ownerRoot -Recurse -File | Sort-Object FullName | ForEach-Object { [PSCustomObject]@{Path=$_.FullName.Substring($ownerRoot.Length);Hash=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash} } | ConvertTo-Json -Compress } }
$before=Fingerprint
$before | Set-Content (Join-Path $reviewRoot 'owner-before.json')
$priorAppData=$env:APPDATA
try {
 $env:APPDATA=Join-Path $projectRoot 'output/mining-rover-scale-isolated'
 New-Item -ItemType Directory -Force -Path $env:APPDATA | Out-Null
 & 'C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe' --path $projectRoot --script res://tools/capture_mining_rover_scale.gd *> (Join-Path $reviewRoot 'native-scale.log')
 $result=$LASTEXITCODE
} finally { $env:APPDATA=$priorAppData; $after=Fingerprint; $after | Set-Content (Join-Path $reviewRoot 'owner-after.json'); if($before -cne $after){throw 'Owner save fingerprint changed'} }
if($result -ne 0){throw "Scale fixture failed: $result"}
'Owner save fingerprints unchanged.' | Set-Content (Join-Path $reviewRoot 'save-check.txt')
Get-Content (Join-Path $reviewRoot 'native-scale.log') -Tail 5

