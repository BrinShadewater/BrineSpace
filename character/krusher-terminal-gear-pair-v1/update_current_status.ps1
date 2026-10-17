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
## Krusher Dom terminal bare/helmet pair - October 2, 2026

character/krusher-terminal-gear-pair-v1 extends west raise6/type6/lower7 to both
gears with24 unique frames. Exact body equality below row62 in compatible west
masters permits existing pose reuse and fixed upper helmet/face pixels.182package
checks0errors; exact locomotion idle files, source body, helmet, clocks and joins.
Fresh Godot4.7.2 paired standalone preview:19paired captures,engine0/5.26s,
127native checks0errors. Rendered body/helmet stability and endpoint joins pass.
All2930owner non-log files unchanged with scratch APPDATA. Native type/release and
pair board reviewed; no continuous-motion or station/controller acceptance.
Only west family proved at row62; no blind reuse of this boundary in other views.
Full character/motion/gear-direction/turn-expression/station work remains active.
No normal selectors changed. Source evidence and HANDOFF.md in candidate folder.

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
