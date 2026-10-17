$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-v5.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher V5 native canonical head/cyan milestone - October 4, 2026

Owner says bare side head connections look better; remaining yellow accents must
be muted matte cyan #527C80, then “keep going.” Native canonical-v8 now revises
24 idle/walk/tablet states / 2,122 references across four facings and both gears.
Complete authored skin-neck heads use one uniform nearest export. Original body,
collar/shell geometry, clocks, pivots and H148 ruler retained; painted gold body
accents converted to shaded cyan. 2,138 body/shell/join checks, 2,122 canvas checks,
52 metadata comparisons and 14,881 native loader checks pass, zero errors.
Scratch APPDATA: all 2,935 fingerprinted owner non-log files unchanged.
Standing, tablet and selected source-clock walk phases visually inspected.
Preview: character/krusher-head-fit-v5/standing-review-mobile.png and
walk-review-mobile.gif. Other 562 action/life/water states remain historical V4;
full V5 propagation, coherent bank and fresh station review still pending.
Unselected candidate; no normal roster/gameplay/save edits. Current handoff:
character/krusher-head-fit-v5/HANDOFF.md.

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
