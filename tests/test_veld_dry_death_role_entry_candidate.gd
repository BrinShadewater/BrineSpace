extends SceneTree
## Actual oxygen deaths with candidate art injection; normal selection remains pending.
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
	game.meta.save_path="user://dry-entry.meta";game.run_save_path="user://dry-entry.loop";game.Preferences.save_path="user://dry-entry.cfg"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false)
	var grid=game.grid_view;var player=grid.veld_player
	player.load_manifest("res://character/veld-death-ground-family-v1/bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/veld-death-ground-family-v1/helmet-manifest.json"),"Candidate dry equipment injection")
	var home:Vector2i=game.placed_rooms[0].pos
	var center:Vector2=(Vector2(home)+Vector2.ONE*.5)*384
	var board_textures:=[]
	for facing in ["east","west","north","south"]:
		for gear in ["","diving-helmet"]:
			for mode in ["carry","pickup","unload","interact","stand","carry-turn"]:
				for offset in [0.0,17.43]:
					var actor=game.veld_npc;actor.dead=false;await actor.rebuild(game)
					actor.active=true;actor.dead=false;actor.state="carry" if mode=="carry-turn" else mode;actor.direction=facing;actor.helmet_equipped=not gear.is_empty();actor.foot=center;actor.stage="";actor.goal="";actor.path.clear();actor.expedition.clear();actor.locker_request.clear();actor.air_recovery=0;actor.movement_medium="dry";actor.air_was_low=false;actor.breath_oxygen=15;actor.tank_oxygen=60;actor.water_death_motion.clear();actor.water_death_last_frame=null
					game.resources.oxygen=100;game.resources.food=100;game.occupied[home].water_level=0;game.recovered_crew=[{"architect_id":"veld","alive":true}];game.crew_count=4
					player.current_key="";player.motion.clear();player.last_time=-1;game.visual_time_seconds=offset
					if mode=="carry-turn":actor.direction={"east":"north","west":"south","north":"east","south":"west"}[facing]
					grid._get_veld_frame_source(game)
					if mode=="carry-turn":
						actor.direction=facing;game.visual_time_seconds=offset+.13;grid._get_veld_frame_source(game)
					game.visual_time_seconds=offset+.35
					var incoming=grid._get_veld_frame_source(game);var at:float=game.visual_time_seconds
					game.resources.oxygen=0;actor.breath_oxygen=.01;actor.tank_oxygen=.01
					Flood.step_crew(game,actor,"veld",.02);deaths+=1
					check(actor.dead and actor.state=="death-ground","Actual dry oxygen death")
					check(not actor.water_death_motion.is_empty(),"Captured last drawn dry pose")
					if actor.water_death_motion.is_empty():continue
					var saved:Dictionary=actor.water_death_motion.duplicate(true)
					var expected_facing:String=incoming.get_meta("crew_water_facing",facing)
					if expected_facing not in ["east","west","north","south"]:expected_facing=facing
					check(saved.clip=="death-ground-"+expected_facing,"Death camera follows actual incoming projection")
					check(saved.entry_key.begins_with(mode+"-") if mode!="carry-turn" else saved.entry_key.begins_with("carry-turn-"),"Actual requested role row, no idle fallback")
					if mode in ["pickup","unload","stand"]:
						var idle_row:Array=player.frames[saved.clip] if gear.is_empty() else player.equipment_frames[gear][saved.clip]
						var lowered:bool=incoming.get_meta("crew_alpha_extent").size.y<idle_row[0].get_meta("crew_alpha_extent").size.y*.78
						check(saved.first==(2 if lowered else 1),"Lowered cargo/action phase avoids rising reset")
					check(grid._get_veld_frame_source(game)==incoming,"Exact incoming whole pose at death")
					game.visual_time_seconds=at+.179;check(grid._get_veld_frame_source(game)==incoming,"Held incoming entry")
					var rows:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
					# Sample after the boundary: subtraction at a nonzero clock can round
					# the nominal .18 elapsed infinitesimally into the held entry slot.
					for elapsed in [.180001,.36,.60,1.06,3.0]:
						game.visual_time_seconds=at+elapsed;var shown=grid._get_veld_frame_source(game)
						check(shown!=null,"Authored dry interior")
						if elapsed==.180001:check(shown==rows[saved.clip][saved.first],"Correct first lowered interior")
						var data:Dictionary=bytes_to_var(var_to_bytes(actor.snapshot()))
						check(Veld.valid_veld_snapshot(data),"Saved dry selectors validate")
						var playback:Dictionary=bytes_to_var(var_to_bytes(player.snapshot()))
						game.veld_npc=Veld.new();await game.veld_npc.restore_snapshot(game,data);actor=game.veld_npc;player.restore_snapshot(playback)
						check(grid._get_veld_frame_source(game)==shown,"Paused actor/player restore exact")
						check(actor.water_death_motion==saved,"Saved entrance and clock survive")
					check(grid._get_veld_frame_source(game)==rows[saved.clip][-1],"Finite dry corpse held")
					if mode in ["pickup","unload","carry-turn"] and offset==0.0:board_textures.append(incoming);board_textures.append(rows[saved.clip][saved.first]);board_textures.append(rows[saved.clip][-1])
					var bad:Dictionary=actor.snapshot();bad.veld_water_death.first=4;check(not Veld.valid_veld_snapshot(bad),"Invalid dry start rejected")
					bad=actor.snapshot();bad.veld_water_death.clip="death-water-"+facing;check(not Veld.valid_veld_snapshot(bad),"Mixed dry/wet contract rejected")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(600,3960);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(600,3960);bg.color=Color("202a30");view.add_child(bg)
		for i in board_textures.size():
			var texture:Texture2D=board_textures[i];var sprite:=Sprite2D.new();sprite.texture=texture;sprite.centered=false;sprite.scale=Vector2.ONE*82/float(texture.get_meta("crew_standing_height",148));sprite.position=Vector2((i%3)*200+100,(i/3)*165+150)-Vector2(texture.get_meta("crew_pivot"))*sprite.scale;view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-dry-death-role-entry-candidate-v1/native-contact.png")==OK,"Native standing/lowered entrances and corpses")
		view.queue_free()
	game.queue_free();await process_frame;await process_frame
	print("VELD DRY DEATH ROLE ENTRY CANDIDATE: %d checks,%d failures,%d oxygen deaths"%[checks,failures,deaths]);quit(1 if failures else 0)

