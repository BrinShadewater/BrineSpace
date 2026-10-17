$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-head-fit.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher owner head-fit correction - October 3, 2026

Owner reports helmet head too small and bare side heads disconnected from collar.
This supersedes earlier visual-readiness claims; goal active/incomplete.
New krusher-head-fit-v2 preserves exact prompt/reference baseline and built-in
imagegen fit study. Generated body pixels not used. Native eight-pose reference
uses existing source heads: side heads back2/down2, helmet face fit enlarged inside
visor; original184canvas/92,172pivot/ruler148/body rows54+ retained.16protection
checks0. Sheet reviewed, not full animation propagation/native motion acceptance.
West exact Krusher cue admission added alongside unchanged James cues. Actual
West fixture95checks14failures/51.46s/owner2930unchanged: all service-loss returns
failed to start; direct cue/rejection guards pass. Diagnose actual controller state.
Next propagate corrected head/neck fit coherently, refresh package/cue bindings,
finish bare-water/West contexts and full visual review. See character/
krusher-head-fit-v2/HANDOFF.md. No live native process or external blocker.


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
