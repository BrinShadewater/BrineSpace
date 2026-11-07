extends SceneTree
## Native strategy fixture with explicit rooms/cards; not paid-expedition evidence.
const Player=preload("res://tests/playtest_procedural_expedition.gd")
var failures:=0
func _init(): call_deferred("run")
func check(ok: bool,label: String):
	if not ok: failures+=1;push_error(label)
func run():
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://player_recipe_%d.meta"%OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	game.set_meta("site_seed",73)
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.Preferences.pause_unfocused=false
	game._set_paused(false,false)
	game.selected_rotation=0
	game._place_room("solar_array",Vector2i(21,20),true)
	game._place_room("mining_drone_bay",Vector2i(21,21),true)
	game._place_room("hydroponics_bay",Vector2i(20,21),true)
	game.resources.metal=30
	game.resources.rare_minerals=1
	var player=Player.new(false)
	player.game=game;player.all_crew=true
	player.out="res://output/procedural-sites-2026-09-23/recipe-strategy/"
	DirAccess.make_dir_recursive_absolute(player.out)
	game.meta.discovered_synergy_ids.erase("industrial_heat_capture")
	check(player.planned_reactor_cell()==Vector2i(-1,-1),"Unknown recipe does not influence placement")
	game.meta.discovered_synergy_ids["industrial_heat_capture"]=true
	var target: Vector2i=player.planned_reactor_cell()
	check(target==Vector2i(21,22),"Known recipe reserves a matching-door reactor neighbor of the mining bay")
	game.hand=["current_turbine"]
	player.choose_build(100)
	check(not game.drone_fleet.orders.is_empty(),"Turbine can build while preserving the recipe")
	for order in game.drone_fleet.orders:
		check(order.pos!=target and game._turbine_intake_cell(order)!=target,"Turbine and its intake leave the planned reactor cell free")
	game.drone_fleet.orders.clear()
	game.hand=["reactor"]
	player.choose_build(200)
	check(game.drone_fleet.orders.any(func(order):return order.id=="reactor" and order.pos==target),"Actual player places the reactor beside the mining bay")
	game._set_time_speed(2)
	var deadline:=Time.get_ticks_msec()+60000
	while Time.get_ticks_msec()<deadline and game.running and not game.active_synergies.has("industrial_heat_capture"):
		await process_frame
		if game.crew_comms.panel.visible: game.crew_comms.advance()
		elif game.paused: game._set_paused(false,false)
	check(game.active_synergies.has("industrial_heat_capture"),"Normal simulation activates the learned recipe")
	check(player.planned_reactor_cell()==Vector2i(-1,-1),"Completed reactor releases the planning reservation")
	player.free()
	print("PROCEDURAL PLAYER RECIPE: failures=",failures," active=",game.active_synergies.has("industrial_heat_capture"))
	quit(0 if failures==0 else 1)
