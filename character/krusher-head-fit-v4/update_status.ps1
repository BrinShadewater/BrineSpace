$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-v4.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher head repair delivered as a reviewable V4 candidate - October 4, 2026

Krusher Dom / System Administrator / AI & Robotics / James utility suit /
matte muted cyan #527C80. Replaced the rejected head set with complete authored
skin-neck heads, natural helmet faces, quarter/pitch/rest variants and matte
visor lining; removed old hair/collar fragments and duplicate underwater faces.
All 586 states / 8,058 frame references now propagated to repaired candidates.
Portable character/krusher-animation-package-v4: 3,486 PNGs; 16,790 source and
57,025 native loader checks pass. Fresh station repair, furnished water routes,
West unloading/cue guards and bunk lifecycle: 15,973 checks, zero failures,
352 captures. Selected native room views and source boards visually reviewed.
Each native run preserved all 2,935 fingerprinted non-log owner files.
Original bodies, shells, props, clocks, pivots and source density retained.
Head-repair deliverable complete; owner visual acceptance remains their judgment.
Candidate UNSELECTED for normal roster; no playable/perk/save integration.
Mobile preview: character/krusher-head-fit-v4/mobile-head-review.png.
Scope and evidence: character/krusher-head-fit-v4/HANDOFF.md.

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
