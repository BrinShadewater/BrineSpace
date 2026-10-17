$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-construction-cargo.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher cargo complete-head candidate - October 4, 2026

Full goal active/incomplete. Cargo-family-v3/cargo-settle-profile-v3:50states,
342refs/148unique/120revised/28rear retained. Original whole cargo manifests,
body/case/hands/lower body, helmet alpha and clocks preserved; nearest West
settle root profile exact except whole candidate paths. New four quarter full
head/neck masters preserve builtin raw/prompt/alpha extraction/native hashes.
Detached East-to-North poses registered whole heads down4/2pixels; inherited
isolated face scraps removed, no painted neck. North-to-West helm4 restored
original hardware outside observed visor polygon (old warm-metal hull error).
1549independent checks0/63complete bare source/topology/collar contacts,
64join comparisons/12source-equal joins. All120changed contexts/3boards and
targeted native full/small formerly detached/quarter/restored shell views reviewed.
Final native4482checks0/154captures/engine0/12.64s;1920distance-driven gait
ticks/24automatic turns. ScratchAPPDATA;2930owner nonlog files unchanged.
171paired source holds20.880s/encoded20.883333s within1frame; not continuous
station/world contact acceptance. Mobile overview/HTML/MP4 delivered. Full selected
bank remains old; residual yellow shoulders remain open for cyan palette audit.
Next rest/water-cargo/interruption/death/recovery, rear/quarter/cyan audit,
coherent bank/package, strict West cues/service-loss and station/barewater refresh.
Handoff:character/krusher-head-fit-v3/CARGO_HANDOFF.md. No live job/approval gate.

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
