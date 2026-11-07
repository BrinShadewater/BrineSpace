extends SceneTree
## The whale passes over the station, not under it (owner playtest, Sept 29): its pass is drawn after every
## surface pass, and the water-level life pass no longer draws it.
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	TitleSettings.save_path = "user://life_over_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://life_over_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://life_over_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	var grid = game.grid_view
	expect(grid.life_over != null and is_instance_valid(grid.life_over), "The over-station life pass exists")
	var last_surface: int = -1
	for layer in grid.surface_passes: last_surface = maxi(last_surface, layer.get_index())
	expect(grid.life_over.get_index() > last_surface, "It is drawn after every surface pass")
	expect(grid.life_over.get_index() > grid.env_passes[grid.Env.LIFE].get_index(), "It is drawn after the water-level life pass")
	var source := FileAccess.get_file_as_string("res://scripts/ocean_life.gd")
	var draw_body := source.substr(source.find("static func draw(canvas"), source.find("static func draw_over") - source.find("static func draw(canvas"))
	expect(not draw_body.contains("_draw_whale"), "The water-level pass does not draw the whale")
	expect(source.contains("static func draw_over") and source.substr(source.find("static func draw_over")).contains("_draw_whale"), "The over-station pass draws the whale")
	print("LIFE OVER STATION: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
