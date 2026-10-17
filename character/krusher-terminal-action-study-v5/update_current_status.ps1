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
## Krusher Dom glove foreground and shared action master - October 2, 2026

character/krusher-moving-equipment-test-v2 adds cuff/orientation/material-tracked
source glove foreground over fixed equipment:948 cardinal bare/helmet idle/walk
frames,5722 checks0errors.674 overlapping frames,29650 source pixels restored.
Four bare walk boards and helmet west sampled; full-cycle mask review remains.
character/krusher-terminal-action-study-v5 rebases west raise6/type6/lower7 onto
that corrected idle byte-for-byte, removing27hip-pixel join mismatch.97package
checks and86native checks0errors. Fresh Godot4.7.2 standalone preview19captures,
engine0/4.95s; all2930owner non-log files unchanged with scratch APPDATA. Native
idle/type reviewed; no station gameplay or full continuous-motion acceptance.
Inherited alpha1 fringe markers retained; no bright native-rendered fringe found.
Full character polish/gear/views/turn-expression/station work remains active.
No normal art/controller selector changes. Both candidate HANDOFF.md files saved.

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
