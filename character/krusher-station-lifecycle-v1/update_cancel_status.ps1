$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-cancel.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher actual exterior recall and indexed cancellation - October 3, 2026

Goal active/incomplete; all338bare/248helmet states staged. Four actual helmet
airlock/exterior pickup recalls with fresh-scene mid-action disk Continue using
Krusher bank before strict saved-art admission.48indexed branches from actual
work arrivals, all6work/all6pickup indices per facing,20case release branches,
exact entrance/empty join/fixed world anchors/actor-only restore/no credit.
14643checks0,engine0/220.68s/no logged errors/scratch APPDATA/2930owner files unchanged.
84selected native pose/source captures,16.8s snapshot gallery; actual body/case
separation reviewed all four directions. Not48complete trips or continuous video.
First runtime rejected because fresh scene loaded James bank before Krusher restore;
fixture ordering fixed, strict validation retained. No production/roster changes.
Source close-up found old neutral-grey/warm head remnants around bare quarter
turns (confirmed swim-carry-turn-east-south frame1); diagnostic/quarter-head-review.json
saved. Next v2 skull mask cleanup preserving body/hardware/helmets, then remaining
floor/life/water contacts and final full-library review/delivery.
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
