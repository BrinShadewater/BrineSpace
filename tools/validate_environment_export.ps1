param(
    [Parameter(Mandatory=$true)][string]$GodotExecutable,
    [Parameter(Mandatory=$true)][ValidatePattern('^environment-export-[a-zA-Z0-9_-]+$')][string]$OutputName
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'wait_environment_process.ps1')
$projectRoot = Split-Path -Parent $PSScriptRoot
$buildDirectory = Join-Path $projectRoot ('output/' + $OutputName)
if (Test-Path -LiteralPath $buildDirectory) { throw 'Use a new output name to preserve prior evidence' }
$enginePath = (Resolve-Path -LiteralPath $GodotExecutable).Path
New-Item -ItemType Directory -Path $buildDirectory | Out-Null
Push-Location $projectRoot
try {
    python tools/build_environment_export_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'Source contract failed; export stopped' }
    Copy-Item -LiteralPath assets/environment/export-contract.json -Destination (Join-Path $buildDirectory 'source-contract.json')
    $exportLog = Join-Path $buildDirectory 'export.log'
    $outputExe = Join-Path $buildDirectory 'BRINE.exe'
    $exportArgs = '--headless --path "' + $projectRoot + '" --export-debug "Windows Environment Validation" "' + $outputExe + '" --log-file "' + $exportLog + '"'
    $exportProcess = Start-Process -FilePath $enginePath -ArgumentList $exportArgs -WindowStyle Hidden -PassThru
    Write-Output "Editor export process: $($exportProcess.Id)"
    Wait-EnvironmentProcess -Process $exportProcess -ExpectedExecutable $enginePath -LogPath $exportLog
    if ($exportProcess.ExitCode -ne 0 -or (Select-String -LiteralPath $exportLog -Pattern 'SCRIPT ERROR:|ERROR:')) {
        throw 'Editor export failed; inspect export.log'
    }
    $isolatedDirectory = Join-Path $env:TEMP ('BRINE-environment-validation-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $isolatedDirectory | Out-Null
    Copy-Item -LiteralPath $outputExe,(Join-Path $buildDirectory 'BRINE.pck') -Destination $isolatedDirectory
    $isolatedExe = Join-Path $isolatedDirectory 'BRINE.exe'
    $captureDirectory = Join-Path $buildDirectory 'captures'
    $runLog = Join-Path $buildDirectory 'isolated-run.log'
    $evidence = [ordered]@{
        isolated_directory=$isolatedDirectory
        executable_sha256=(Get-FileHash -LiteralPath $isolatedExe).Hash
        pack_sha256=(Get-FileHash -LiteralPath (Join-Path $isolatedDirectory 'BRINE.pck')).Hash
        capture_directory=$captureDirectory
    }
    [System.IO.File]::WriteAllText((Join-Path $buildDirectory 'execution.json'), ($evidence | ConvertTo-Json), [System.Text.UTF8Encoding]::new($false))
    $runArgs = '--log-file "' + $runLog + '" -- --capture-dir="' + $captureDirectory + '"'
    $runProcess = Start-Process -FilePath $isolatedExe -WorkingDirectory $isolatedDirectory -ArgumentList $runArgs -WindowStyle Hidden -PassThru
    Write-Output "Isolated export process: $($runProcess.Id)"
    Wait-EnvironmentProcess -Process $runProcess -ExpectedExecutable $isolatedExe -LogPath $runLog
    if ($runProcess.ExitCode -ne 0 -or (Select-String -LiteralPath $runLog -Pattern 'SCRIPT ERROR:|ERROR:')) {
        throw 'Isolated export failed; inspect isolated-run.log'
    }
    if (-not (Select-String -LiteralPath $runLog -SimpleMatch 'ENVIRONMENT EXPORT PASS:')) {
        throw 'Executable did not complete the environment fixture'
    }
    $result = Get-Content -LiteralPath (Join-Path $captureDirectory 'result.json') -Raw | ConvertFrom-Json
    $contract = Get-Content -LiteralPath (Join-Path $buildDirectory 'source-contract.json') -Raw | ConvertFrom-Json
    if ($result.png_count -ne $contract.png_count) { throw 'Packaged contract count differs from source evidence' }
    Write-Output "ENVIRONMENT VALIDATION COMPLETE: $($result.png_count) source PNGs; $buildDirectory"
} finally {
    Pop-Location
}
