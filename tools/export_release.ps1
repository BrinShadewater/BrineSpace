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

# The export presets point at two template executables under output/, which is
# also where cleanup passes look. Restore them from the verified bundle rather
# than failing the build (September 12, 2026 — a cleanup left only the .tpz).
$templateDir = Join-Path $releaseRoot 'output/production-ten/export-tools'
$templateNames = @('windows_debug_x86_64.exe', 'windows_release_x86_64.exe')
$missingTemplates = @($templateNames | Where-Object { -not (Test-Path -LiteralPath (Join-Path $templateDir $_)) })
if ($missingTemplates.Count -gt 0) {
    $bundle = Join-Path $templateDir 'Godot_v4.6.1-stable_export_templates.tpz'
    $sums = Join-Path $templateDir 'SHA512-SUMS.txt'
    if (-not (Test-Path -LiteralPath $bundle)) {
        throw "Export templates missing ($($missingTemplates -join ', ')) and no bundle at $bundle. Re-download the 4.6.1 export templates."
    }
    if (Test-Path -LiteralPath $sums) {
        $expected = (Select-String -LiteralPath $sums -Pattern ([regex]::Escape((Split-Path $bundle -Leaf))) |
            Select-Object -First 1).Line -replace '\s.*$', ''
        $actual = (Get-FileHash -Algorithm SHA512 -LiteralPath $bundle).Hash.ToLower()
        if ($expected -and $actual -ne $expected.ToLower()) {
            throw "Export template bundle failed its SHA-512 check. Expected $expected, got $actual."
        }
    }
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [IO.Compression.ZipFile]::OpenRead($bundle)
    try {
        foreach ($name in $missingTemplates) {
            $entry = $archive.Entries | Where-Object { $_.FullName -eq "templates/$name" }
            if (-not $entry) { throw "Bundle $bundle has no templates/$name." }
            [IO.Compression.ZipFileExtensions]::ExtractToFile($entry, (Join-Path $templateDir $name), $true)
            Write-Output "Restored export template from bundle: $name"
        }
    } finally { $archive.Dispose() }
}
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
