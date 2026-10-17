$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-water.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher flooded station movement review - October 3, 2026

Goal active/incomplete; all338bare/248helmet animation states staged. Four actual
furnished default storage-bay swim routes x both gears,93% water. Production
movement/rendered Krusher poses, every route segment and destination, low-air
distress/air restoration/camera verified.6471checks0,98captures,engine0/81.2s,
no logged errors/scratch APPDATA/2930owner non-log files unchanged. West start and
East stop both gears play; six starts suppressed by actual furniture transition
clearance, recorded and verified. Rejected endpoint/unconditional-start fixture
runs retained. Native body/head/helmet water contact views reviewed;14.7s paired
49snapshot gallery, uniform2x source crops, not continuous station recording.
No production gameplay/art/roster changes. Remaining exterior cargo cancellation/
case-release, floor repair/death/West release, quarter-water pitch and final full
library identity/material/joins/delivery. See character/krusher-station-lifecycle-v1/HANDOFF.md.


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
