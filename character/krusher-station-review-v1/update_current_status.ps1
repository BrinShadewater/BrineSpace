$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-station-review.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher station test delivered - October3,2026

Owner selected station test first, then requested retry. Fixture-only canonical-v4
Krusher replaces appearance in existing Branforth slot in actual main scene/core.
32prescribed action samples (4directions/2gears/4clocks), production core-floor
route191ticks/32captures. Clean retry260checks0failures, engine0/61.07s/no logged
script errors.67artifact checks0; scratch APPDATA/all2930 owner files unchanged.
First selected-only architect_run fixture was rejected for core lighting errors;
full core state retained, runner now rejects logged errors. Rejection recorded.
Actual room/fullscene/8pose sheet visually reviewed.6.4s walk MP4 uses0.2s sim
samples, not continuous recording.4file previewZIP1623946bytes. Normal roster,
perks, dialogue, recovery and save schema unchanged by this work; no new NPC.
Test covers one core-floor route, not doors/crowds/all rotations. Appearance
review delivered; next owner scope can address roster/behavior integration.
See character/krusher-station-review-v1/HANDOFF.md.

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
