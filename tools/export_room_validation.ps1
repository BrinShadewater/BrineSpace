param(
    [Parameter(Mandatory=$true)][string]$Godot,
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [string]$Python = 'python',
    [string[]]$AdditionalManifest = @(),
    [switch]$ControlledTour,
    [switch]$CompositionReview,
    [switch]$ThreeCrewReview,
    [ValidateRange(60,300)][int]$RuntimeTimeoutSeconds = 60,
    [ValidateRange(60,300)][int]$ExportTimeoutSeconds = 60
)
$ErrorActionPreference = 'Stop'
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$destination = [IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $destination) { throw 'Use a new output directory; evidence is never overwritten.' }
if (-not (Test-Path -LiteralPath $Godot -PathType Leaf)) { throw 'Godot executable does not exist.' }
if ($CompositionReview -and -not $ControlledTour) { throw 'CompositionReview requires ControlledTour.' }
if ($ThreeCrewReview -and -not $ControlledTour) { throw 'ThreeCrewReview requires ControlledTour.' }
foreach ($manifest in $AdditionalManifest) {
    if (-not $manifest.StartsWith('res://')) { throw 'Additional manifests must use res:// project paths.' }
    $manifestPath = Join-Path $workspace $manifest.Substring(6)
    if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) { throw "Missing additional manifest: $manifest" }
    $entries = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json -NoEnumerate
    if ($entries -isnot [array] -or $entries.Count -eq 0) { throw "Additional manifest must contain a nonempty room array: $manifest" }
}
New-Item -ItemType Directory -Path $destination | Out-Null

function Invoke-CheckedProcess([string]$Executable, [string[]]$InvocationArgs, [string]$WorkingDirectory, [string]$Label) {
    $stdout = Join-Path $destination ($Label + '.log')
    $stderr = Join-Path $destination ($Label + '.err')
    $quoted = $InvocationArgs | ForEach-Object { '"' + $_ + '"' }
    $process = Start-Process -FilePath $Executable -ArgumentList $quoted -WorkingDirectory $WorkingDirectory -WindowStyle Hidden -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    $timeoutMs = if ($Label -eq 'runtime') { $RuntimeTimeoutSeconds * 1000 } else { $ExportTimeoutSeconds * 1000 }
    if (-not $process.WaitForExit($timeoutMs)) {
        Stop-Process -Id $process.Id
        throw "$Label timed out; its process was stopped. Inspect $stderr"
    }
    $process.Refresh()
    if ($process.ExitCode -ne 0) { throw "$Label exited $($process.ExitCode). Inspect $stderr" }
    $errors = Select-String -LiteralPath $stdout,$stderr -Pattern '^(SCRIPT ERROR:|ERROR:)'
    if ($errors) { throw "$Label logged errors despite its exit status. Inspect $stderr" }
}

Push-Location $workspace
try {
    $profileManifests = @('rooms/production-ten/manifest.json') + @($AdditionalManifest | ForEach-Object { $_.Substring(6) })
    & $Python (Join-Path $PSScriptRoot 'audit_composition_dependencies.py') @profileManifests
    if ($LASTEXITCODE -ne 0) { throw 'Composition dependency audit failed before export.' }
    & $Python (Join-Path $PSScriptRoot 'audit_room_floor_hooks.py')
    if ($LASTEXITCODE -ne 0) { throw 'Room floor dressing hook audit failed.' }
    & $Python (Join-Path $PSScriptRoot 'build_room_export_fixture.py')
    if ($LASTEXITCODE -ne 0) { throw 'Fixture generation failed.' }
    # Refresh newly added raw JSON/PNG dependencies before selected-resource export.
    # An old editor filesystem cache omitted the Life Support profile in v24.
    Invoke-CheckedProcess $Godot @('--headless','--editor','--path',$workspace,'--import') $workspace 'import'
    # Resolve furnishing hosts after native room initialization/rotation, not just
    # profile hashes: derived views may replace the parent's machinery identities.
    Invoke-CheckedProcess $Godot @('--headless','--path',$workspace,'--script','res://tools/audit_room_dressing_hosts.gd') $workspace 'dressing-hosts'
    $binary = Join-Path $destination 'BRINE.exe'
    Invoke-CheckedProcess $Godot @('--headless','--path',$workspace,'--export-debug','Windows Room Validation',$binary) $workspace 'export'
    if (-not (Test-Path -LiteralPath $binary)) { throw 'Export did not produce an executable.' }
    $external = Join-Path ([IO.Path]::GetTempPath()) ('brine-export-check-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $external | Out-Null
    $captures = Join-Path $destination 'captures'
    $runtimeArgs = @('--',"--capture-dir=$captures",'--viewport-width=1600')
    if ($ControlledTour) { $runtimeArgs += '--controlled-tour' }
    if ($CompositionReview) { $runtimeArgs += '--composition-review' }
    if ($ThreeCrewReview) { $runtimeArgs += '--three-crew-review' }
    foreach ($manifest in $AdditionalManifest) { $runtimeArgs += "--additional-manifest=$manifest" }
    Invoke-CheckedProcess $binary $runtimeArgs $external 'runtime' 
    $runtimeLog = Get-Content -LiteralPath (Join-Path $destination 'runtime.log') -Raw
    $movementMarker = if ($ControlledTour) { 'CONTROLLED ROOM TOUR:' } else { 'TEN ROOM MIXED STATION:' }
    foreach ($marker in @('TEN ROOM ASSETS:', $movementMarker, 'ROOM SCENE PASS [production_ten_station]')) {
        if (-not $runtimeLog.Contains($marker)) { throw "Missing runtime evidence: $marker" }
    }
    $summary = Get-Content -LiteralPath (Join-Path $captures 'station-summary.json') -Raw | ConvertFrom-Json
    $batch = Get-Content -LiteralPath (Join-Path $workspace 'rooms/production-ten/manifest.json') -Raw | ConvertFrom-Json
    $expectedCount = $batch.Count
    foreach ($manifest in $AdditionalManifest) {
        if (-not $manifest.StartsWith('res://')) { throw 'Additional manifests must use res:// project paths.' }
        $extra = @(Get-Content -LiteralPath (Join-Path $workspace $manifest.Substring(6)) -Raw | ConvertFrom-Json)
        $expectedCount += $extra.Count
    }
    $extraHab = if ($ThreeCrewReview) { 1 } else { 0 }
    if ($summary.rooms -ne ($expectedCount + [Math]::Ceiling($expectedCount / 2.0) + $extraHab) -or $summary.visited -ne $summary.rooms) { throw 'Incomplete mixed-station coverage.' }
    if ($ControlledTour -and ($summary.mode -ne 'controlled-tour' -or $summary.arrivals -ne $summary.rooms)) { throw 'Incomplete controlled arrivals.' }
    $crewEvidence = $null
    if ($ThreeCrewReview) {
        $crewEvidence = Get-Content -LiteralPath (Join-Path $captures 'controlled-tour-start.state.json') -Raw | ConvertFrom-Json
        foreach ($field in @('crew_active','crew_present')) {
            $flags = @($crewEvidence.$field)
            if ($flags.Count -ne 3 -or @($flags | Where-Object { $_ -isnot [bool] -or -not $_ }).Count -ne 0) { throw "Three-crew evidence missing: $field" }
        }
    }
    $compositionEvidence = $null
    if ($CompositionReview) {
        $compositionEvidence = Get-Content -LiteralPath (Join-Path $captures 'composition-review.json') -Raw | ConvertFrom-Json
        if ($compositionEvidence.rooms.Count -ne ($expectedCount + $extraHab)) { throw 'Incomplete focused room captures.' }
        foreach ($room in $compositionEvidence.rooms) {
            if ([Math]::Abs($room.zoom - 0.52) -gt 0.00001) { throw "Unexpected focused zoom: $($room.id)" }
            if (-not (Test-Path -LiteralPath (Join-Path $captures $room.capture) -PathType Leaf)) { throw "Missing focused capture: $($room.id)" }
        }
    }
    @{
        scope = if ($ControlledTour) { 'Windows debug controlled room traversal; not autonomous destination-choice or release acceptance' } else { 'Windows debug room validation; not publication or release acceptance' }
        executable_sha256 = (Get-FileHash -LiteralPath $binary -Algorithm SHA256).Hash
        pack_sha256 = (Get-FileHash -LiteralPath (Join-Path $destination 'BRINE.pck') -Algorithm SHA256).Hash
        external_working_directory = $external
        station = $summary
        composition_review = $compositionEvidence
        three_crew_start = $crewEvidence
    } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $destination 'verification.json') -Encoding UTF8
    Write-Output "Export and runtime checks passed: $destination"
} finally {
    Pop-Location
}
