$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-water-cargo-turns.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher underwater turns/carrying/pickup candidates checked - October 3, 2026

Full goal active/incomplete. Staged266bare/176helmet,72missing states per gear:
68water cancellations/releases and4distress. New64paired states/464references/
160unique,240composition/2026independent/7283native checks pass.16pickup joins,
8carry wraps,96turn/gait joins and48reversed choreographies exact. Whole-source
RGBA equality preserves shared endpoints despite differing PNG encodings.
Source256x276/128128/standing148 and per-group filters/strides retained.
464native captures,1920continuous cargo gait samples,48automatic swim/carry
turns. Reviewed quarter-view hip wrench/attachment retains original pixels.
Scratch APPDATA/2930owner files unchanged; engine0/21.01s/no logged errors.
25.12s paired original-hold sprite replay, not live station recording.
Final full-library identity/material/camera/joins and station lifecycle/contact
acceptance remain open. See character/krusher-water-cargo-turns-v1/HANDOFF.md.

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
