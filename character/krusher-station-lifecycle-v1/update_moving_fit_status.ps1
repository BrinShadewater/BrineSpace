$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-moving-fit.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher moving head-fit candidates - October 3, 2026

Goal active/incomplete. Canonical-v5 propagates owner head correction through
24idle/walk/tablet states,2122pose refs/1675unique outputs/1062changed. Original
body/collar/tool protection and all metadata retained; eight neutral references
and eight tablet entrance/exit pairs exact.2761composition/5715independent checks0.
Native4256admission0/3270pose events/144.76s/owner2930unchanged. First capture cycle
missed4short West slots; second selected all1637slots,10draws up to11.004ms late.
Supplement12checks0/7.26s fills all4native captures; media67.3s1637pose replay,
not continuous station footage. Source and actual native head/collar views reviewed.
Inspection-v2 binds all1146old RGBA poses to corrected canonical,1146mask/8033native
checks0,7.88s/owner unchanged. New candidates not yet selected in full bank/package:
remaining-family head/helmet/joins must be corrected coherently first. World bare
water/West release diagnostics and full visual closeout remain. See character/
krusher-james-canonical-v5/HANDOFF.md. No live native process or external blocker.


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
