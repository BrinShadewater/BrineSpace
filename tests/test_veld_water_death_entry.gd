extends SceneTree
const Flood=preload("res://scripts/room_flooding.gd")
const Veld=preload("res://scripts/veld_npc.gd")
var checks:=0
var failures:=0
var deaths:=0
func check(ok:bool,why:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init()->void:call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://death-entry.meta";game.run_save_path="user://death-entry.loop";game.Preferences.save_path="user://death-entry.cfg"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false)
	var grid=game.grid_view;var player=grid.veld_player
	var home:Vector2i=game.placed_rooms[0].pos
	var center:Vector2=(Vector2(home)+Vector2.ONE*.5)*384
	var board_textures:=[]
	for facing in ["east","west","north","south"]:
		for gear in ["","diving-helmet"]:
			for mode in ["tread","swim","swim-start","swim-stop"]:
				for offset in [0.0,17.43]:
					var actor=game.veld_npc
					actor.dead=false;await actor.rebuild(game)
					actor.active=true;actor.dead=false;actor.state="walk" if mode in ["swim","swim-stop"] else "idle";actor.direction=facing;actor.helmet_equipped=not gear.is_empty();actor.foot=center;actor.stage="";actor.goal="";actor.path.clear();actor.expedition.clear();actor.locker_request.clear();actor.air_recovery=0;actor.movement_medium="flooded";actor.air_was_low=false;actor.breath_oxygen=15;actor.tank_oxygen=60;actor.water_death_motion.clear();actor.water_death_last_frame=null
					game.resources.oxygen=100;game.resources.food=100;game.occupied[home].water_level=1;game.recovered_crew=[{"architect_id":"veld","alive":true}];game.crew_count=4
					var clear_point:=Vector2.INF
					for y in range(48,337,24):
						for x in range(48,337,24):
							actor.foot=Vector2(home)*384+Vector2(x,y)
							if actor.action_pose_clear("transition") and actor.swim_segment_clear(actor.foot,actor.foot,facing,facing,true):clear_point=actor.foot;break
						if clear_point.is_finite():break
					check(clear_point.is_finite(),"Actual room has clear transition point")
					actor.foot=clear_point if clear_point.is_finite() else center
					player.current_key="";player.motion.clear();player.last_time=-1
					game.visual_time_seconds=offset;grid._get_veld_frame_source(game)
					if mode in ["swim-start","swim-stop"]:
						actor.state="walk" if mode=="swim-start" else "idle"
						game.visual_time_seconds=offset+.13;grid._get_veld_frame_source(game)
					elif mode=="swim":actor.foot+=Vector2(7,0)
					game.visual_time_seconds=offset+.35
					var incoming=grid._get_veld_frame_source(game)
					if facing=="east" and gear.is_empty() and offset==0.0:print("ENTRY PROBE ",mode," state=",actor.animation_state()," kind=",incoming.get_meta("crew_water_kind")," motion=",player.motion)
					var at:float=game.visual_time_seconds
					actor.breath_oxygen=.01;actor.tank_oxygen=.01
					Flood.step_crew(game,actor,"veld",.02);deaths+=1
					check(actor.dead and actor.state=="death-water","Actual oxygen death")
					check(not actor.water_death_motion.is_empty(),"Saved live entrance")
					if actor.water_death_motion.is_empty():continue
					var saved:Dictionary=actor.water_death_motion.duplicate(true)
					var expected:String=("death-water-" if mode=="swim" else "death-water-tread-")+facing
					check(saved.clip==expected,"Incoming camera selects collapse family: "+mode)
					if mode in ["swim-start","swim-stop"]:check(saved.entry_key.begins_with(mode+"-"),"Actual partial-pitch entrance")
					check(grid._get_veld_frame_source(game)==incoming,"Exact whole incoming frame at death")
					game.visual_time_seconds=at+.179
					check(grid._get_veld_frame_source(game)==incoming,"Live pose held through entry slot")
					for elapsed in [.18,.36,.60,1.06,3.0]:
						game.visual_time_seconds=at+elapsed
						var shown=grid._get_veld_frame_source(game)
						check(shown!=null,"Authored collapse frame")
						var data:Dictionary=bytes_to_var(var_to_bytes(actor.snapshot()))
						check(Veld.valid_veld_snapshot(data),"Actor death checkpoint selector valid")
						var playback:Dictionary=bytes_to_var(var_to_bytes(player.snapshot()))
						game.veld_npc=Veld.new();await game.veld_npc.restore_snapshot(game,data)
						actor=game.veld_npc;player.restore_snapshot(playback)
						check(grid._get_veld_frame_source(game)==shown,"Restored actor and playback retain exact pose")
						check(actor.water_death_motion==saved,"Checkpoint keeps incoming selectors and clock")
					var rows:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
					check(grid._get_veld_frame_source(game)==rows[saved.clip][-1],"Finite authored terminal holds")
					game.occupied[home].water_level=0;game.paused=false;Flood.advance(game,.02);game.paused=true
					check(actor.dead and grid._get_veld_frame_source(game)==rows[saved.clip][-1],"Room drying preserves water corpse")
					if mode=="tread" and offset==0.0:board_textures.append(incoming);board_textures.append(rows[saved.clip][saved.first]);board_textures.append(rows[saved.clip][-1])
					var legacy:Dictionary=actor.snapshot();legacy.erase("veld_water_death")
					check(Veld.valid_veld_snapshot(legacy),"Older corpse checkpoint remains readable")
					var bad:Dictionary=actor.snapshot();bad.veld_water_death.entry_index=-1
					check(not Veld.valid_veld_snapshot(bad),"Invalid cached entrance rejected")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(600,1320);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(600,1320);bg.color=Color("202a30");view.add_child(bg)
		for i in board_textures.size():
			var texture:Texture2D=board_textures[i];var sprite:=Sprite2D.new();sprite.texture=texture;sprite.centered=false;sprite.scale=Vector2.ONE*82/float(texture.get_meta("crew_standing_height",148));sprite.position=Vector2((i%3)*200+100,(i/3)*165+82)-Vector2(texture.get_meta("crew_pivot"))*sprite.scale;view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-water-death-entry-v1/native-contact.png")==OK,"Native entrance/collapse/corpse board")
		view.queue_free()
	game.queue_free();await process_frame;await process_frame
	print("VELD LIVE WATER DEATH ENTRY: %d checks,%d failures,%d oxygen deaths"%[checks,failures,deaths]);quit(1 if failures else 0)
