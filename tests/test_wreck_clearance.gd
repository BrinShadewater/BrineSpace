extends SceneTree
const Field := preload("res://scripts/wreck_field.gd")
const Save := preload("res://scripts/run_save.gd")
var game
var failures := 0
var save_path := ""

func _init() -> void:
	call_deferred("run")

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func run() -> void:
	game = load("res://scenes/main.tscn").instantiate()
	save_path = "user://wreck_test_%d.loop" % OS.get_process_id()
	game.run_save_path = save_path
	game.meta.save_path = save_path+".meta"
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game.drone_fleet.sites_initialized = true
	game.drone_fleet.sites.clear() # This fixture measures only the wreck's one-time yield.
	game.set_process(false)
	game.tick_timer.stop()
	game._set_paused(true,false)
	var wreck_count := 0
	for obstacle in game.wrecks.values():
		wreck_count += int(Field.TYPES.has(obstacle.kind))
	check(wreck_count==4,"Four distinct wrecks seed a new run alongside terrain")
	check(Field.valid(game.wrecks,game.occupied),"Initial wrecks do not overlap station rooms")
	var cell := Vector2i(18,18)
	check(game.get_placement_problem("corridor",cell).contains("wreckage"),"Wreck blocks paid placement")
	game._toggle_wreck_work(cell)
	check(not game.wrecks[cell].active,"Cannot salvage beyond adjacent station reach")
	game._place_room("salvage_drone_bay",Vector2i(18,19),true) # Fixture bay/access; normal runs still pay.
	game._on_grid_clicked(cell)
	check(game.selected_room_cell==cell and game.selected_card_id.is_empty(),"Click selects wreck")
	game.hover_cell = cell
	game._refresh_inspector()
	game._toggle_inspected_room()
	check(game.wrecks[cell].active,"Inspector starts dismantling")
	game._update_wreck_clearance(5.0)
	check(game.wrecks[cell].progress==0.0,"Global pause freezes clearance")
	game.paused = false
	game._update_wreck_clearance(8.0)
	var partial: float = game.wrecks[cell].progress
	check(partial>0.0 and partial<8.0 and Field.blocks(game.wrecks,cell),"Partial progress remains blocked")
	game._toggle_wreck_work(cell)
	game._update_wreck_clearance(4.0)
	check(game.wrecks[cell].progress==partial,"Individual pause retains cuts")
	game._toggle_wreck_work(cell)
	game._place_room("corridor",Vector2i(22,19),true)
	game._toggle_wreck_work(Vector2i(22,18))
	check(not game.wrecks[Vector2i(22,18)].active,"Only one basic rig can work")
	check(Save.write(game,save_path)==OK,"Active salvage writes a real isolated checkpoint")
	var checkpoint := Save.read(save_path)
	check(not checkpoint.is_empty(),"Active salvage checkpoint validates")
	game.wrecks.clear()
	check(Save.restore(game,checkpoint),"Restore salvage checkpoint")
	check(game.wrecks[cell].progress==partial and game.wrecks[cell].active and game.paused,"Progress, job assignment and paused Continue survive")
	game.tick_timer.stop()
	var legacy: Dictionary = checkpoint.duplicate(true)
	legacy.erase("wrecks")
	legacy.erase("architects")
	check(Save.restore(game,legacy) and game.wrecks.is_empty(),"Legacy checkpoint never gains new obstacles")
	check(Save.restore(game,checkpoint),"Restore new checkpoint after legacy check")
	game.tick_timer.stop()
	var invalid: Dictionary = checkpoint.duplicate(true)
	invalid.wrecks[cell].progress = NAN
	check(not Save.restore(game,invalid),"Reject non-finite progress before mutation")
	game.paused = false
	var metal_before: int = game.resources.metal
	game._update_wreck_clearance(90.0) # Includes finishing an interrupted trip and battery recharge stops.
	check(not Field.blocks(game.wrecks,cell),"Completion releases footprint")
	check(game.resources.metal==metal_before+Field.YIELDS.engineering,"Completion awards salvage once")
	metal_before = game.resources.metal
	game._update_wreck_clearance(100.0)
	check(game.resources.metal==metal_before,"No duplicate salvage after completion")
	game.selected_card_id = "corridor"
	game.selected_rotation = 0
	game.hand.assign(["corridor"])
	check(game.get_placement_problem("corridor",cell).is_empty(),"Cleared footprint accepts connected room")
	var cost: int = game.RoomDatabaseScript.get_room("corridor").cost.metal
	game._on_grid_clicked(cell)
	check(game.drone_fleet.reserved(cell),"Normal input reserves cleared wreck for paid construction")
	game._update_wreck_clearance(30.0)
	check(game.occupied.has(cell),"Construction drone completes build over cleared wreck")
	check(game.resources.metal==metal_before-cost,"Build-over spends normal metal cost")
	check(Save.write(game,save_path)==OK and not Save.read(save_path).is_empty(),"Cleared wreck plus new room persists")
	var after_build := Save.read(save_path)
	check(Save.restore(game,after_build),"Built-over checkpoint restores")
	game.paused = false
	metal_before = game.resources.metal
	game._update_wreck_clearance(100.0)
	check(game.resources.metal==metal_before,"Continue cannot repay cleared wreck")
	var meta_path: String = game.meta.save_path
	game.free()
	for path in [save_path,save_path+".bak",save_path+".tmp",meta_path]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	print("WRECK CLEARANCE %s: occupancy, reach, one job, global/job pause, save/legacy/validation, once-only salvage and paid rebuild" % ("PASS" if failures==0 else "FAIL"))
	quit(0 if failures==0 else 1)
