$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-v6.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher bare animation collar registration repair - October 4, 2026

Owner says bare animation heads look less connected. Canonical-v9 retains current
V5 heads/cyan suit; bare heads now register to original body/collar bands instead
of legacy portrait offsets and insert two source pixels deeper, with original
collar foreground overlap. All 1,061 bare references have opaque four-neighbour
head-to-torso contact and at least 13 collar contact pixels. All 1,061 helmet
references remain byte-identical. 2,138 source/join checks, 2,122 canvas checks,
52 metadata comparisons and 14,881 native loader checks pass; zero failures.
Scratch APPDATA: all 2,935 owner non-log files unchanged. 4.5-second source-clock
motion comparison: character/krusher-head-fit-v6/bare-connection-review.gif.
Selected before/after views inspected; owner moving-anatomy judgment remains open.
Only 24 canonical states revised; other 562 action/life/water states still pending.
No normal roster/gameplay/save or fresh station lifecycle changes. Handoff:
character/krusher-head-fit-v6/HANDOFF.md.

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
