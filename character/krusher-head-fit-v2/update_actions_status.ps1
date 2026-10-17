$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-actions-fit.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher action head-fit candidates - October 3, 2026

Goal active/incomplete. Repair-v2, torch-v2 and seated-v2 carry owner correction
through 96 paired states/1710 pose refs/972 unique outputs,648 changed. Existing
pitched identities retained; bare side heads back2/down2 with protected collars,
marks and foreground; visible helmet faces enlarged inside bounded visor. North
rear unchanged. Exact original root/state clocks;48 canonical-v5 standing joins.
1560composition/2511independent/12075native admission checks0. Native render10770
checks0/288snapshots. All runs scratch APPDATA;2930owner nonlog files unchanged.
Changed-head chronology boards,source sheets and native large/92px views reviewed.
Three paired all-source-hold replays: repair12.668s,torch12.468s,seated30.640s;
source replays,not continuous station capture or new world contact acceptance.
New packs listed in visualReview.correctedCandidates only. Full bank/package
remain old while helmet transitions/meals/cargo/rest/water/interruption/death/
recovery and joins need coherent correction. See new pack HANDOFF.md files.
No live process or blocker. West service-loss/bare water/world closeout remain.


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
