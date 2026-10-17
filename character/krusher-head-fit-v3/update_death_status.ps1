$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-construction-death.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher death complete-head candidate - October 4, 2026

Full goal active/incomplete. Death-v2:16states/96refs/96unique/73revised;
original whole manifests/body/clocks/shell retained,8exact canonical-v6 starts.
New closed bowed heads preserve builtin raw/prompt/alpha/extraction hashes.
Complete sources registered to original collar; front lying source rigid35degree
rotation includes transformed neck-end checks.772source+478independent+
1012native checks0/96prescribed captures/33bare source contacts. All73changed
contexts and targeted full/small native fall/terminal views reviewed. Native8.78s,
scratch APPDATA,2930owner files unchanged.48paired original holds14.98s.
Source/prescribed playback checks do not establish actual station mortality.
Full selected bank unchanged. Next coherent coverage/join bank audit, rear/quarter
identity and cyan trim, package, West and actual station/bare-water closeout.
Handoff:character/krusher-head-fit-v3/DEATH_HANDOFF.md. No live job/approval gate.

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
