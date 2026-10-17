$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-veld-cardinal.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher Veld four-direction reuse trial - October 2, 2026

423 frames / eight cardinal idle-walk states in character/krusher-veld-motion-fit-v2
and krusher-veld-cyan-test-v2. Existing directional Krusher heads and matte muted
cyan #527C80; source body, tools, alpha, registration and gait clocks preserved.
Head-fit checks 846/1326 and cyan 1269/2169 pass. Existing consumer native probe
1277 checks, zero errors, exit 0 / 5.76s; scratch APPDATA and all 2930 owner files
unchanged. Cardinal and 72 side/rear collar samples reviewed. Source-timed video
18s / 867757 bytes. No full temporal artistic acceptance. Veld helmets untested;
Marsh static only. Earlier bundle-v2 retained. Normal selectors unchanged.
See character/krusher-veld-cyan-test-v2/HANDOFF.md for scope and next steps.

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
