extends SceneTree
## The Room Layout Studio has an ocean behind the room (owner playtest, Sept 29): a node of its own behind the
## canvas, switchable, drifting only when motion and effects allow it.
const Editor = preload("res://scripts/room_layout_editor.gd")
const Store = preload("res://scripts/room_layout_store.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _init() -> void: call_deferred("run")

func run() -> void:
	root.size = Vector2i(1600, 900)
	Store.path = "user://studio_ocean_layouts.json"
	Store.defaults_path = "user://studio_ocean_defaults.json"
	Store.loaded = true
	Store.data = {}
	TitleSettings.reduced_motion = false
	TitleSettings.effects_quality = 1
	var editor = Editor.open(root)
	editor.autosave_enabled = false
	await process_frame
	await process_frame
	var ocean = editor.ocean_backdrop
	expect(ocean != null and ocean.get_parent() == editor.canvas, "The ocean is a child of the canvas")
	expect(ocean.show_behind_parent, "It draws behind the room canvas")
	expect(editor.ocean_on and ocean.visible, "It is on by default")
	expect(ocean.animated(), "It drifts at Medium with motion allowed")
	var before: float = ocean.clock
	ocean._process(0.2)
	expect(ocean.clock > before, "Its clock advances")
	TitleSettings.reduced_motion = true
	expect(not ocean.animated(), "Reduced Motion holds it still")
	TitleSettings.reduced_motion = false
	TitleSettings.effects_quality = 0
	expect(not ocean.animated(), "Low quality holds it still")
	TitleSettings.effects_quality = 1
	editor.ocean_toggle.button_pressed = false
	expect(not editor.ocean_on and not ocean.visible and not ocean.animated(), "The toggle turns it off")
	editor.ocean_toggle.button_pressed = true
	expect(editor.ocean_on and ocean.visible, "And back on")
	print("STUDIO OCEAN: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
