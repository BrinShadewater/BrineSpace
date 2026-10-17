$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-review-delivery.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher Dom portable review delivery - October 2, 2026

character/krusher-review-bundle-v1 consolidates current sheets, complete motion,
separate facial studies and body-family comparison into one responsive index.html.
Preview ZIP: 25 files / 2,254,406 bytes. Full ZIP: 998 files / 20,327,987 bytes,
including 970 runtime PNGs and self-contained manifests. Original source bytes,
fonts/OFL and NOTICE retained; no publication or external upload. 4,052 source,
ZIP/resource/runtime/chapter checks pass with zero errors. At 390x844, character
sheet visible initially, all images/videos load, no horizontal overflow; terminal
chapter seek/play verified. Browser viewport reset. Actual owner phone access and
artistic motion acceptance remain separate. Optional Bill/James/Marsh build choice
asked; no response this turn, current Bill work retained. Facial studies stay out
of runtime manifests. Existing selections unchanged; see delivery HANDOFF.md.

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
