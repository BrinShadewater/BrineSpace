$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-delivery-package.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher salvage delivery and portable animation package - October 3, 2026

Goal active/incomplete. Four actual helmet salvage deliveries complete all phases,
all six pickup/unload poses, eight water carry turns, exact credit and fresh-scene
mid-return Continue.13103checks0,engine0/222.03s/no logged errors/scratch APPDATA/
2930owner unchanged. Native four-facing case/body reviewed;23.2s116snapshot gallery.
First fixture used nonadvancing return elapsed; rejected evidence retained, corrected
trigger to ten actual return ticks. No production gameplay change.
New krusher-animation-package-v1 includes338bare/248helmet states,8058pose slots,
3498self-contained PNGs, exact individual profiles/metadata, current James-body
character sheet and local viewer.8058copy/18462independent/57025native checks0;
native21.99s/owner unchanged. Full canvases fit corrected viewer, visual checks pass.
West floor-case cue hashes currently admit James only; Krusher cue compatibility
and actual West interruptions remain, plus bare flooded cancellation/cargo and
final full-library audit/closeout. Package staged/incomplete. See character/
krusher-station-lifecycle-v1/HANDOFF.md. Preview localhost8874 retained.


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
