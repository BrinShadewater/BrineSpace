$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-construction-canonical.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher complete head/neck canonical and inspection candidates - October 3, 2026

Owner head rejection remains governing; complete animation goal active/incomplete.
Canonical-v6 revises1314E/S/W drawings/2122refs with complete head/neck and
full visor identity on original James bodies.361rear retained. Original manifest
bytes exact, tablet foreground protected,16idle joins exact.12941independent
checks0 including657bare collar/topology contacts. All21 source boards/1314
contexts and representative native East idle/West walk/South tablet reviewed.
Native4256admission/3271events/144.41s/engine0: second cycle all1637slots selected;
first capture cycle missed912,916,920. Three controlled midpoint captures fill
67.305s source-hold replay (67.3s encoded).12late draws,max11.072ms; not perfect
wall-clock cadence or station distance gait proof. Motion audit11456checks0.
Inspection-v3 maps1146refs/8states exactly to revised drawings;2328independent,
8033nativechecks0/7.36s/engine0. All native runs scratchAPPDATA,2930owner files
unchanged. Full selected bank/package still older; no normal playable installation.
Next repair/torch/seated then remaining families, rear/quarter/cyan shoulder audit,
coherent bank/package and strictWest/service-loss/barewater/world closeout.
No live process, blocker or approval gate. Handoff:
character/krusher-james-canonical-v6/HANDOFF.md.

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
