$ErrorActionPreference = 'Stop'
$krusherStatusPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../docs/CURRENT_STATUS.md'))
$krusherTempPath = Join-Path ([IO.Path]::GetDirectoryName($krusherStatusPath)) 'CURRENT_STATUS.krusher-rest-water-fit.tmp'
$krusherInput = $null
$krusherOutput = $null
try {
    # Preserve the large concurrent status file byte-for-byte. Deny writers while
    # copying; permit atomic replacement so the original cannot be partly written.
    $krusherInput = [IO.FileStream]::new($krusherStatusPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, ([IO.FileShare]::Read -bor [IO.FileShare]::Delete))
    $krusherOutput = [IO.FileStream]::new($krusherTempPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    $krusherHeader = @'
## Krusher rest and swimming head fit - October 3, 2026

Goal active/incomplete.
rest-family-v3: 174 references, 36 unique poses changed; 902 independent and 1290 native checks, zero errors. Original manifest objects retained. Replay 25.483333s, original holds within one encoded frame.
water-family-v2: 192 references, 70 unique poses changed; 1236 independent and 6066 native checks, zero errors. Original manifest objects retained. Replay 19.516667s, original holds within one encoded frame.
Original bodies, manifests and helmet alpha protected. All9 source boards and representative native large/small views reviewed. Scratch APPDATA,2930 owner nonlog files unchanged. Added four corrected candidate manifests only; full bank/package remain older. Watercargo/interruption/death/recovery and joins remain; final palette audit includes yellow West reclined rest shoulder patches. Strict West hash refresh, service-loss diagnosis, changed station and barewater proof remain. See new pack HANDOFFs. No live process or blocker.


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
