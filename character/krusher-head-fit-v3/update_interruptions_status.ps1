$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-construction-interruptions.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher underwater interruptions complete-head candidate - October 4, 2026

Goal active/incomplete. Water-interruptions-v2:144states/1104refs/198unique,
148revised. Original whole manifests/body/tools/event clocks retained;94exact
corrected shared poses and0,96registered padding.39bare full source/neck contacts.
Original West face fragment removed; complete head registered8pxleft and tool
mask excludes observed head. Original-skin visor masks and palette leak restoration
preserve shell/rim/alpha. All148changed contexts and targeted native full/small views
reviewed.3317source+986independent+13439native checks0/1104prescribed captures;
1920distress timer samples/8phase resets. Scratch APPDATA;2930owner files unchanged.
552paired original holds37.64s; not continuous station acceptance. Full selected
bank unchanged. Next death, identity/cyan audit, coherent bank/package, West and
actual station/bare-water closeout. No live jobs/approval gate.
Handoff:character/krusher-head-fit-v3/INTERRUPTIONS_HANDOFF.md.

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
