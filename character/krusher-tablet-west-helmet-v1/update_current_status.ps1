$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-tablet-west.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher paired West tablet action - October 3, 2026

Owner-selected James utility suit retained for Krusher Dom, System Administrator,
AI & Robotics, matte muted cyan #527C80. West bare/helmet 154 poses each, 5500ms;
complete canonical idle start/return RGBA exact. Source tablet, clock, body and
helmet shell protected. Bare 464/626/native466 checks zero (exit0 /5.99s);
helmet 462/781/native467 zero (exit0 /6.28s). Scratch APPDATA; all2930 owner
non-log files unchanged. Paired keys/native read/all154 helmet crops viewed.
Paired source-derived preview 228713 bytes /5.5s, not continuous native capture.
North source turns rear-to-right toward tablet; needs authored angled head
reference. Diagnostic warm pixels include hair and do not measure skin/angle.
Canonical-v2 still East-only combined package. Goal active; selectors unchanged.
See character/krusher-tablet-west-helmet-v1/HANDOFF.md.

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
