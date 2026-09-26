extends SceneTree
## Run directly: native strategy regression using a paid-run checkpoint; injected hands are
## fixture setup, so this is not reported as a fresh dealt-hand expedition.
const Save=preload("res://scripts/run_save.gd")
const Player=preload("res://tests/playtest_procedural_expedition.gd")
const OUT="res://output/procedural-sites-2026-09-23/"
var failures := 0
func _init(): call_deferred("run")
func check(ok: bool, label: String):
	if not ok: failures+=1;push_error(label)
func run():
	var saved:=Save.read(OUT+"expedition-73-fresh-door-routes/final.loop")
	if saved.is_empty(): push_error("Requires the recorded seed-73 paid checkpoint");quit(1);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://berth_strategy_%d.meta"%OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	Save.pending=saved
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.Preferences.pause_unfocused=false
	game.crew_comms.minimize()
	game._set_paused(false,false)
	var player=Player.new(false)
	player.game=game;player.all_crew=true;player.recovered=true
	player.out=OUT+"berth-strategy/"
	DirAccess.make_dir_recursive_absolute(player.out)
	game.hand=["crew_hab","crew_hab","research_lab"]
	game.resources.food=1
	game.rerolls_remaining=1
	player.choose_build(100)
	check(not player.events.is_empty() and player.events[-1].kind=="reroll" and player.events[-1].id=="crew_hab","Duplicate Hab can be rerolled while one needed Hab is retained")
	check(game.hand.has("crew_hab"),"Retain a Hab for the pending rescue")
	check(Save.restore(game,saved),"Restore untouched checkpoint for paid construction")
	game.crew_comms.minimize()
	game.hand=["crew_hab"]
	game._set_paused(false,false)
	var metal: int=game.resources.metal
	var cost: int=game.RoomDatabaseScript.get_room("crew_hab").cost.get("metal",0)
	player.choose_build(200)
	check(not game.testing_free_build and not game.testing_disable_failures,"Normal cost and failure rules")
	check(game.drone_fleet.orders.any(func(order):return order.id=="crew_hab"),"Completed chamber routes do not block Hab construction")
	check(game.resources.metal==metal-cost,"Hab spends its normal metal cost")
	game._set_time_speed(2)
	var deadline:=Time.get_ticks_msec()+90000
	while Time.get_ticks_msec()<deadline and game.running and not game.recovered_crew.any(func(member):return member.get("architect_id","")=="marsh"):
		await process_frame
		if game.crew_comms.panel.visible: game.crew_comms.advance()
		elif game.paused: game._set_paused(false,false)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="marsh"),"Normal Hab construction frees a berth and Marsh wakes")
	check(game.crew_count==6 and game._get_crew_capacity()==6,"Hab resident and Marsh both count against capacity")
	game._set_paused(true,false)
	check(Save.write(game,player.out+"recovered.loop")==OK,"Recovered fixture saves")
	game._fit_station_view(false)
	await process_frame
	RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(player.out+"marsh-recovered.png")
	player.free()
	print("PROCEDURAL BERTH STRATEGY: failures=",failures," crew=",game.crew_count," capacity=",game._get_crew_capacity())
	quit(0 if failures==0 else 1)
