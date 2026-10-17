$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-construction-rest-recovery.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher rest and recovery complete-head candidates - October 4, 2026

Full goal active/incomplete. Rest-v4:30states/174refs/92unique/72revised;
recovery-salvage-v2:16states/96refs/86unique/65revised. Complete authored heads
and necks register to original body/collar poses; original helmets fit full visor
identity. Original whole manifests/clocks/pivots/tools/shell alpha retained.
Rest698independent/1290native; recovery692independent/764native; all errors0.
65full bare source/body contacts,137changed contexts and targeted native full/small
views reviewed.270prescribed captures; scratch APPDATA,2930owner files unchanged.
Original-hold videos25.48/15.36s within one frame; not continuous station acceptance.
Selected full bank remains old. Next underwater cargo/interruption/death,
rear/quarter/cyan shoulder audit, coherent bank/package, West and station review.
Handoff:character/krusher-head-fit-v3/REST_RECOVERY_HANDOFF.md.

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
