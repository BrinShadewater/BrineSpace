$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-water.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher swimming/treading/start-stop candidates checked - October 3, 2026

Full goal active/incomplete. Staged234bare/144helmet,104missing swim states per gear.
Basic water32states/192references/112unique;168composition/1080independent/
6078native checks pass. All32entry/exit joins,8reversed choreographies,
16loop wraps exact.192native captures,3840continuous gait samples,
16automatic start/stop transitions. Original256x276/128128/standing148;
water metadata and selected North-polish overrides retained. Open-eyed heads,
South foreground gloves/wrist metal preserved. Scratch APPDATA/2930owner
files unchanged; engine0/14.58s/no logged errors.19.52s coherent paired sprite
replay, not live station recording. Final full-library identity/material/
camera/joins and native station lifecycle/contact acceptance remain open.
Next underwater turns/carry/pickup/cancel/release/distress and console overrides.
See character/krusher-water-family-v1/HANDOFF.md.

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
