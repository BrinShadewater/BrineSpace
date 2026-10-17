$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-construction-water-cargo.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher underwater cargo complete-head candidate - October 4, 2026

Goal active/incomplete. Water-cargo-turns-v3:64states/464refs/160unique,
138revised. Original whole manifests/body/case/tools/clocks/pivots retained;
16exact corrected water-v3/recovery-v2 shared poses. Complete cardinal/quarter
H3 heads and necks; rear helmet shell restored outside observed apertures.
2026source +783independent +7272native checks0;63bare contacts,
12shell checks,464prescribed captures,48automatic turns/1920distance gait ticks.
Scratch APPDATA;2930owner files unchanged; native28.26s.
All138changed source contexts and targeted full/small native views reviewed.
232paired original-hold replay25.12s; not continuous station acceptance.
Full selected bank unchanged. Next interruptions/death, identity/cyan audit,
coherent bank/package, strict West and actual station/bare-water closeout.
Handoff:character/krusher-head-fit-v3/WATER_CARGO_HANDOFF.md.

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
