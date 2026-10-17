extends SceneTree
## Normal-loader selected cardinal family, actual life/renderer and every-phase joins.
## Synthetic geometry only; furnished world and disk restore remain separate.
const Life=preload("res://scripts/crew_life.gd")
const Flood=preload("res://scripts/room_flooding.gd")
const PACKS={"bare":"res://character/veld-swim-distress-family-coherent-v1/bare-manifest.json","helmet":"res://character/veld-swim-distress-family-coherent-v1/helmet-manifest.json"}
const JOIN_DONORS={"east-bare": "res://character/veld-water-east-coherent-v1/frames/bare/swim-east/000.png", "east-helmet": "res://character/veld-water-east-coherent-v1/frames/helmet/swim-east/000.png", "west-bare": "res://character/veld-water-west-coherent-v1/frames/bare/swim-west/000.png", "west-helmet": "res://character/veld-water-west-coherent-v1/frames/helmet/swim-west/000.png", "north-bare": "res://character/veld-water-north-coherent-v1/frames/bare/swim-north/000.png", "north-helmet": "res://character/veld-water-north-coherent-v1/frames/helmet/swim-north/000.png", "south-bare": "res://character/veld-water-south-coherent-v1/frames/bare/swim-south/000.png", "south-helmet": "res://character/veld-water-south-coherent-v1/frames/helmet/swim-south/000.png"}
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
	game.meta.save_path="user://veld-distress.meta";game.run_save_path="user://veld-distress.loop"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	var grid=game.grid_view;var player=grid.veld_player;var actor=game.veld_npc
	check(player.equipment_frames.has("diving-helmet"),"Normal loader selected equipment")
	var profile: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/dr-veld-v2/clearance.json"))
	var retained: Dictionary=Life.clearance.duplicate(true)
	Life.clearance["veld"]=profile.life.duplicate(true)
	var home: Vector2i=game.placed_rooms[0].pos
	var center: Vector2=(Vector2(home)+Vector2.ONE*.5)*384.0
	var textures:=[]
	for direction in ["east","west","north","south"]:
		for gear in ["bare","helmet"]:
			var equipment: String="" if gear=="bare" else "diving-helmet"
			actor.dead=false;actor.active=true;actor.helmet_equipped=gear=="helmet";actor.direction=direction;actor.state="walk";actor.foot=center;actor.goal="";actor.stage="";actor.path.clear();actor.expedition.clear();actor.locker_request.clear();actor.moonbay_assignment.clear()
			actor.geometry.clear()
			for y in range(-1,2):
				for x in range(-1,2):actor.geometry[home+Vector2i(x,y)]={"swim_blockers":[]}
			actor.swim_region_cache.clear()
			var row: Array=player.frames["swim-distress-"+direction] if gear=="bare" else player.equipment_frames[equipment]["swim-distress-"+direction]
			var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACKS[gear]));var s: Dictionary={}
			for state in m.states:
				if state.id=="swim-distress-"+direction:s=state
			check(row.size()==6 and s.loop,"Candidate coverage and loop")
			for i in 6:
				check(row[i].get_image().get_data()==Image.load_from_file(PACKS[gear].get_base_dir().path_join(s.frameFiles[i])).get_data(),"Candidate frame pixels")
				check(row[i].get_meta("crew_pivot")==Vector2(128,128) and row[i].get_meta("crew_standing_height")==148.0,"Swimming registration")
				check(row[i].get_meta("crew_water_kind")=="swim" and row[i].get_meta("crew_water_pose"),"Prone wet metadata")
				check(player.frame_at_elapsed("swim-distress-"+direction,i*.16+.00001,equipment)==row[i],"Every manifest slot")
			var swim: Array=player.frames["swim-"+direction] if gear=="bare" else player.equipment_frames[equipment]["swim-"+direction]
			var donor:PackedByteArray=Image.load_from_file(JOIN_DONORS[direction+"-"+gear]).get_data()
			for join_slot in [0,5]:check(row[join_slot].get_image().get_data()==donor,"Exact selected swim entry and closure")
			textures.append(swim[0]);textures.append_array(row)
			# Exercise actual player transitions using distance-driven swim phase.
			# These assertions prove phase/reset/pixels, not perceived smoothness.
			for join_phase in 6:
				player.current_key="";player.last_time=-1
				var stamp:float=100.0+join_phase*3.0
				var pos:=Vector2(2,2)
				player.frame("swim",direction,stamp,pos,equipment,false)
				pos.x+=float(player.strides["swim"])*(join_phase+.01)/6.0
				check(player.frame("swim",direction,stamp+.01,pos,equipment,false)==swim[join_phase],"Every distance-driven swim entry phase")
				check(player.frame("swim-distress",direction,stamp+.02,pos,equipment,false)==row[0],"Every swim phase enters exact master distress0")
				check(player.frame("swim-distress",direction,stamp+.02+join_phase*.16+.001,pos,equipment,false)==row[join_phase],"Every distress exit phase")
				check(player.frame("swim",direction,stamp+.03+join_phase*.16+.001,pos,equipment,false)==swim[0],"Every distress phase returns selected swim0")

			for offset in [0.0,17.43]:
				actor.dead=false;actor.state="walk";actor.expedition.clear();actor.movement_medium="flooded";actor.air_was_low=false;actor.air_recovery=0;actor.tank_oxygen=60;actor.breath_oxygen=15
				game.occupied[home].water_level=1;game.resources.oxygen=100;game.resources.food=100
				game.visual_time_seconds=offset;grid._get_veld_frame(game)
				check(actor.animation_state()=="swim","Normal swimming before low air")
				actor.tank_oxygen=12.01;actor.breath_oxygen=5.01
				check(actor.animation_state()=="swim","Above threshold excludes distress")
				Flood.step_crew(game,actor,"veld",.02)
				# Low-air history is sampled before consumption; the first crossing tick
				# exposes distress, and the following unsafe tick records the episode.
				check(actor.animation_state()=="swim-distress","Threshold crossing exposes distress immediately")
				Flood.step_crew(game,actor,"veld",.02)
				check(actor.movement_medium=="flooded" and actor.air_was_low and not actor.dead,"Actual flooded low-air episode")
				check(actor.animation_state()=="swim-distress" and actor.action_elapsed()<0,"Actual life chooser uses cosmetic distress")
				game.visual_time_seconds=offset+.04
				check(grid._get_veld_frame(game)==row[0],"State entry resets to frame zero at arbitrary visual offset")
				for i in 6:
					game.visual_time_seconds=offset+.04+i*.16+.001
					check(grid._get_veld_frame(game)==row[i],"Actual renderer distress slot "+str(i))
				game.visual_time_seconds=offset+.04+.961
				check(grid._get_veld_frame(game)==row[0],"Actual distress loop wraps")
				game.visual_time_seconds=offset+.04+1.281
				check(grid._get_veld_frame(game)==row[2],"Interior pose before interruption")
				actor.expedition={"phase":"return","cargo":{"sample":1}}
				check(actor.animation_state()=="swim-carry","Cargo excludes collar-touch distress")
				check(grid._get_veld_frame(game)!=row[2],"Cargo interruption changes rendered state")
				actor.expedition.clear()
				game.visual_time_seconds+=.02
				check(grid._get_veld_frame(game)==row[0],"Cargo interruption reentry resets phase")
				actor.tank_oxygen=60;actor.breath_oxygen=15
				check(actor.animation_state()=="swim","Restored wet air exits distress")
				grid._get_veld_frame(game)
				actor.tank_oxygen=11;actor.breath_oxygen=4
				game.visual_time_seconds+=.02
				check(grid._get_veld_frame(game)==row[0],"Second low-air episode resets phase")
				game.occupied[home].water_level=0
				Flood.step_crew(game,actor,"veld",.02)
				check(actor.movement_medium=="dry" and actor.animation_state()!="swim-distress","Actual safe-air transition excludes wet pose")
				actor.movement_medium="flooded";actor.tank_oxygen=11;actor.breath_oxygen=4;actor.dead=false
				actor.die()
				check(actor.animation_state()=="death-water","Death method excludes distress")
				actor.dead=false;actor.state="walk"
			# Test the actual consumed life extent against a synthetic edge blocker.
			var extent: Array=Life.clearance.veld[gear]["swim-distress-"+direction]
			actor.movement_medium="flooded";actor.swim_region_cache.clear()
			# The consumed footprint unions base swim with the additional life extent.
			var base: Array=actor.swim_clearance[gear][direction]
			var merged_right: float=maxf(float(base[2]),float(extent[2]))
			actor.geometry[home].swim_blockers=[Rect2(Vector2(merged_right-.5,0),Vector2.ONE)]
			check(not Life.clear(actor,"swim-distress") and actor.animation_state()!="swim-distress","Life gate rejects touching blocker")
			actor.geometry[home].swim_blockers=[Rect2(Vector2(merged_right+4,0),Vector2.ONE)];actor.swim_region_cache.clear()
			check(Life.clear(actor,"swim-distress") and actor.animation_state()=="swim-distress","Life gate accepts outside blocker")
	Life.clearance=retained
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(994,1320);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(994,1320);bg.color=Color("202a30");view.add_child(bg)
		for i in textures.size():
			var sprite:=Sprite2D.new();sprite.texture=textures[i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2((i%7)*142,(i/7)*165+20);view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-swim-distress-family-installed-v1/native-contact.png")==OK,"Native station-scale contact")
		view.queue_free()
	game.queue_free();await process_frame;await process_frame
	print("VELD DISTRESS FAMILY INSTALLED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
