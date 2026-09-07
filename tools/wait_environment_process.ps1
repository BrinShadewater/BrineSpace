function Wait-EnvironmentProcess {
    param(
        [Parameter(Mandatory=$true)][System.Diagnostics.Process]$Process,
        [Parameter(Mandatory=$true)][string]$ExpectedExecutable,
        [Parameter(Mandatory=$true)][string]$LogPath,
        [ValidateRange(1,3600)][int]$TimeoutSeconds = 600
    )
    $expectedPath = [System.IO.Path]::GetFullPath($ExpectedExecutable)
    $timer = [System.Diagnostics.Stopwatch]::StartNew()
    $failure = $null
    while (-not $Process.WaitForExit(500)) {
        if ((Test-Path -LiteralPath $LogPath) -and
            (Select-String -LiteralPath $LogPath -Pattern 'SCRIPT ERROR:|ERROR:' -Quiet)) {
            $failure = "Environment process reported an error; inspect $LogPath"
        } elseif ($timer.Elapsed.TotalSeconds -ge $TimeoutSeconds) {
            $failure = "Environment process exceeded $TimeoutSeconds seconds; inspect $LogPath"
        }
        if ($failure) {
            if (-not $Process.HasExited) {
                if ([System.IO.Path]::GetFullPath($Process.Path) -ne $expectedPath) {
                    throw 'Process path changed; refusing to terminate an unverified executable'
                }
                $Process.Kill()
                $Process.WaitForExit()
            }
            throw $failure
        }
    }
    # Include errors emitted immediately before normal process exit.
    if ($Process.ExitCode -ne 0 -or ((Test-Path -LiteralPath $LogPath) -and
        (Select-String -LiteralPath $LogPath -Pattern 'SCRIPT ERROR:|ERROR:' -Quiet))) {
        throw "Environment process failed; inspect $LogPath"
    }
}
