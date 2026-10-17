$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-tablet-east.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher bare East tablet action - October3,2026

character/krusher-tablet-east-v1 fits141source lift/read/stow poses(5500ms) to
selected James utility Krusher. Existing East head/collar tracking and cyan suit
mask retain body/tablet/glove motion. Start/return complete RGBA match canonical
idle after4faint fringe corrections.425composition/574independent checks0;
actual consumer427checks0 including finite tail, exit0 /5.74s. Scratch APPDATA/
all2930 owner files unchanged. Key poses/all141head-tablet crops/native read
viewed;5.5s source-derived preview247995bytes. No full temporal/world acceptance.
Initial424native capture-list error superseded; current action captures named
start/lift/read/return. Next helmet fit and paired preview; selectors unchanged.
Handoff: character/krusher-tablet-east-v1/HANDOFF.md. Goal active.

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
