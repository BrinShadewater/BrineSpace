extends SceneTree
## Candidate art, real life chooser/renderer, flooded respiration and geometry gate.
const Life=preload("res://scripts/crew_life.gd")
const Flood=preload("res://scripts/room_flooding.gd")
const PACKS={"bare":"res://character/veld-swim-distress-south-coherent-v1/bare-manifest.json","helmet":"res://character/veld-swim-distress-south-coherent-v1/helmet-manifest.json"}
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
	player.load_manifest(PACKS.bare,true)
	check(player.load_equipment_manifest("diving-helmet",PACKS.helmet),"Candidate equipment injection")
	var profile: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/dr-veld-v2/clearance.json"))
	var report: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/veld-swim-distress-south-coherent-v1/validation.json"))
	var retained: Dictionary=Life.clearance.duplicate(true)
	Life.clearance["veld"]=profile.life.duplicate(true)
	for record in report.records:Life.clearance.veld[record.gear]["swim-distress-south"]=record.conservativeCandidateExtent
	var home: Vector2i=game.placed_rooms[0].pos
	var center: Vector2=(Vector2(home)+Vector2.ONE*.5)*384.0
	var textures:=[]
	for gear in ["bare","helmet"]:
		var equipment: String="" if gear=="bare" else "diving-helmet"
		actor.dead=false;actor.active=true;actor.helmet_equipped=gear=="helmet";actor.direction="south";actor.state="walk";actor.foot=center;actor.goal="";actor.stage="";actor.path.clear();actor.expedition.clear();actor.locker_request.clear();actor.moonbay_assignment.clear()
		actor.geometry.clear()
		for y in range(-1,2):
			for x in range(-1,2):actor.geometry[home+Vector2i(x,y)]={"swim_blockers":[]}
		actor.swim_region_cache.clear()
		var row: Array=player.frames["swim-distress-south"] if gear=="bare" else player.equipment_frames[equipment]["swim-distress-south"]
		var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACKS[gear]));var s: Dictionary=m.states[0]
		check(row.size()==6 and s.loop,"Candidate coverage and loop")
		for i in 6:
			check(row[i].get_image().get_data()==Image.load_from_file(PACKS[gear].get_base_dir().path_join(s.frameFiles[i])).get_data(),"Candidate frame pixels")
			check(row[i].get_meta("crew_pivot")==Vector2(128,128) and row[i].get_meta("crew_standing_height")==148.0,"Swimming registration")
			check(row[i].get_meta("crew_water_kind")=="swim" and row[i].get_meta("crew_water_pose"),"Prone wet metadata")
			check(player.frame_at_elapsed("swim-distress-south",i*.16+.00001,equipment)==row[i],"Every manifest slot")
		var swim: Array=player.frames["swim-south"] if gear=="bare" else player.equipment_frames[equipment]["swim-south"]
		textures.append(swim[0]);textures.append_array(row)
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
			actor.expedition={"phase":"return","cargo":{"sample":1}}
			check(actor.animation_state()=="swim-carry","Cargo excludes collar-touch distress")
			actor.expedition.clear()
			game.occupied[home].water_level=0
			Flood.step_crew(game,actor,"veld",.02)
			check(actor.movement_medium=="dry" and actor.animation_state()!="swim-distress","Actual safe-air transition excludes wet pose")
			actor.movement_medium="flooded";actor.tank_oxygen=11;actor.breath_oxygen=4;actor.dead=false
			actor.die()
			check(actor.animation_state()=="death-water","Death method excludes distress")
			actor.dead=false;actor.state="walk"
		# Test the actual consumed life extent against a synthetic edge blocker.
		var extent: Array=Life.clearance.veld[gear]["swim-distress-south"]
		actor.movement_medium="flooded";actor.swim_region_cache.clear()
		# The consumed footprint unions base swim with the additional life extent.
		var base: Array=actor.swim_clearance[gear]["south"]
		var merged_right: float=maxf(float(base[2]),float(extent[2]))
		actor.geometry[home].swim_blockers=[Rect2(Vector2(merged_right-.5,0),Vector2.ONE)]
		check(not Life.clear(actor,"swim-distress") and actor.animation_state()!="swim-distress","Life gate rejects touching blocker")
		actor.geometry[home].swim_blockers=[Rect2(Vector2(merged_right+4,0),Vector2.ONE)];actor.swim_region_cache.clear()
		check(Life.clear(actor,"swim-distress") and actor.animation_state()=="swim-distress","Life gate accepts outside blocker")
	Life.clearance=retained
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(994,330);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(994,330);bg.color=Color("202a30");view.add_child(bg)
		for i in textures.size():
			var sprite:=Sprite2D.new();sprite.texture=textures[i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2((i%7)*142,(i/7)*165+20);view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-swim-distress-south-candidate-v1/native-contact.png")==OK,"Native station-scale contact")
		view.queue_free()
	game.queue_free();await process_frame;await process_frame
	print("VELD DISTRESS SOUTH CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
