$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-water-interruptions.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher complete animation coverage staged - October 3, 2026

All frozen338bare/248helmet states staged; goal active/incomplete pending full-library
visual consistency and native station lifecycle/contact acceptance. Latest pack:
character/krusher-water-interruptions-v1 adds144paired cancel/release/distress states,
1104references/198unique outputs.297composition/3317independent/13450native checks
pass;136indexed entrances/136empty-swim ends/16padded distress endpoints exact.
Original clocks/pivots/ruler/water flags and case release events preserved.
1104native captures,1920distress timer samples,8return gait-phase resets.
Scratch APPDATA/2930owner files unchanged at run; engine0/34.36s/no logged errors.
37.64s paired source-hold replay is not live station motion/contact proof.
Next: full head/material/camera audit and isolated station bunk/chair/tool/case/water
lifecycle review. See character/krusher-complete-animation-v1/HANDOFF.md.

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
