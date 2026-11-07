extends SceneTree
## Direct native fixture: supplied hand, owned blueprint and five-Metal boundary state.
## This is not a fresh dealt-hand paid expedition.
const Save=preload("res://scripts/run_save.gd")
const Player=preload("res://tests/playtest_procedural_expedition.gd")
const OUT="res://output/procedural-sites-2026-09-23/"
var failures := 0
func _init(): call_deferred("run")
func check(ok: bool, label: String):
	if not ok: failures+=1;push_error(label)
func run():
	var saved:=Save.read(OUT+"expedition-73-fresh-rescue-berths/final.loop")
	if saved.is_empty(): push_error("Requires recorded depleted-mining checkpoint");quit(1);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://salvage_strategy_%d.meta"%OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	Save.pending=saved
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.Preferences.pause_unfocused=false
	game.crew_comms.minimize()
	game._set_paused(false,false)
	var player=Player.new(false)
	player.game=game;player.all_crew=true;player.recovered=true
	player.out=OUT+"salvage-strategy/"
	DirAccess.make_dir_recursive_absolute(player.out)
	var cost: int=game.RoomDatabaseScript.get_room("salvage_drone_bay").cost.get("metal",0)
	game.resources.metal=cost
	game.hand=["life_support"]
	game.meta.unlocked_room_ids.erase("salvage_drone_bay")
	check(player.salvage_reserve()==0,"Never reserve metal for a locked blueprint")
	game.meta.unlocked_room_ids["salvage_drone_bay"]=true # Owned-profile fixture setup.
	check(player.salvage_reserve()==cost,"Exhausted mining with known scrap reserves a first salvage bay")
	player.choose_build(100)
	check(game.resources.metal==cost and game.drone_fleet.orders.is_empty(),"Nonessential construction cannot spend the salvage reserve")
	game.hand=["salvage_drone_bay"]
	player.choose_build(200)
	check(game.resources.metal==0,"First salvage bay spends its normal metal cost")
	check(game.drone_fleet.orders.any(func(order):return order.id=="salvage_drone_bay"),"Salvage bay queues through normal placement")
	check(not game.testing_free_build and not game.testing_disable_failures,"Normal costs and failure rules")
	game._set_time_speed(2)
	var deadline:=Time.get_ticks_msec()+90000
	while Time.get_ticks_msec()<deadline and game.running and int(game.resources.metal)==0:
		await process_frame
		if game.crew_comms.panel.visible: game.crew_comms.advance()
		elif game.paused: game._set_paused(false,false)
	check(int(game.resources.metal)>0,"Surveyed scrap restores metal income after the bay completes")
	check(player.salvage_reserve()==0,"Existing salvage worker releases reserve")
	game._set_paused(true,false)
	check(Save.write(game,player.out+"income-restored.loop")==OK,"Income-restored fixture saves")
	player.free()
	print("PROCEDURAL SALVAGE STRATEGY: failures=",failures," metal=",game.resources.metal)
	quit(0 if failures==0 else 1)
