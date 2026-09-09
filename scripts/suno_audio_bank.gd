extends RefCounted
## Explicit dependencies keep audio in selected-resource exports.
const CLIPS := {
	"moonlit_canyon": [preload("res://assets/audio/suno-v1/moonlit_canyon_01.ogg"), preload("res://assets/audio/suno-v1/moonlit_canyon_02.ogg")],
	"moonlit_test_run": [preload("res://assets/audio/suno-v1/moonlit_test_run_01.ogg"), preload("res://assets/audio/suno-v1/moonlit_test_run_02.ogg")],
	"interior": [preload("res://assets/audio/suno-v1/interior_01.ogg"), preload("res://assets/audio/suno-v1/interior_02.ogg")],
	"ocean": [preload("res://assets/audio/suno-v1/ocean_01.ogg"), preload("res://assets/audio/suno-v1/ocean_02.ogg")],
	"placement": [preload("res://assets/audio/suno-polish-v1/placement_01.wav"), preload("res://assets/audio/suno-polish-v1/placement_02.wav"), preload("res://assets/audio/suno-polish-v1/placement_03.wav"), preload("res://assets/audio/suno-polish-v1/placement_04.wav")],
	"power_on": [preload("res://assets/audio/suno-polish-v1/power_on_01.wav"), preload("res://assets/audio/suno-polish-v1/power_on_02.wav")],
	"door": [preload("res://assets/audio/suno-polish-v1/door_01.wav"), preload("res://assets/audio/suno-polish-v1/door_02.wav")],
	"airlock": [preload("res://assets/audio/suno-v1/airlock_01.ogg"), preload("res://assets/audio/suno-v1/airlock_02.ogg")],
	"drone": [preload("res://assets/audio/suno-v1/drone_01.ogg"), preload("res://assets/audio/suno-v1/drone_02.ogg")],
	"cargo": [preload("res://assets/audio/suno-polish-v1/cargo_01.wav"), preload("res://assets/audio/suno-polish-v1/cargo_02.wav")],
	"terminal": [preload("res://assets/audio/suno-polish-v1/terminal_01.wav"), preload("res://assets/audio/suno-polish-v1/terminal_02.wav")],
	"discovery": [preload("res://assets/audio/suno-polish-v1/discovery_01.wav"), preload("res://assets/audio/suno-polish-v1/discovery_02.wav")],
	"warning": [preload("res://assets/audio/suno-polish-v1/warning_01.wav")],
}
