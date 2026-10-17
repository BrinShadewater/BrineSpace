$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-construction-meals.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher meal, pickup and equipment complete-head candidates - October 3, 2026

Full animation goal active/incomplete. Meal-family-v3, helmet-transition-v3,
meal-service-v3:106states/612refs/147unique records/104revised. Original v1
whole manifests exact; complete H3 heads/necks, original food/cup/hand foreground,
helmet alpha and lower bodies preserved. New deeper South head masters retain
builtin raw/prompt/alpha extraction/hashes.1621independent checks0/49bare source
contacts/100exact idle joins. All147source contexts across6boards reviewed,
plus representative native large/small meals, partial/equipped helmet and pickup.
3980native checks0:meal641/48captures/7.50s,equipment172/24/7.07s,
service3167/492rows/39unique captures/8.19s. All engine0/noerrors/scratchAPPDATA;
2930owner nonlog files unchanged each interval. Source-hold native pose replays
18.00/4.383333/7.20s within1frame; not continuous station acceptance. Updated
mobile overview/full sheets/HTML/MP4/ZIP delivered. Selected full bank stays old.
Remaining cargo/rest/water-cargo/interruption/death/recovery head migration,
rear/quarter identity and residual yellow shoulder cyan pass, coherent bank,
strict West cues/service-loss and actual changed station/bare-water closeout.
Handoff:character/krusher-head-fit-v3/MEALS_HANDOFF.md. No approval gate/live job.

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
