extends SceneTree
## Native strategy fixture; explicit room/resource/hand setup, not paid-run evidence.
const Player=preload("res://tests/playtest_procedural_expedition.gd")
var failures:=0
func _init(): call_deferred("run")
func check(ok: bool,label: String):
	if not ok: failures+=1;push_error(label)
func run():
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://player_power_%d.meta"%OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	game.set_meta("site_seed",73)
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.Preferences.pause_unfocused=false
	game._set_paused(false,false)
	game.selected_rotation=3
	game._place_room("current_turbine",Vector2i(20,21),true)
	game.occupied[Vector2i(20,21)].rotation=3
	var turbine: Dictionary=game.occupied[Vector2i(20,21)]
	check(game._turbine_intake_clear(turbine),"Fixture starts with a clear working intake")
	var player=Player.new(false)
	player.game=game;player.all_crew=true
	player.out="res://output/procedural-sites-2026-09-23/power-strategy/"
	DirAccess.make_dir_recursive_absolute(player.out)
	game.resources.metal=20
	game.hand=["solar_array"]
	player.choose_build(100)
	check(game.drone_fleet.orders.any(func(order):return order.id=="solar_array"),"Solar construction still finds a legal route")
	check(not game.drone_fleet.orders.any(func(order):return order.pos==game._turbine_intake_cell(turbine)),"New construction preserves the existing turbine intake")
	game.drone_fleet.orders.clear() # Reset explicit fixture setup before the independent reroll case.
	game.resources.metal=0;game.resources.power=0
	game.hand=["reactor","quarantine_cell","research_lab"]
	game.rerolls_remaining=1
	player.choose_build(200)
	check(game.hand.has("reactor"),"Retain needed reactor while it is unaffordable")
	check(player.events[-1].kind=="reroll" and player.events[-1].id=="quarantine_cell","Unaffordable support does not freeze unrelated rerolls")
	player.free()
	print("PROCEDURAL PLAYER POWER: failures=",failures)
	quit(0 if failures==0 else 1)
