$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-station-chairs.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher chair/tablet station and whole delivery checks - October 3, 2026

Goal active/incomplete; all338bare/248helmet states staged. Actual merged station
chair/tablet fixtures:2rooms/four rotations/2gears,384captures,931lounge and1531
observation checks pass, engine0/97.97s and132.49s/no logged errors/scratch APPDATA/
2930owner files unchanged. North chair and South sofa contacts visually reviewed.
37.04s paired original-hold native replay, not continuous station recording.
Complete source delivery25150checks0;54registered pad cases retained. West settle
filter mismatch repaired by exact source-root override manifests, no raster change.
All8058slots checked in complete merged native delivery:57025checks0,586states,
geometry/clocks/pixels/original settle-nearest; engine0/22.21s/owner unchanged.
Remaining: tool/cargo/water/floor/death actual station lifecycle/contact and final
full-library identity/material/camera/joins. See character/krusher-station-lifecycle-v1/HANDOFF.md.

'@
    $krusherBytes = [Text.UTF8Encoding]::new($false).GetBytes($krusherHeader + "`n")
    $krusherOutput.Write($krusherBytes, 0, $krusherBytes.Length)
    $krusherInput.CopyTo($krusherOutput)
    $krusherOutput.Flush($true)
    $krusherOutput.Dispose()
    $krusherOutput = $null
    [IO.File]::Replace($krusherTempPath, $krusherStatusPath, [NullString]::Value)
    Write-Output 'CURRENT_STATUS.md updated atomically; previous content preserved.'
} finally {
    if ($null -ne $krusherOutput) { $krusherOutput.Dispose() }
    if ($null -ne $krusherInput) { $krusherInput.Dispose() }
}
