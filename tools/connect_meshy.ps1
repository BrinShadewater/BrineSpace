param([switch]$Check)
$ErrorActionPreference = 'Stop'
$keyDirectory = Join-Path $env:LOCALAPPDATA 'BrineSpaceTools'
$keyPath = Join-Path $keyDirectory 'meshy-key.dpapi'
$secret = $null
$plain = $null
$headers = $null
try {
    if ($Check) {
        if (-not (Test-Path -LiteralPath $keyPath)) {
            Write-Host 'Meshy key not configured. Run this script without -Check to connect.'
            exit 2
        }
        $secret = Get-Content -LiteralPath $keyPath -Raw | ConvertTo-SecureString
    } else {
        $secret = Read-Host 'Paste your Meshy API key (hidden)' -AsSecureString
    }
    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
    try { $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer).Trim() }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
    if ([string]::IsNullOrWhiteSpace($plain)) { throw 'Empty key' }
    $headers = @{ Authorization = 'Bearer ' + $plain }
    $balance = Invoke-RestMethod -Uri 'https://api.meshy.ai/openapi/v1/balance' -Headers $headers -Method Get -TimeoutSec 30 -MaximumRedirection 0
    if ($null -eq $balance.balance) { throw 'Missing balance' }
    if (-not $Check) {
        New-Item -ItemType Directory -Path $keyDirectory -Force | Out-Null
        $normalized = ConvertTo-SecureString $plain -AsPlainText -Force
        try { $normalized | ConvertFrom-SecureString | Set-Content -LiteralPath $keyPath -Encoding ASCII }
        finally { $normalized.Dispose() }
    }
    Write-Host ('Meshy connected. Available API credits: ' + $balance.balance)
    if (-not $Check) { Write-Host 'Key saved outside the project, encrypted for your Windows account.' }
} catch {
    # Avoid printing exception/request objects that might contain authorization data.
    Write-Host 'Meshy connection failed. Check your API key, API access and network connection. No new key was saved.'
    exit 1
} finally {
    $plain = $null
    if ($null -ne $headers) { $headers.Clear() }
    if ($null -ne $secret) { $secret.Dispose() }
}
