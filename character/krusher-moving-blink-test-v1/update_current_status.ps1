$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-moving-blink.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher Dom moving south blink comparison - October 2, 2026

character/krusher-moving-blink-test-v1 fits the authored eye edit to existing south
bare idle, preserving all73body poses and holds. Frames47/48 close eyes for84ms at
1958-2042ms in the3,042ms cycle. Existing consumer native comparison:219paired
pose events over3cycles; Godot4.7.2 exit0/14.26s.956native clock/coverage checks and
296source/native body-protection checks pass, zero errors. All2,930fingerprinted
owner files unchanged under scratch APPDATA. Native closed pose visually reviewed;
face/neck/body stable, small display change subtle. Complete natural-blink motion
acceptance remains separate.85,510byte MP4 and browser blink/hold controls retained;
closed pose seek/pause verified at1.98s. Current runtime candidate unchanged.
Helmet/profile fitting remains separate; see candidate HANDOFF.md.

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
