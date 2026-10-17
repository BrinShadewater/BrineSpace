$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-station-lifecycle.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher native bunk contact and North rest correction - October 3, 2026

Goal active/incomplete; all338bare/248helmet states remain staged. Real main scene
bunk test uses production fatigue chooser/route/arrival/update, merged Krusher packs.
Final239checks/30captures pass, camera visibly centered and entire sprite canvas
inside grid; engine0/58.17s/scratch APPDATA/2930owner files unchanged. First RNG setup
and second camera-omitted runs rejected, retained. Lower mattress contact visually
reviewed;4.68s paired native pose replay, not continuous station recording.
North reclining/lying crown corrected in krusher-rest-family-v2: seven bare outputs
changed,85others including allhelmet outputs byte-identical.138composition/
752independent/1307native checks pass,174captures,20joins; engine0/15.33s/owner unchanged.
Next: reachable chair/read/rise, tool/cargo/water/floor/death contact and remaining
full-library identity/material/camera/joins. See character/krusher-station-lifecycle-v1/HANDOFF.md.

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
