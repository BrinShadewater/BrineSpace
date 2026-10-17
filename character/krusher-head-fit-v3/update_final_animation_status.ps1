$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-animation-complete.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher complete corrected-head animation package - October4,2026

Complete original animation scope:338bare/248helmet states,8058refs/3502PNGs.
Offline progress now selects coherent package-v3. Connected heads, fuller helmet
faces, clean hair and reviewed matte muted cyan#527C80. Full source-contract
coverage/hashes/profile clocks pass;54registered padded states preserve pivots
and148pixel density.35749palette+57025native+637preview checks;930joins0regressions.
Current station repair/galley/bunk/chairs/construction/workshop/mortality/water/
barecargo/West/delivery/recall all functional checks0/engine0; delivery and recall
fresh-scene Continue, barewater4routes+48indexed cancellations. Native detail
boards reviewed, mobile GIF and full portable viewer delivered. Runs use scratch
profiles; later fingerprints record independent normal-gamePID169528writes in
real profile, not unchanged-owner claims. No task edits/restores of real saves.
Owner visual acceptance separate; roster/perks/export outside animation scope.
Handoff:character/krusher-head-fit-v3/FINAL_ANIMATION_HANDOFF.md.
No live process or required animation work remaining.

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
