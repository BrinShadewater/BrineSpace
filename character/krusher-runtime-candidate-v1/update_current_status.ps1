$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-package.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher Dom consolidated runtime candidate - October 2, 2026

character/krusher-runtime-candidate-v1 consolidates four-direction idle/walk and
west terminal raise/type/lower, 11 states per gear. 970 unique PNGs / 986 frame
references; exact terminal idle and held aliases. 3,015 package checks passed.
Existing CrewSpritePlayer native probe: 3,967 checks, zero errors, Godot 4.7.2
exit 0 / 6.55 seconds. Every frame midpoint resolves to exact source pixels; gear
admission, metadata, filters and clocks pass. All 2,930 fingerprinted owner files
unchanged under scratch APPDATA. Terminal native sample visually inspected.
PNG LFS attributes verified. No normal selectors or gameplay changes. Complete
artistic motion acceptance remains separate. README.md and HANDOFF.md retain
scope, sources and rebuild commands; frame_at_elapsed loop callers need modulo.

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
