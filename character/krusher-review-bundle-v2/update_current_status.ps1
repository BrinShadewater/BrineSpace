$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-combined-review.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher combined Bill/James review and reuse guide - October 2, 2026

character/krusher-review-bundle-v2 combines current Bill and James sheets,
paired motion, facial studies and four-family references. Preview ZIP37files
4,228,860bytes; full ZIP1988files41,741,608bytes/1,946runtime PNGs. Bill11-state
and James8-state bare/helmet packages remain separate; guide preserves family
clocks, masks, collars and likeness fit. 8,029 delivery checks0. Current identity
and all four184x184/pivot92,172/standing148 manifests inspected. Browser390x844
width375,8images/4videos loaded, James playback advances; paused/reset viewport.
Actual owner phone access and final temporal polish remain separate. Veld/Marsh
remain static fits. Loopback preview server restarted after connection refusal;
tab9 retained. No sprites/normal selectors/NPC changed. Goal remains active;
see delivery HANDOFF.md and browser-verification.json for scope/next steps.

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
