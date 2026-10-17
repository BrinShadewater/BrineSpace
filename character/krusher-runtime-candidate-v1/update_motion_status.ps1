$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-full-motion.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher Dom complete candidate playback - October 2, 2026

character/krusher-runtime-candidate-v1 now retains continuous native playback of
all 11 states per gear through existing CrewSpritePlayer. Two 22,480 ms cycles,
986 paired pose events, no skipped poses or consumer mismatches. Godot 4.7.2
exit 0 / 50.37 seconds; 4,444 checks passed with zero errors. Finish overrun6.669 ms,
max selection latency19.295 ms and draw latency33.298 ms. All2,930fingerprinted
owner files unchanged under scratch APPDATA. All289bare idle native-size crops
reviewed chronologically, without an obvious head/equipment discontinuity.
Complete review/full-motion-preview.mp4 includes493paired captures, all11chapters,
1,118,590bytes; browser idle chapter seeking/playback verified. Source clocks and
art unchanged. Temporal artistic acceptance remains separate; no normal selection
or station/controller change. See candidate README.md and HANDOFF.md.

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
