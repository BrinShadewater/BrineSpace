$ErrorActionPreference = 'Stop'
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$source = Get-Content -LiteralPath (Join-Path $workspace 'tests/test_menu_recovery.gd') -Raw
$adapter = @'
extends Node
# Generated from test_menu_recovery.gd by tools/build_menu_export_fixture.ps1.
var root: Window:
	get: return get_tree().root
var current_scene: Node:
	get: return get_tree().current_scene
	set(value): get_tree().current_scene = value
var process_frame: Signal:
	get: return get_tree().process_frame
func create_timer(seconds: float) -> SceneTreeTimer:
	return get_tree().create_timer(seconds)
func quit(code: int) -> void:
	get_tree().quit(code)
'@
$source = $source.Replace('extends SceneTree', $adapter).Replace('func _init() -> void:', 'func _ready() -> void:')
$destination = Join-Path $workspace 'tests/runtime_generated'
New-Item -ItemType Directory -Path $destination -Force | Out-Null
[IO.File]::WriteAllText((Join-Path $destination 'menu_recovery.gd'), $source)
$scene = @'
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://tests/runtime_generated/menu_recovery.gd" id="1"]

[node name="MenuRecoveryValidation" type="Node"]
script = ExtResource("1")
'@
[IO.File]::WriteAllText((Join-Path $destination 'menu_recovery.tscn'), $scene)
