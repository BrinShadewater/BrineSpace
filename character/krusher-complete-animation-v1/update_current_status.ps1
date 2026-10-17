$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-cargo.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher cargo animations checked - October 3, 2026

Full animation goal active/incomplete. Staged187bare/97helmet states;
151missing per gear against frozen selected James338bare/248helmet states.
Cargo50states/342references/148unique outputs: pickup, carry, unload,
12quarter/half turns and West settle per gear. Original256canvas/foot128224,
standing148, per-direction travel stride and source pose metadata retained.
Four authored intermediate yaw heads; matte cyan markings; case/hands protected.
219composition/1283independent/4470native checks pass,150native samples.
1920actual distance-driven gait samples visit all6poses,24automatic turn
sequences resume destination gait pose0. Engine0/13.29s, no logged errors;
scratch APPDATA/all2930owner files unchanged. Full-pose20.88s paired MP4.
Original floor cases retained.12of64source task/turn joins exact; remaining
source variation/full station cargo lifecycle contact still needs final review.
Build uses frozen cargo scope, with25state-per-gear guards; goal remains active.
Next rest/lying/sleep, recovery/salvage/death, swim/tread and final whole library.
See character/krusher-cargo-family-v1/HANDOFF.md and complete-animation handoff.

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
