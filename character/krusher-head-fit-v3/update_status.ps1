$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-construction-water.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher complete head/neck sources transferred to water candidate - October 3, 2026

Goal active/incomplete; latest owner head rejection remains governing.
New head-fit-v3 has side and front/bowed generated sources, exact prompts,
explicit extraction polygons/boxes/native sizes and hashes. Generated body and
helmet shell pixels are not used in production body composition.

Water-family-v3:112unique/192refs,84E/S/W heads revised,North28retained.
Complete bare head/neck replaces interfering original head/collar pixels;
complete identity fitted through registered visor apertures, original helmet
shell alpha and glass protected. Original full manifests byte-identical,body
outside local edits exact;32joins/8reversals/16loop endpoints retained.
940independent checks0;42bare head topology/contact checks0 (minimum3body-edge
pixels), pose-aware upper/back crown contact for prone South. Broad removal
ellipse had erased original collar: native playback passed but topology failed.
Rejected four actual native South gap screenshots retained; narrow old-head
removal and South up3registration retain actual original collar.

Final native6066checks0/192prescribed captures/9.58s/engine0/noerrors;
scratchAPPDATA,2930owner nonlog files unchanged. All84changed drawings across
six source boards, equal3x before/after views and representative actual native
large/small captures reviewed. New14.64s108paired source-hold replay includes
updatedE/S/W only; not continuous station footage or whole-bank acceptance.
Full selected bank/package still old. Next canonical idle/walk/tablet and
inspection using new sources, then remaining dry/life/water families and joins,
rear/quarter/palette review, full package and strictWest/world/barewater closeout.
No live process, approval gate or blocker. Handoff:character/krusher-water-family-v3/HANDOFF.md.


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
