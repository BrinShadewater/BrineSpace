$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-workshop-torch.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher production workshop and paid torch station review - October 3, 2026

Goal active/incomplete; all338bare/248helmet states staged. Eight ordinary workshop
journeys in current James cargo actor/player with Krusher packs, four rotations/two
gears: inspection/work/pickup/generated carry route/turn/unload/idle.19391checks0,
100native captures,engine0/81.43s/no logged errors/scratch APPDATA/2930owner files unchanged.
Two normal paid North-core life-support builds, Metal24->19 each, draw/weld/stow,
power-off exact pose/stow/hold/pause/return and exact held-pose restoration.
2565checks0,28captures,engine0/53.81s/no logged errors/owner unchanged. Rejected
missing-floor and blocked-center fixture runs retained; final uses real floor node.
15s workshop and4.2s torch paired snapshot galleries,300ms/sample, not continuous
recordings. Native carry/tool/hold contacts visually reviewed. No gameplay/art edits.
Remaining water/floor/death/repair and West release interruption contexts plus final
full-library consistency/joins/delivery. See character/krusher-station-lifecycle-v1/HANDOFF.md.

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
