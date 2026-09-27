extends SceneTree
const C=preload("res://scripts/companions.gd")
const Art=preload("res://scripts/companion_rescue_art.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT="res://output/robot-rescue-native"
var game
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,message:String):
	if not ok:failures+=1;push_error(message)
func capture(label:String):
	if DisplayServer.get_name()=="headless":return
	game._focus_inspected_room()
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT.path_join(label+".png"))
func run():
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://rescue-art.meta";game.run_save_path="user://rescue-art.loop"
	game.meta.unlocked_companion_ids={};game.meta.selected_companion_ids=[]
	root.size=Vector2i(1600,900);root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=false
	game.Architects.advance_core(game,10)
	for id in ["river","josh"]:
		var cell:Vector2i=C.CELLS[id]
		game._place_room("corridor",Vector2i(20,19) if id=="river" else Vector2i(21,20),true)
		C.connect_room(game,cell);game.wrecks[cell].cleared=true;game.wrecks[cell].paid=true;game.wrecks[cell].progress=18.0
		game.powered_room_cells[cell]=true
		game._set_grid_zoom(2.5);await process_frame
		game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room();await process_frame
		await capture(id+"-closed")
		C.toggle(game,cell)
		for stamp in [.45,.9,1.3,3.8,6.3,7.2,7.95]:
			C.advance(game,stamp-float(game.wrecks[cell].boot))
			var before:float=game.wrecks[cell].boot
			var texture:Texture2D=C.rescue_texture(game,cell)
			check(texture.get_size()==Vector2(320,440),"Canvas "+id)
			check(texture.get_meta("crew_standing_height")==148,"Density "+id)
			game.paused=true;C.advance(game,.2)
			check(game.wrecks[cell].boot==before and C.rescue_texture(game,cell)==texture,"Pause holds frame "+id)
			game.paused=false;game.powered_room_cells.erase(cell);C.advance(game,.2)
			check(game.wrecks[cell].boot==before,"Power loss holds recovery "+id)
			game.powered_room_cells[cell]=true
			await capture(id+"-"+str(stamp))
			if stamp==3.8:
				var saved:Dictionary=Save.capture(game)
				check(Save.restore(game,saved),"Save restores reboot "+id)
				game.tick_timer.stop();game.paused=false;game.powered_room_cells[cell]=true
				check(game.wrecks[cell].boot==before,"Saved visual clock "+id)
		var actor=game.companion_actors[id]
		var exit_point:Variant=C.spawn_point(actor,cell)
		print("RESCUE EXIT ",id," ",exit_point-(Vector2(cell)+Vector2.ONE*.5)*384.0-C.CONTAINER_FOOT)
		C.advance(game,.05)
		check(game.wrecks[cell].recovered and actor.active,"Eight second handoff "+id)
		check(actor.foot.distance_to(exit_point)<1,"Exit navigation continuity "+id)
		check(C.rescue_texture(game,cell)==Art.empty_frame(id),"Recovered container empty "+id)
		await capture(id+"-recovered")
	print("ROBOT RESCUE ART ","PASS" if failures==0 else "FAIL"," failures=",failures)
	game.queue_free();await process_frame;quit(failures)
