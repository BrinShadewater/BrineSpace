extends SceneTree
## Prone candidate, actual oxygen death and renderer clock. No normal selection/world proof.
const Flood=preload("res://scripts/room_flooding.gd")
const PACKS={"bare":"res://character/veld-death-water-east-coherent-v1/bare-manifest.json","helmet":"res://character/veld-death-water-east-coherent-v1/helmet-manifest.json"}
var checks:=0
var failures:=0
func check(ok:bool,why:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init()->void:call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Isolated profile")
	if failures:quit(1);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://veld-death.meta";game.run_save_path="user://veld-death.loop";game.Preferences.save_path="user://veld-death.cfg"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false)
	var grid=game.grid_view;var player=grid.veld_player;var actor=game.veld_npc
	player.load_manifest(PACKS.bare,true)
	check(player.load_equipment_manifest("diving-helmet",PACKS.helmet),"Candidate equipment injection")
	var home:Vector2i=game.placed_rooms[0].pos
	var center:Vector2=(Vector2(home)+Vector2.ONE*.5)*384
	var textures:=[]
	for gear in ["bare","helmet"]:
		var equipment:String="" if gear=="bare" else "diving-helmet"
		var row:Array=player.frames["death-water-east"] if gear=="bare" else player.equipment_frames[equipment]["death-water-east"]
		var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACKS[gear]));var state:Dictionary=manifest.states[0]
		check(row.size()==6 and not player.timing["death-water-east"].loop,"Finite death coverage")
		for i in 6:
			check(row[i].get_image().get_data()==Image.load_from_file(PACKS[gear].get_base_dir().path_join(state.frameFiles[i])).get_data(),"Exact candidate pixels")
			check(row[i].get_meta("crew_pivot")==Vector2(128,128) and row[i].get_meta("crew_standing_height")==148.0,"Prone ruler")
			check(row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_water_kind")=="swim","Wet metadata")
		textures.append_array(row)
		for offset in [0.0,17.43]:
			actor.active=true;actor.dead=false;actor.state="walk";actor.direction="east";actor.helmet_equipped=gear=="helmet";actor.foot=center;actor.stage="";actor.goal="";actor.path.clear();actor.expedition.clear();actor.locker_request.clear();actor.air_recovery=0;actor.movement_medium="flooded";actor.air_was_low=false;actor.breath_oxygen=15;actor.tank_oxygen=60
			game.resources.oxygen=100;game.resources.food=100;game.occupied[home].water_level=1;game.recovered_crew=[{"architect_id":"veld","alive":true}];game.crew_count=4
			player.current_key="";player.motion.clear();player.last_time=-1
			game.visual_time_seconds=offset;grid._get_veld_frame_source(game)
			actor.breath_oxygen=.01;actor.tank_oxygen=.01
			Flood.step_crew(game,actor,"veld",.02)
			check(actor.dead and actor.state=="death-water" and actor.animation_state()=="death-water","Real oxygen exhaustion selects wet death")
			check(actor.stage.is_empty() and actor.goal.is_empty() and actor.path.is_empty() and actor.expedition.is_empty(),"Death cancels live activity")
			game.visual_time_seconds=offset+.02
			check(grid._get_veld_frame_source(game)==row[0],"Death enters exact swim master at arbitrary visual clock")
			var elapsed:=0.0
			for i in 6:
				game.visual_time_seconds=offset+.02+elapsed+.001
				var shown=grid._get_veld_frame_source(game)
				check(shown==row[i],"Actual death renderer slot "+str(i))
				var saved:Dictionary=bytes_to_var(var_to_bytes(player.snapshot()))
				check(player.valid_snapshot(saved),"Death playback snapshot valid")
				player.restore_snapshot(saved)
				check(grid._get_veld_frame_source(game)==shown,"Paused/restored playback retains corpse pose")
				elapsed+=float(state.frameDurationsMs[i])/1000
			game.visual_time_seconds=offset+.02+elapsed+3
			check(grid._get_veld_frame_source(game)==row[5],"Finite terminal corpse holds beyond cycle")
			game.occupied[home].water_level=0;Flood.step_crew(game,actor,"veld",.02)
			check(actor.dead and actor.animation_state()=="death-water","Drying water does not revive corpse or switch death kind")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(994,330);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(994,330);bg.color=Color("202a30");view.add_child(bg)
		for i in textures.size():
			var sprite:=Sprite2D.new();sprite.texture=textures[i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2((i%6)*165,(i/6)*165+20);view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-death-water-east-candidate-v1/native-contact.png")==OK,"Native candidate board")
		view.queue_free()
	game.queue_free();await process_frame;await process_frame
	print("VELD EAST WATER DEATH CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
