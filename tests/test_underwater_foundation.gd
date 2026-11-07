extends SceneTree
const Field = preload("res://scripts/wreck_field.gd")
const Visibility = preload("res://scripts/underwater_visibility.gd")
var failures := 0
var game
const OUT := "res://output/underwater-foundation/"
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	if not ok: failures+=1;push_error(message)
var focus := Vector2(20.5,20.5)
var zoom:=.45
func capture(label: String):
	game._set_grid_zoom(zoom,true,focus/40.0)
	game._refresh_all()
	game.grid_view.queue_redraw()
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+label+".png")
func run():
	var field := Field.initial()
	check(Field.valid(field,{}),"New formations validate")
	var home := {Vector2i(20,20):true}
	check(not Field.reachable(home,Vector2i(14,20),field),"Solid interior cannot be targeted through rock")
	check(Field.reachable(home,Vector2i(16,20),field)==false,"Joined mountain edge behind old shelf remains sealed")
	check(Field.reachable(home,Vector2i(17,20),field),"Exposed mountain reachable across water")
	check(not Field.visible(field,Vector2i(13,21)),"Sealed pocket is unidentified")
	for cell in [Vector2i(17,20),Vector2i(16,20),Vector2i(15,20),Vector2i(14,20),Vector2i(13,20)]:
		check(Field.reachable(home,cell,field),"Tunnel advances only after previous cut")
		field[cell].active=true
		Field.advance(field,home,9)
		check(not field[cell].cleared,"Partial drill work remains solid")
		Field.advance(field,home,9)
		check(field[cell].cleared,"Full drill work opens tunnel")
	check(Field.visible(field,Vector2i(13,21)),"Excavation reveals buried service pocket")
	check(Visibility.clear_ray(field,Vector2(17.5,20.5),Vector2(13.5,20.5)),"Light follows open tunnel")
	check(not Visibility.clear_ray(field,Vector2(17.5,20.5),Vector2(13.5,22.5)),"Remaining rock blocks light")
	check(Visibility.clear_ray(field,Vector2(14.5,20.5),Vector2(14.5,19.5)),"Survey records the first exposed mountain face")
	check(not Visibility.valid({Vector2i(40,0):true}),"Survey rejects out of bounds cells")
	DirAccess.make_dir_recursive_absolute(OUT)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://underwater_%d.meta"%OS.get_process_id()
	game.run_save_path="user://underwater_%d.loop"%OS.get_process_id()
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	for i in range(10): await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	game.paused=true;game.selected_card_id="";game.hovered_card_id="";game._set_grid_zoom(.5)
	game.inspector_focus_button.set_meta("cell",Vector2i(20,20));game._focus_inspected_room()
	var initial_lights := Visibility.sources(game)
	check(not initial_lights.is_empty(),"Core provides exterior sources")
	await capture("station-on")
	game.hardware.exterior=false
	check(Visibility.sources(game).is_empty(),"Exterior switch removes station beams")
	await capture("station-off")
	game.hardware.exterior=true
	game.wrecks=field
	game.bill_npc.active=true;game.bill_npc.dead=false;game.bill_npc.movement_medium="exterior";game.bill_npc.helmet_equipped=true
	game.bill_npc.foot=Vector2(15.5,20.5)*384;game.bill_npc.direction="west"
	focus=Vector2(15.5,20.5)
	check(Visibility.sources(game).any(func(light):return light.kind=="diver"),"Diver carries directional lamp")
	await capture("excavated-tunnel-diver")
	game.hardware.exterior=false
	check(Visibility.sources(game).size()==1,"Diver lamp independent of station switch")
	await capture("diver-only")
	game._place_room("mining_drone_bay",Vector2i(18,20),true)
	for i in range(12): await process_frame
	game.drone_fleet.synchronize(game.placed_rooms)
	var drone: Dictionary=game.drone_fleet.drones[Vector2i(18,20)]
	drone.phase="working";drone.job="clear";drone.target=Vector2(14,19);drone.position=drone.target
	check(Visibility.sources(game).any(func(light):return light.kind=="drone"),"Drone carries independent work light")
	focus=Vector2(14.5,20.1)
	await capture("drill-silt")
	game.bill_npc.active=false
	drone.phase="docked"
	game.visual_time_seconds+=7
	zoom=.16;focus=Vector2(15,21)
	for cell in game.wrecks: game.surveyed_water[cell]=true
	await capture("surveyed-mountain")
	game.surveyed_water[Vector2i(15,20)]=true
	var saved: Dictionary=preload("res://scripts/run_save.gd").capture(game)
	check(saved.surveyed_water.has(Vector2i(15,20)) and saved.wrecks[Vector2i(13,20)].cleared,"Checkpoint retains survey and excavation")
	print("UNDERWATER FOUNDATION: %s failures=%d"%["PASS" if failures==0 else "FAIL",failures])
	quit(1 if failures else 0)
