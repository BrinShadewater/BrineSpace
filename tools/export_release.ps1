param(
    [string]$Godot = 'C:/Users/Alex/Desktop/Projects/Godot_v4.6.1-stable_win64.exe',
    [string]$ProjectRoot = (Split-Path $PSScriptRoot -Parent),
    [string]$OutputPath = 'builds/BrineSpace-reliability/BrineSpace.exe'
)
$ErrorActionPreference = 'Stop'
$releaseRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$releaseTarget = if ([IO.Path]::IsPathRooted($OutputPath)) { $OutputPath } else { Join-Path $releaseRoot $OutputPath }
New-Item -ItemType Directory -Force (Split-Path $releaseTarget -Parent) | Out-Null
New-Item -ItemType Directory -Force (Join-Path $releaseRoot 'output') | Out-Null
$releaseLog = Join-Path $releaseRoot 'output/release-export.log'
python (Join-Path $releaseRoot 'tools/build_release_manifest.py')
if ($LASTEXITCODE -ne 0) { throw 'Runtime dependency manifest failed.' }
python (Join-Path $releaseRoot 'tools/set_raw_png_import_keep.py')
if ($LASTEXITCODE -ne 0) { throw 'Raster import-role sync failed.' }
$releaseArgs = @('--headless','--path',('"'+$releaseRoot+'"'),'--export-release','"Windows Game"',('"'+$releaseTarget+'"'),'--log-file',('"'+$releaseLog+'"'))
$releaseProcess = Start-Process -FilePath $Godot -ArgumentList $releaseArgs -WindowStyle Hidden -PassThru -Wait
$releaseErrors = @(Select-String -LiteralPath $releaseLog -Pattern 'ERROR:|SCRIPT ERROR|Parse Error')
if ($releaseProcess.ExitCode -ne 0 -or $releaseErrors.Count -gt 0) {
    $releaseErrors | Select-Object -First 8
    throw "Export failed validation. Full log: $releaseLog"
}
Copy-Item -LiteralPath (Join-Path $releaseRoot 'build_info.json') -Destination (Join-Path (Split-Path $releaseTarget -Parent) 'build_info.json')
Write-Output "Release ready: $releaseTarget"
