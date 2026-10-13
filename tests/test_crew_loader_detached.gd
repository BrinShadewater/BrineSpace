extends SceneTree
# Fixtures call the crew loaders on a grid that never enters the scene tree, in either
# order and on several grids. The game loads from the grid's _ready, inside the tree,
# and that path must keep one storage session per grid.
const Router := preload("res://scripts/crew_storage/router.gd")
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(why)
func _init() -> void: call_deferred("run")
func run() -> void:
	check(OS.get_user_data_dir().replace("\\", "/").begins_with(OS.get_environment("APPDATA").replace("\\", "/") + "/"), "Scratch profile")
	if failures: quit(1); return

	# The game path: a session owned by the grid, closed when the grid leaves.
	check(Router.active == null, "No session before the game loads")
	var game = load("res://scenes/main.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	await process_frame
	check(Router.active != null and Router.active.tree == self, "Game grid starts its session on the scene tree")
	var game_bank = Router.active.bank if Router.active != null else null
	check(game_bank != null and game_bank.sources.size() > 0, "Game session holds crew frames")
	check(game.grid_view.human_water_player.frames.has("walk-south") and game.grid_view.veld_player != null and game.grid_view.branforth_player != null, "Game grid loaded Bill, Veld and Branforth")
	game.queue_free()
	await process_frame
	await process_frame
	check(Router.active == null, "Game session closes with its grid")

	# Bill first, the order most fixtures use.
	var first = load("res://scripts/grid_canvas.gd").new()
	first._load_major_bill_animations()
	check(Router.active != null, "Detached Bill load opens a session")
	check(first.human_water_player != null and first.human_water_player.frames.has("walk-south"), "Detached Bill load fills the player")
	var shared = Router.active.bank if Router.active != null else null
	check(shared != game_bank, "Detached session does not reuse the closed game bank")
	var bill_sources: int = shared.sources.size() if shared != null else 0
	first._load_replacement_crew_animations()
	check(Router.active != null and Router.active.bank == shared, "Detached crew load joins the same session")
	check(first.veld_player != null and first.branforth_player != null and first.marsh_player != null, "Detached crew load fills Veld, Branforth and Marsh")
	check(shared != null and shared.sources.size() > bill_sources, "Crew frames join the shared bank")
	var bill_frame: Texture2D = first.human_water_player.frames["walk-south"][0]
	check(shared != null and shared.sources.has(bill_frame.get_instance_id()) and shared.source_image(bill_frame) != null, "Bill frames stay readable after the crew load")

	# Crew first, on a second grid in the same process.
	var second = load("res://scripts/grid_canvas.gd").new()
	second._load_replacement_crew_animations()
	second._load_major_bill_animations()
	check(second.veld_player != null and second.veld_player.frames.size() > 12, "Second detached grid loads Veld")
	check(second.human_water_player != null and second.human_water_player.frames.has("walk-south"), "Second detached grid loads Bill")
	var veld_frame: Texture2D = second.veld_player.frames.values()[0][0]
	check(Router.active != null and Router.active.bank.source_image(veld_frame) != null, "Second grid's frames are readable")
	first.free(); second.free()
	print("CREW LOADER DETACHED: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
