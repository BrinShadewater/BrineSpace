$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher Dom reusable Bill-body continuation — October 2, 2026

Owner direction: Krusher Dom / System Administrator / AI & Robotics, muted matte
grey-cyan; existing Bill/Veld/James/Marsh models can be reused by likeness/build.
New unselected character/krusher-bill-base-test-v2 covers cardinal idle/walk in
bare/helmet variants:948frames,5273package checks0errors. Original body pixels
outside head/marking masks, lower body/feet, timing and helmet silhouette retained.
Cardinal masters, sampled neck boards and browser walk playback reviewed; no
native station or owner acceptance claim. character/krusher-equipment-study-v1
adds12accessory views and four static hip fits. Moving attachment/hand contact,
typing/actions, expression/turn joins and station evidence remain. Goal active.
No normal actor/art selection or owner-save changes. Handoffs in both directories.

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
