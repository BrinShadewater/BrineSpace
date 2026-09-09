extends RefCounted
## Measured constant gains; rebuild with tools/polish_suno_audio.py.
const GAIN_DB := {
	"res://assets/audio/suno-v1/moonlit_canyon_01.ogg": -0.68,
	"res://assets/audio/suno-v1/moonlit_canyon_02.ogg": -1.02,
	"res://assets/audio/suno-v1/moonlit_test_run_01.ogg": -5.1,
	"res://assets/audio/suno-v1/moonlit_test_run_02.ogg": -3.58,
	"res://assets/audio/suno-v1/interior_01.ogg": -2.67,
	"res://assets/audio/suno-v1/interior_02.ogg": -1.54,
	"res://assets/audio/suno-v1/ocean_01.ogg": -2.43,
	"res://assets/audio/suno-v1/ocean_02.ogg": -1.5,
	"res://assets/audio/suno-polish-v1/placement_01.wav": -2.75,
	"res://assets/audio/suno-polish-v1/placement_02.wav": -1.68,
	"res://assets/audio/suno-polish-v1/placement_03.wav": -0.45,
	"res://assets/audio/suno-polish-v1/placement_04.wav": 0.99,
	"res://assets/audio/suno-polish-v1/power_on_01.wav": -5.64,
	"res://assets/audio/suno-polish-v1/power_on_02.wav": -10.39,
	"res://assets/audio/suno-polish-v1/door_01.wav": -7.33,
	"res://assets/audio/suno-polish-v1/door_02.wav": -1.04,
	"res://assets/audio/suno-v1/airlock_01.ogg": -0.36,
	"res://assets/audio/suno-v1/airlock_02.ogg": -10.61,
	"res://assets/audio/suno-v1/drone_01.ogg": -3.92,
	"res://assets/audio/suno-v1/drone_02.ogg": -1.86,
	"res://assets/audio/suno-polish-v1/cargo_01.wav": -4.03,
	"res://assets/audio/suno-polish-v1/cargo_02.wav": -2.41,
	"res://assets/audio/suno-polish-v1/terminal_01.wav": 2.61,
	"res://assets/audio/suno-polish-v1/terminal_02.wav": -9.08,
	"res://assets/audio/suno-polish-v1/discovery_01.wav": -6.46,
	"res://assets/audio/suno-polish-v1/discovery_02.wav": -10.43,
	"res://assets/audio/suno-polish-v1/warning_01.wav": -8.96,
}

static func gain(stream: AudioStream) -> float:
	return float(GAIN_DB.get(stream.resource_path, 0.0))
