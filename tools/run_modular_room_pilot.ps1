param(
    [Parameter(Mandatory = $true)][string]$Godot,
    [switch]$Test
)
$ErrorActionPreference = 'Stop'
$pilotRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$pilotExecutable = (Resolve-Path -LiteralPath $Godot).Path
$pilotArguments = @('--path', $pilotRoot, '--script', 'res://tools/modular_room_pilot.gd')
if ($Test) { $pilotArguments = @('--headless') + $pilotArguments + @('--', '--test') }
& $pilotExecutable @pilotArguments
