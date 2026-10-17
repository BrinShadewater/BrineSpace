$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.crew-base-reference.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Reusable crew body family reference - October 2, 2026

character/crew-base-reference-v1 adds a sixteen-view comparison of Bill, Veld,
James (Branforth) and Marsh at shared 2x source scale, with original heads, colours
and equipment retained. Human rows follow declared ACTIVE_ASSETS matte locomotion;
Marsh follows ordered selected catalog overrides, including his current south idle.
Catalog records exact sources/hashes, body bounds, shared 184x184 / (92,172) / 148
standing profile and differing idle/walk coverage. 147 checks pass with zero errors;
all sixteen views visually inspected. README.md records the proposed body families,
Veld default suggestion, per-family tint/head/helmet rules and Krusher's demonstrated
Bill reuse. No new derivatives, original art changes or normal selector changes.
See catalog HANDOFF.md; shared metadata alone does not prove cross-family fitting.

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
