extends Node
const FIXTURES = {
	"station": preload("res://tests/runtime_generated/station.gd"),
	"cryo_chamber": preload("res://tests/runtime_generated/cryo_chamber.gd"),
	"clone_lab": preload("res://tests/runtime_generated/clone_lab.gd"),
	"data_archive": preload("res://tests/runtime_generated/data_archive.gd"),
	"biodome": preload("res://tests/runtime_generated/biodome.gd"),
	"xeno_lab": preload("res://tests/runtime_generated/xeno_lab.gd"),
	"anomaly_lab": preload("res://tests/runtime_generated/anomaly_lab.gd"),
	"bio_lab": preload("res://tests/runtime_generated/bio_lab.gd"),
	"holographic_core": preload("res://tests/runtime_generated/holographic_core.gd"),
	"med_center": preload("res://tests/runtime_generated/med_center.gd"),
	"med_office": preload("res://tests/runtime_generated/med_office.gd"),
	"med_bay": preload("res://tests/runtime_generated/med_bay.gd"),
	"reactor": preload("res://tests/runtime_generated/reactor.gd"),
	"reactor_effects": preload("res://tests/runtime_generated/reactor_effects.gd"),
	"reactor_lighting": preload("res://tests/runtime_generated/reactor_lighting.gd"),
	"mining_drone_bay": preload("res://tests/runtime_generated/mining_drone_bay.gd"),
	"salvage_drone_bay": preload("res://tests/runtime_generated/salvage_drone_bay.gd"),
	"airlock": preload("res://tests/runtime_generated/airlock.gd"),
}
func _ready() -> void:
	var subject := "station"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--room-fixture="): subject = arg.trim_prefix("--room-fixture=")
	if not FIXTURES.has(subject):
		push_error("Unknown exported room fixture: " + subject)
		get_tree().quit(1)
		return
	add_child(FIXTURES[subject].new())
