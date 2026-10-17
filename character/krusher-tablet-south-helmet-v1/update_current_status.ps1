$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-tablet-south.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher paired South tablet action - October3,2026

Source continuity assessment shows South/West/North original141/154/137pose
5500ms actions have exact original-idle body start/returns below54. Source sheet
viewed, hashes retained in krusher-tablet-source-continuity-v1. New South bare/
helmet141poses each: canonical idle RGBA joins exact, cool-grey tablet/source
motion/shell protected. Bare425/574/native427checks0(exit0 /5.36s); helmet423/
716/native428checks0(exit0 /5.64s). Scratch APPDATA/all2930 owner files unchanged.
Paired/key/all141helmet crops/native read viewed;5.5s preview225560bytes. No
full temporal/world acceptance. Next West/North fitting, then combined joins.
Canonical-v2 still East-only combined package. Normal selectors unchanged.
See character/krusher-tablet-south-helmet-v1/HANDOFF.md. Goal active.

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
