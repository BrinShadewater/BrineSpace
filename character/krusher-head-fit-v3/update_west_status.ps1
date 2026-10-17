$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-h3-west.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher corrected-head West station returns - October 4, 2026

Goal active/incomplete. H3 package-v2 station fixture:383checks0failures/
14cases(all7unload indices,bothgears),84room captures+14diagnostic records.
Engine0/72.12s/scratch APPDATA/2930owner files unchanged. Representative room
views reviewed. Earlier service-loss failure was fixture delta0: controller
skips delta<=0. Positive1microsecond steps exercise real return controller.
Exact current cue guards admitted; original James and altered-cue checks pass.
Quarter review confirms residual gold shoulder patches; proposal mask also
selects helmet hardware, so no global palette edits. Next explicit shoulder
masks and remaining station/barewater/Continue closeout. Selected bank unchanged.
Handoff:character/krusher-head-fit-v3/STATION_WEST_HANDOFF.md.
No live process or approval gate.

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
