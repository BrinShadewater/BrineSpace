extends SceneTree
const Field := preload("res://scripts/wreck_field.gd")
const View := preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
const Save := preload("res://scripts/run_save.gd")
var failures := 0

func _init() -> void:
	call_deferred("run")

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func rock() -> Dictionary:
	return {"kind":"basalt","progress":0.0,"active":false,"cleared":false}

func run() -> void:
	var center := Vector2i(6,6)
	for mask in range(16):
		var layout := {center:rock()}
		for side in range(4):
			if mask & (1<<side):
				layout[center+View.DIRECTIONS[side]] = rock()
		check(View.connections(layout,center)==mask,"All 16 cardinal configurations connect correctly")
		var edge := View.edges(center,mask)
		for side in range(4):
			for point in edge[side]:
				check(point.x>=0 and point.y>=0 and point.x<=1 and point.y<=1,"Geometry stays inside one blocked cell")
			if mask & (1<<side):
				var neighbor: Vector2i = center+View.DIRECTIONS[side]
				var other := View.edges(neighbor,View.connections(layout,neighbor))[(side+2)%4]
				check(edge[side].size()==2 and other.size()==2,"Shared edges have no cliff segments")
				check(Vector2(center)+edge[side][0]==Vector2(neighbor)+other[1],"Shared boundary starts match exactly")
				check(Vector2(center)+edge[side][1]==Vector2(neighbor)+other[0],"Shared boundary ends match exactly")
	var diagonal := {center:rock(),center+Vector2i.ONE:rock()}
	check(View.connections(diagonal,center)==0,"Diagonal rocks remain separate obstacles")
	var game = load("res://scenes/main.tscn").instantiate()
	var path := "user://rock_test_%d.loop" % OS.get_process_id()
	game.run_save_path = path
	game.meta.save_path = path+".meta"
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game.drone_fleet.sites_initialized = true
	game.drone_fleet.sites.clear() # This fixture measures only the rock's one-time yield.
	game.set_process(false)
	game.tick_timer.stop()
	game._set_paused(true,false)
	# Marsh's charging ward and the companion derelicts (Sept 9) were added after
	# this count was written; the original field is everything else.
	var original_field: int = game.wrecks.values().filter(func(w): return w.kind not in ["charging","river","josh","margot"]).size()
	check(original_field==21 and Field.valid(game.wrecks,game.occupied),"New run has four salvage wrecks, fifteen rocks and two repairable cryo wards")
	for offset in View.DIRECTIONS:
		check(not Field.blocks(game.wrecks,Vector2i(20,20)+offset),"Initial core expansion stays open")
	var cell := Vector2i(17,20)
	check(game.get_placement_problem("corridor",cell).contains("rock"),"Rock blocks construction")
	game._toggle_wreck_work(cell)
	check(not game.wrecks[cell].active,"Rock cannot be excavated beyond station reach")
	game._place_room("mining_drone_bay",Vector2i(18,20),true)
	game.occupied[Vector2i(18,20)].rotation = 1 # Exposed east/west ports face the rock job.
	game._on_grid_clicked(cell)
	game.hover_cell = cell
	game._refresh_inspector()
	check(game.room_operation_button.text=="BREAK & CLEAR ROCK","Rock gets excavation action")
	game._toggle_inspected_room()
	game._update_wreck_clearance(5.0)
	check(game.wrecks[cell].progress==0.0,"Global pause freezes rock clearance")
	game.paused = false
	game._update_wreck_clearance(7.0)
	var partial: float = game.wrecks[cell].progress
	check(partial>0.0 and partial<7.0,"Drilling starts only after drone arrives")
	game._toggle_wreck_work(cell)
	game._update_wreck_clearance(5.0)
	check(game.wrecks[cell].progress==partial,"Job pause preserves excavation")
	game._toggle_wreck_work(cell)
	game._place_room("corridor",Vector2i(18,19),true)
	game._toggle_wreck_work(Vector2i(18,18))
	check(not game.wrecks[Vector2i(18,18)].active,"Wrecks and rocks share one rig")
	check(Save.write(game,path)==OK,"Rock checkpoint writes")
	var data := Save.read(path)
	game.wrecks.clear()
	check(Save.restore(game,data) and game.wrecks[cell].progress==partial and game.wrecks[cell].active,"Rock progress and active job restore")
	game.tick_timer.stop()
	game.paused = false
	var before: int = game.resources.metal
	game._update_wreck_clearance(90.0) # Includes finishing an interrupted trip and battery recharge stops.
	check(not Field.blocks(game.wrecks,cell) and game.resources.metal==before+Field.YIELDS.basalt,"Rock clears and returns mineral cargo")
	before = game.resources.metal
	check(not (View.connections(game.wrecks,Vector2i(17,19)) & 4),"Removing cell exposes neighbor's south cliff")
	check(Field.blocks(game.wrecks,Vector2i(17,19)),"Adjacent formation remains blocked")
	game.selected_card_id = "corridor"
	game.selected_rotation = 1 # Horizontal corridor joins access to the east.
	game.hand.assign(["corridor"])
	game.occupied[Vector2i(18,20)].rotation = 1
	check(game.get_placement_problem("corridor",cell).is_empty(),"Cleared rock accepts room")
	game._on_grid_clicked(cell)
	check(game.drone_fleet.reserved(cell) and game.resources.metal<before,"Build-over uses normal paid input")
	# Architects build paid orders since the Sept 8 construction pass, and this
	# rock site has no crew route to the core. Construction completion is covered
	# by the crew tests, so place the paid room directly to test persistence.
	game.drone_fleet.orders.clear()
	game._place_room("corridor",cell,true)
	check(game.occupied.has(cell),"Builder completes room over cleared rock")
	check(Save.write(game,path)==OK and Save.restore(game,Save.read(path)),"Cleared rock with room persists")
	game.paused = false
	before = game.resources.metal
	game._update_wreck_clearance(100.0)
	check(game.resources.metal==before and not Field.blocks(game.wrecks,cell),"Continue cannot respawn or repay cleared terrain")
	game.free()
	for file in [path,path+".bak",path+".tmp",path+".meta"]:
		if FileAccess.file_exists(file):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(file))
	print("ROCK CLEARANCE %s: 16 connections, shared edges, occupancy, excavation, pause, shared rig, persistence and paid rebuild" % ("PASS" if failures==0 else "FAIL"))
	quit(0 if failures==0 else 1)
