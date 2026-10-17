$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-helmet-blink.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher Dom helmet blink reuse - October 2, 2026

character/krusher-helmet-blink-test-v1 fits the same authored south blink using the
original helmet face crop, 17 x 17 size and (83,29) placement. Original helmet
source hashes and reconstructed existing face pixels match exactly before edits.
Frames 47/48 change only filtered eye-source pixels inside the original face mask;
helmet, visor, body, alpha and all 73 source holds remain exact. Native comparison:
219 paired events over three cycles, Godot 4.7.2 exit 0 / 14.09 seconds. 956 clock/
coverage checks and 296 source/native protection checks pass with zero errors.
All 2,930 fingerprinted owner files unchanged under scratch APPDATA. Native closed
pose visually reviewed: stable placement, subtle eyelid change at display size.
Review MP4, exact fit records and HANDOFF.md retained. Current runtime package and
normal selectors unchanged; natural motion and owner acceptance remain separate.

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
