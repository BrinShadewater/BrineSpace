param(
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [int]$ViewportWidth = 1600,
    [ValidateRange(60,180)][int]$RuntimeTimeoutSeconds = 60,
    [switch]$ExerciseInputIsolation,
    [ValidateSet('cryo_chamber','clone_lab','data_archive','biodome','xeno_lab','anomaly_lab','bio_lab','holographic_core','med_center','med_office','med_bay','reactor','mining_drone_bay','salvage_drone_bay')]
    [string[]]$RoomIds = @('cryo_chamber','clone_lab','data_archive','biodome','xeno_lab','anomaly_lab','bio_lab','holographic_core','med_center','med_office')
)
$ErrorActionPreference = 'Stop'
$binary = [IO.Path]::GetFullPath($Executable)
$destination = [IO.Path]::GetFullPath($OutputDirectory)
if (-not (Test-Path -LiteralPath $binary -PathType Leaf)) { throw 'Missing validation executable.' }
if (Test-Path -LiteralPath $destination) { throw 'Use a new evidence directory.' }
if ($ViewportWidth -notin @(1280,1600,2560)) { throw 'Use a supported validation viewport.' }
if ($RoomIds.Count -eq 0 -or @($RoomIds | Select-Object -Unique).Count -ne $RoomIds.Count) { throw 'Room selection must be nonempty and unique.' }
New-Item -ItemType Directory -Path $destination | Out-Null
$external = Join-Path ([IO.Path]::GetTempPath()) ('brine-room-states-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $external | Out-Null
$subjects = $RoomIds
$records = @()
foreach ($subject in $subjects) {
    $stdout = Join-Path $destination ($subject + '.log')
    $stderr = Join-Path $destination ($subject + '.err')
    $captures = Join-Path $destination $subject
    $runtimeArgs = @('--',"--room-fixture=$subject","--capture-dir=$captures","--viewport-width=$ViewportWidth")
    if ($subject -eq 'reactor') { $runtimeArgs += '--reactor' }
    if ($ExerciseInputIsolation) { $runtimeArgs += '--exercise-input-isolation' }
    $arguments = $runtimeArgs | ForEach-Object { '"' + $_ + '"' }
    $process = Start-Process -FilePath $binary -ArgumentList $arguments -WorkingDirectory $external -WindowStyle Hidden -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    if (-not $process.WaitForExit($RuntimeTimeoutSeconds * 1000)) {
        Stop-Process -Id $process.Id
        throw "Exported $subject exceeded $RuntimeTimeoutSeconds seconds; only this runner's process was stopped."
    }
    $process.Refresh()
    if ($process.ExitCode -ne 0) { throw "$subject exited $($process.ExitCode)." }
    if (Select-String -LiteralPath $stdout,$stderr -Pattern 'ERROR:|SCRIPT ERROR:') { throw "$subject reported engine errors." }
    $log = Get-Content -LiteralPath $stdout -Raw
    if (-not $log.Contains("ROOM SCENE PASS [$subject]")) { throw "Missing subject-specific result for $subject." }
    if ($ExerciseInputIsolation -and -not $log.Contains('ART INPUT ISOLATION:')) { throw "Missing input-isolation exercise for $subject." }
    foreach ($quarter in 0..3) {
        $rotationFile = if ($subject -eq 'reactor') { "nursery-life-q$quarter.png" } elseif ($subject -eq 'med_bay') { "med-q$quarter-connected.png" } else { "room-q$quarter.png" }
        if (-not (Test-Path -LiteralPath (Join-Path $captures $rotationFile))) { throw "Missing $subject rotation $quarter capture." }
    }
    $states = @(Get-ChildItem -LiteralPath $captures -Filter '*.state.json' -File)
    if ($states.Count -eq 0) { throw "Missing full-frame state records for $subject; rebuild the fixture." }
    foreach ($stateFile in $states) {
        $state = Get-Content -LiteralPath $stateFile.FullName -Raw | ConvertFrom-Json
        $png = Join-Path $captures ($stateFile.Name -replace '\.state\.json$', '.png')
        $stream = [IO.File]::OpenRead($png)
        try {
            $header = New-Object byte[] 24
            if ($stream.Read($header,0,24) -ne 24) { throw "Truncated capture: $png" }
        } finally { $stream.Dispose() }
        if ([BitConverter]::ToString($header[0..7]) -ne '89-50-4E-47-0D-0A-1A-0A' -or [Text.Encoding]::ASCII.GetString($header,12,4) -ne 'IHDR') { throw "Invalid PNG header: $png" }
        $actualWidth = [uint32]$header[16]*16777216 + [uint32]$header[17]*65536 + [uint32]$header[18]*256 + $header[19]
        $actualHeight = [uint32]$header[20]*16777216 + [uint32]$header[21]*65536 + [uint32]$header[22]*256 + $header[23]
        $expectedHeight = [int]($ViewportWidth * 9 / 16)
        if ($actualWidth -ne $ViewportWidth -or $actualHeight -ne $expectedHeight -or $state.viewport_width -ne $actualWidth -or $state.viewport_height -ne $actualHeight) { throw "Actual capture dimensions do not match requested viewport: $png ($actualWidth x $actualHeight)" }
    }
    $records += @{ id=$subject; exit_code=$process.ExitCode; log_sha256=(Get-FileHash -LiteralPath $stdout -Algorithm SHA256).Hash; captures=$captures; dimension_checked_frames=$states.Count }
    Write-Output "EXPORTED ROOM PASS: $subject at $ViewportWidth"
}
@{
    scope='Individual exported room fixture assertions; pixel review separate; legacy route helpers do not certify autonomous NPC behavior'
    executable_sha256=(Get-FileHash -LiteralPath $binary -Algorithm SHA256).Hash
    pack_sha256=(Get-FileHash -LiteralPath ([IO.Path]::ChangeExtension($binary,'.pck')) -Algorithm SHA256).Hash
    viewport_width=$ViewportWidth
    runtime_timeout_seconds=$RuntimeTimeoutSeconds
    input_isolation_exercised=[bool]$ExerciseInputIsolation
    external_working_directory=$external
    rooms=$records
} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $destination 'verification.json') -Encoding UTF8
