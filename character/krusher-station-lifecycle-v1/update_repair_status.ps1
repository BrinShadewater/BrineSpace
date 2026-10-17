$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-turn-repair.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher turn cleanup and floor maintenance review - October 3, 2026

Goal active/incomplete;338bare/248helmet staged. Underwater turn v2 corrects24bare
original-head silhouette/fringe outputs,56bare/all80helmet and all state endpoints
unchanged.240composition/2026independent/228revision/7286native0;464captures,
engine0/22.53s/owner unchanged. True alpha composite diagnostic reviewed; one
initially assumed stray alpha1 red point belongs to authored Krusher head, retained.
Final candidate selects v2; complete25150audit/57025native8058slot checks pass,
engine0/21.58s/no logged errors/scratch APPDATA/2930owner files unchanged.
Four actual storage-equipment floor facings x both gears, ordinary arrive/update
kneel/repair/stand/idle, exact source every60Hz tick/fixed clear foot/camera.
8951checks0,120captures,engine0/81.99s/no errors/owner unchanged.18s60paired native
snapshot gallery at300ms each, not continuous motion. Floor contact views reviewed.
Initial empty-goal fixture expectation rejected: all8stages completed and normal
controller selected next curiosity task. Final records successor; no gameplay edits.
Remaining death/recovery/bare-water cancellation/carry/West release/galley contacts
and final full-library review/portable delivery. See character/krusher-station-lifecycle-v1/HANDOFF.md.


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
