$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-construction-actions.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher repair, welding and seated complete-head candidates - October 3, 2026

Full animation goal active/incomplete. New builtin downward E/W head/neck and
visor sources saved with exact prompt, raw alpha, explicit polygons/native sizes
and hashes. Generated collars/helmet shells are excluded from body composition.
Repair/torch/seated-family-v3:96states/1710refs/972unique,748revised. Original
whole manifests byte exact; original bodies outside local heads, helmet alpha and
lower limbs exact.48standing joins match canonical-v6.7321independent checks0,
including365bare full-head source/topology/collar contacts. All748changed source
contexts reviewed across17pages, plus representative native full/small bare/helmet
repairEast,weldWest,seatedEast views. Residual original yellow shoulder trim is
visible: palette audit remains open, not silently accepted as cyan.
Native10770checks0/288prescribedcaptures across3isolated real-display fixtures:
repair4478/72/9.52s,torch4306/72/8.84s,seated1986/144/9.68s;engine0/noerrors.
ScratchAPPDATA;2930real nonlog profile files unchanged each run. Original-hold
paired source replays12.668/12.468/30.64s (encodedwithin1frame); not continuous
native/station motion or furniture contact proof. Whole selected bank still old.
Next meal/equipment and remaining cargo/rest/water/death/recovery head migration,
rear/quarter/cyan shoulder review, coherent bank/package, strictWest cue/service
loss and actual changed station/barewater/full-library closeout. No live process,
blocker or approval gate. Handoff:character/krusher-head-fit-v3/ACTIONS_HANDOFF.md.

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
