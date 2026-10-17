$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-mortality-galley.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher station mortality, recovery and galley - October 3, 2026

Goal active/incomplete; 338 bare / 248 helmet states staged. Actual production
actor/player with current candidate bank: dry/flooded death four directions x both
gears, all eight recoveries, and default galley four rotations x both gears.
Mortality 779 checks / zero failures / 184 captures / 24 cases, engine 0 / 98.92s.
Galley 13323 checks / zero failures / 132 captures / eight cases, engine 0 / 85.92s.
Both no logged errors, scratch APPDATA, all 2930 owner non-log files unchanged.
Clear corpse floor contacts, underwater visibility and recovery sheets reviewed.
Galley contacts all North, not four meal facings; bare completes all six food/cup
phases with hunger relief; sealed helmet uses inspect. Counter/hand/foot reviewed.
27.6s mortality and 26.4s galley selected snapshot galleries, not continuous video.
No production gameplay/roster edits. Remaining bare-water cancellation, water
carry/turn/delivery, West floor-case interruptions and final portable delivery.
See character/krusher-station-lifecycle-v1/HANDOFF.md.


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
