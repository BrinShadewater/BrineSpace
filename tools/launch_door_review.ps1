param([string]$GodotPath = 'C:/Users/Alex/Desktop/Projects/Godot_v4.6.1-stable_win64.exe')
$reviewRoot = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path -LiteralPath $GodotPath)) {
    throw 'Supply the Godot 4.6 executable using -GodotPath.'
}
# Intentionally visible: this launcher opens the owner-operated review station.
Start-Process -FilePath $GodotPath -WorkingDirectory $reviewRoot -ArgumentList '--path "." --script res://tests/door_review_station.gd'
