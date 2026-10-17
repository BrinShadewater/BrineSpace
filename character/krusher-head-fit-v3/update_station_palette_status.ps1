$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-final-cyan-recall.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher corrected head and final cyan station milestone - October 4, 2026

Package-v3 full586states/8058refs/3502PNGs has attached complete heads,
fuller helmet faces and clean hair.457drawings/12310explicit shoulder pixels
recoloured; all529selected final contexts/12boards and mobile views reviewed.
35749palette+57025native bank checks0;930joins/796exact/0regressions.
Pure base water clearance preview637checks/88cases0. Current staged station:
delivery13103checks/4rotations/fresh-scene Continue; water6399checks/8routes/
bothgears; West383checks/14interruptions. All engine0 and scratchAPPDATA;
2930owner files unchanged. Eight delivery,water and West detail views reviewed.
Recall14643checks/4journeys/fresh-scene Continue,engine0/270.11s. No live job.
Full animation goal active;
other lifecycle refresh and furnished bare-water cargo/cancellation pending.
Normal roster/selected bank unchanged; visual owner acceptance separate.
Handoff:character/krusher-head-fit-v3/STATION_PALETTE_CLOSEOUT.md.

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
