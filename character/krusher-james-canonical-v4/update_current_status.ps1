$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-selected-james.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher selected James reference and animation review package - October3,2026

Latest character/krusher-james-canonical-v4:2122PNG/12states each gear, cardinal
idle/walk/tablet with original source clocks/ruler and exact idle joins. North
six-view turn uses authored24x23heads; old James hair fringe removed in north-v3.
Helmet rear shell fully encloses face; original shell/alpha retained.
4474package/2146carry-forward checks zero (2011frames unchanged,111North corrected).
Prior all-direction native2298events/10349checks zero; corrected North562events/
2537checks zero, all4256package texture/clock admission checks zero; engine0/31.76s.
Scratch APPDATA/all2930 owner non-log files unchanged. Native joins and current
sheet/registered North viewed.46s compiled native-pose preview1555142bytes. Phone
viewport390x844:2sheets loaded/2videosready4,no overflow;46s playback reached end.
Preview ZIP6files/3246745bytes verified. Completion audit14requirements proved.
Requested selected-base reference/reuse test delivered; no NPC installation,
unrelated life actions, full micro-pitch equivalence or owner art acceptance
inferred. Source replay media is not unbroken recording; no physical phone test.
See character/krusher-james-canonical-v4/HANDOFF.md and completion-audit.json.

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
