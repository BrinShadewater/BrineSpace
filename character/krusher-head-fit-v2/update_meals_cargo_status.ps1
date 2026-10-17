$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-meals-cargo-fit.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher meals, equipment and dry cargo head fit - October 3, 2026

Goal active/incomplete. New meal-family-v2:96refs/60changed,468independent/641native
checks0,16exact padded helmet idle joins, foreground hands/cups/utensils protected.
Helmet-transition-v2:24refs/12unique revised,99independent/172native checks0,
four exact idle endpoints and original exact reversal. Meal-service-v2:492refs/
39unique outputs all byte-identical;779independent/3167native checks0,80idle joins.
Padding validator repaired to retain original alpha_composite semantics for hidden
transparent RGB; no anatomy change needed in South/North service heads.

Cargo-family-v2:342refs/148unique/106changed,367composition/1245independent checks0.
Final native4478checks0/150snapshots/9.45s, distance carrying/24automatic turns;
original manifests/strides/clocks and64joins (12exact/52original variations) retained.
West nearest settle overrides retargeted in cargo-settle-profile-v2. Four rear-quarter
helmets had visible James faces: now use existing Krusher cardinal face sources
clipped to registered visor apertures. Rejected warm-metal segmentation painted
hardware in two rear views; comparison/raw candidates retained, final masks reviewed.
Source boards and native large/74px samples reviewed. All native runs scratch
APPDATA,2930owner nonlog files unchanged/engine0/noerrors. Replays: meals18s,
equipment4.383333s,service7.2s,cargo20.88s; prescribed source/snapshot replays only.

New candidates listed only; full bank/package still old while rest/water/water
cargo/interruption/death/recovery and joins need correction. Strict West release
hashes must be rebound when selecting revised cargo. Residual yellow department
shoulder panels observed in reused quarter cargo body: final palette audit remains.
Changed world contexts, West service-loss diagnostic, bare-water and full-library
closeout remain. See new pack HANDOFFs. No live process or external blocker.


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
