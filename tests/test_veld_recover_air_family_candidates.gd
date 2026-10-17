extends SceneTree
## Candidate injection, genuine low-air/safe-air transition and disk restoration.
const PACKS={"bare":"res://character/veld-recover-air-family-coherent-v1/bare-manifest.json","helmet":"res://character/veld-recover-air-family-coherent-v1/helmet-manifest.json"}
const Save=preload("res://scripts/run_save.gd")
const Flood=preload("res://scripts/room_flooding.gd")
var checks:=0
var failures:=0
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func run() -> void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://veld-recovery.meta";game.run_save_path="user://veld-recovery.loop"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	var grid=game.grid_view;var player=grid.veld_player
	player.load_manifest(PACKS["bare"],true)
	check(player.load_equipment_manifest("diving-helmet",PACKS["helmet"]),"Candidate injection")
	var home: Vector2i=game.placed_rooms[0].pos
	var center: Vector2=(Vector2(home)+Vector2.ONE*.5)*384.0
	for peer in [game.bill_npc,game.branforth_npc]:peer.active=true;peer.foot=center;peer.state="idle";peer.path.clear();peer.goal="";peer.stage=""
	for gear in ["bare","helmet"]:
		var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACKS[gear]))
		for s in manifest.states:
			var row: Array=player.frames[s.id] if gear=="bare" else player.equipment_frames["diving-helmet"][s.id]
			check(row.size()==6,"Selected coverage")
			for i in 6:
				check(row[i].get_image().get_data()==Image.load_from_file(s.frameFiles[i]).get_data(),"Injected candidate pixels "+s.id+gear+str(i))
				check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Selected dry registration")
	var review_textures:=[]
	for direction in ["east","west","north","south"]:
		for gear in [false,true]:
			var equipment: String="diving-helmet" if gear else ""
			var key: String="recover-air-"+direction
			var row: Array=player.frames[key] if not gear else player.equipment_frames[equipment][key]
			var idle_row: Array=player.frames["idle-"+direction] if not gear else player.equipment_frames[equipment]["idle-"+direction]
			var idle_plane:=Image.create(256,256,false,Image.FORMAT_RGBA8)
			var idle_image: Image=idle_row[0].get_image()
			var idle_pivot: Vector2=idle_row[0].get_meta("crew_pivot")
			idle_plane.blit_rect(idle_image,Rect2i(Vector2i.ZERO,idle_image.get_size()),Vector2i(Vector2(128,224)-idle_pivot))
			check(row[0].get_image().get_data()==idle_plane.get_data() and row[-1].get_image().get_data()==idle_plane.get_data(),"Exact currently selected idle joins on shared plane")
			for origin in ["dry-oxygen-loss","flooded"]:
				for before in ["idle","walk"]:
					for offset in [0.0,.49]:
						var actor=game.veld_npc;actor.dead=false;actor.active=true;actor.direction=direction;actor.helmet_equipped=gear;actor.movement_medium="dry";actor.foot=center;actor.state=before;actor.goal="";actor.stage="";actor.path.clear();actor.expedition.clear();actor.moonbay_assignment.clear();actor.locker_request.clear();actor.timer=0;actor.air_recovery=0;actor.air_was_low=false
						actor.tank_oxygen=11;actor.breath_oxygen=4;actor.starvation=0;game.resources.food=100
						game.occupied[home].water_level=1.0 if origin=="flooded" else 0.0
						game.resources.oxygen=100 if origin=="flooded" else 0
						game.visual_time_seconds=100+offset
						Flood.step_crew(game,actor,"veld",.02)
						check(not actor.dead and actor.air_was_low,"Actual low-air trigger")
						check(actor.air_recovery==0,"Unsafe air does not recover")
						game.occupied[home].water_level=0;game.resources.oxygen=100
						Flood.step_crew(game,actor,"veld",.02)
						check(actor.movement_medium=="dry" and actor.air_recovery==3.0 and not actor.air_was_low,"Actual safe-air recovery transition")
						if before=="walk":
							check(actor.animation_state()!="recover-air","Moving actor does not enter standing recovery")
							actor.state="idle"
						check(actor.animation_state()=="recover-air" and actor.action_elapsed()==0,"Recovery chooser starts at entry")
						check(grid._get_veld_frame(game)==row[0],"Actual renderer selected recovery entry")
						for i in 6:
							Flood.step_crew(game,actor,"veld",.25 if i==0 else .5)
							check(is_equal_approx(actor.action_elapsed(),i*.5+.25),"Survival simulation advances recovery")
							check(grid._get_veld_frame(game)==row[i],"Actual renderer simulation pose")
							game.visual_time_seconds+=17
							check(grid._get_veld_frame(game)==row[i],"Paused simulation ignores visual time")
						Flood.step_crew(game,actor,"veld",.25)
						check(actor.air_recovery==0 and actor.animation_state()=="idle","Three-second survival recovery ends in idle")
			# Check actual disk restoration at two interiors and completed idle.
			for elapsed in [1.25,2.75,3.0]:
				var actor=game.veld_npc;actor.state="idle";actor.direction=direction;actor.helmet_equipped=gear;actor.air_was_low=true;actor.air_recovery=0;actor.movement_medium="dry";actor.foot=center;actor.goal="";actor.stage="";actor.path.clear()
				game.occupied[home].water_level=0;game.resources.oxygen=100;game.resources.food=100
				Flood.step_crew(game,actor,"veld",.02);Flood.step_crew(game,actor,"veld",elapsed)
				var expected_state: String=actor.animation_state();var recovery: float=actor.air_recovery
				var expected: PackedByteArray=grid._get_veld_frame(game).get_image().get_data()
				check(Save.write(game,game.run_save_path)==OK,"Disk recovery checkpoint: "+Save.last_error)
				var data: Dictionary=Save.read(game.run_save_path)
				check(not data.is_empty(),"Readable recovery checkpoint")
				if not data.is_empty():
					check(await Save.restore(game,data),"Actual checkpoint restoration")
					game.set_process(false);game.tick_timer.stop();game.run_save_path="user://veld-recovery.loop"
					check(game.veld_npc.direction==direction and game.veld_npc.helmet_equipped==gear and game.veld_npc.movement_medium=="dry","Restored recovery identity")
					check(is_equal_approx(game.veld_npc.air_recovery,recovery) and game.veld_npc.animation_state()==expected_state,"Restored recovery simulation state")
					check(grid._get_veld_frame(game).get_image().get_data()==expected,"Exact selected recovery/idle pixels restore")
			# Recovery clock continues under interruptions; presentation honors active state.
			for interruption in ["walk","stage","flooded","death"]:
				var actor=game.veld_npc;actor.dead=false;actor.active=true;actor.state="idle";actor.stage="";actor.direction=direction;actor.helmet_equipped=gear;actor.foot=center;actor.goal="";actor.path.clear();actor.expedition.clear();actor.moonbay_assignment.clear();actor.locker_request.clear();actor.air_recovery=0;actor.air_was_low=true
				game.occupied[home].water_level=0;game.resources.oxygen=100;game.resources.food=100
				Flood.step_crew(game,actor,"veld",.02);Flood.step_crew(game,actor,"veld",1.25)
				check(actor.animation_state()=="recover-air" and is_equal_approx(actor.air_recovery,1.75),"Actual recovery before interruption")
				if interruption=="walk":
					actor.state="walk";check(actor.animation_state()!="recover-air","Walking overrides standing recovery")
					Flood.step_crew(game,actor,"veld",.5);actor.state="idle"
					check(actor.animation_state()=="recover-air" and is_equal_approx(actor.action_elapsed(),1.75),"Return to idle resumes performed recovery time")
					check(grid._get_veld_frame(game)==row[3],"Resumed renderer uses performed time")
				elif interruption=="stage":
					actor.stage="life_inspect";check(actor.animation_state()!="recover-air","Existing task stage overrides recovery")
					Flood.step_crew(game,actor,"veld",.5);actor.stage=""
					check(actor.animation_state()=="recover-air" and is_equal_approx(actor.action_elapsed(),1.75),"Task release resumes performed recovery time")
				elif interruption=="flooded":
					actor.tank_oxygen=11;actor.breath_oxygen=4;game.occupied[home].water_level=1
					Flood.step_crew(game,actor,"veld",.02)
					check(actor.movement_medium!="dry" and actor.animation_state()!="recover-air","Flooding excludes dry recovery presentation")
					game.occupied[home].water_level=0;Flood.step_crew(game,actor,"veld",.02)
					check(actor.air_recovery==3.0 and actor.animation_state()=="recover-air","Genuine renewed low-air episode starts new recovery")
				else:
					var retained_recovery: float=actor.air_recovery;actor.die()
					# Normal survival dispatch excludes dead crew; direct step_crew does not.
					var was_paused: bool=game.paused;var was_running: bool=game.running
					game.paused=false;game.running=true;Flood.advance(game,.02);actor.update(game,.02)
					game.paused=was_paused;game.running=was_running
					check(actor.dead and actor.animation_state()=="death-ground" and actor.air_recovery==retained_recovery,"Actual death method and survival dispatch exclude live recovery;state="+actor.animation_state()+" recovery="+str(actor.air_recovery)+" expected="+str(retained_recovery))
				actor.dead=false;actor.state="idle";actor.stage="";actor.air_recovery=0
			for i in [1,3,4]:review_textures.append(row[i])
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1200,420);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(1200,420);bg.color=Color("22343e");view.add_child(bg)
		for i in review_textures.size():
			var sprite:=Sprite2D.new();sprite.texture=review_textures[i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148
			var group: int=i/3;var direction_index: int=group/2
			sprite.position=Vector2(direction_index*300+50+(i%3)*100,190+(group%2)*210)-Vector2(128,224)*82/148;view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-recover-air-family-candidate-native-v1/loaded-water-carry.png")==OK,"Fresh native selected family contact")
		view.queue_free()
	game.set_process(false);game.tick_timer.stop();game.queue_free();await process_frame;await process_frame
	print("VELD RECOVERY CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
