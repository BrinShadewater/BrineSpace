extends SceneTree
## Explicit candidate injection, real survival trigger, finite renderer and disk restoration.
const PACKS={"bare":"res://character/bill-death-ground-family-v1/manifest.json","helmet":"res://character/bill-death-ground-family-v1/helmet-manifest.json"}
const Save=preload("res://scripts/run_save.gd")
const Flood=preload("res://scripts/room_flooding.gd")
var checks:=0
var failures:=0
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok: failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func run() -> void:
	print("BILL LOWERED MORTALITY CANDIDATE profile: "+OS.get_user_data_dir())
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://bill-death.meta";game.run_save_path="user://bill-death.loop"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	var grid=game.grid_view;var player=grid.human_water_player
	
	player.load_manifest(PACKS.bare,true)
	check(player.load_equipment_manifest("diving-helmet",PACKS.helmet),"Candidate gear compatibility")
	if failures:quit(2);return
	# Exercise the existing production dictionary route with explicit candidate rows.
	# This fixture does not change normal artwork selection.
	grid.human_animations["death-ground"]={}
	for facing in ["east","west","north","south"]:
		var candidate_key: String="death-ground-"+facing
		grid.human_animations["death-ground"][facing]=player.frames[candidate_key]
		grid.human_animation_timing[candidate_key]=player.timing[candidate_key]
	grid.human_equipment_frames=player.equipment_frames
	var home: Vector2i=game.placed_rooms[0].pos
	game.occupied[home].water_level=0.0
	var center: Vector2=(Vector2(home)+Vector2.ONE*.5)*384.0
	for peer in [game.veld_npc,game.branforth_npc]:peer.active=true;peer.foot=center;peer.state="idle";peer.path.clear();peer.goal="";peer.stage=""
	for gear in ["bare","helmet"]:
		var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACKS[gear]))
		for s in manifest.states:
			var row: Array=player.frames[s.id] if gear=="bare" else player.equipment_frames["diving-helmet"][s.id]
			check(row.size()==6,"Candidate coverage")
			for i in 6:
				check(row[i].get_image().get_data()==Image.load_from_file(s.frameFiles[i]).get_data(),"Candidate renderer source pixels "+s.id+gear+str(i))
	var terminal_textures:=[]
	for direction in ["east","west","north","south"]:
		for gear in [false,true]:
			var equipment: String="diving-helmet" if gear else ""
			var key: String="death-ground-"+direction
			var row: Array=player.frames[key] if not gear else player.equipment_frames[equipment][key]
			for medium in ["dry"]:
				for cause in ["air","food"]:
					for before in ["kneel","repair"]:
						for offset in [0.0,.49]:
							var actor=game.bill_npc;actor.dead=false;actor.active=true;actor.direction=direction;actor.helmet_equipped=gear;actor.movement_medium=medium;actor.foot=center;actor.state=before;actor.goal="curiosity";actor.stage="";actor.expedition.clear();actor.moonbay_assignment.clear();actor.path=PackedVector2Array([actor.foot+Vector2(12,0)])
							actor.tank_oxygen=.01 if cause=="air" else 60.0;actor.breath_oxygen=.01 if cause=="air" else 15.0;actor.starvation=89.99 if cause=="food" else 0.0;game.resources.food=0 if cause=="food" else 100;game.resources.oxygen=0 if cause=="air" else 100
							grid.human_animation_key="";grid.human_animation_last_time=-1;player.current_key="";player.last_time=-1;player.motion.clear()
							game.visual_time_seconds=100+offset
							grid._get_human_frame_source(before,direction)
							game.visual_time_seconds+=1.0
							var prior_crown:float=grid._get_human_frame_source(before,direction).get_meta("crew_alpha_extent").position.y
							Flood.step_crew(game,actor,"bill",.02)
							check(actor.dead and actor.animation_state()=="death-ground","Actual survival mortality")
							check(is_equal_approx(actor.death_entry_seconds,.55) if direction in ["north","south"] else grid._get_human_frame_source(actor.animation_state(),direction).get_meta("crew_alpha_extent").position.y>=prior_crown-.5,"Authored axial kneel entry or side fall without crown lift: "+direction+str(gear)+before)
							check(actor.path.is_empty() and actor.goal.is_empty() and actor.expedition.is_empty(),"Mortality cancels intent")
							check(grid._get_human_frame_source(actor.animation_state(),direction)==player.frame_at_elapsed(key,actor.death_entry_seconds,equipment),"Actual renderer lowered death entry")
							game.visual_time_seconds=103+offset
							check(grid._get_human_frame_source(actor.animation_state(),direction)==row[-1],"Actual renderer terminal")
							check(grid._get_human_frame_source(actor.animation_state(),direction)==row[-1],"Pause terminal hold")
			# Save genuine deceased actor and its actual renderer clock at midpoint/terminal.
			for elapsed in [.65,2.0]:
				grid.human_animation_key="";grid.human_animation_last_time=-1;game.visual_time_seconds=200
				grid._get_human_frame_source("death-ground",direction);game.visual_time_seconds=200+elapsed
				var saved_entry:float=game.bill_npc.death_entry_seconds
				var expected: PackedByteArray=grid._get_human_frame_source("death-ground",direction).get_image().get_data()
				check(Save.write(game,game.run_save_path)==OK,"Disk death checkpoint: "+Save.last_error)
				var data: Dictionary=Save.read(game.run_save_path)
				check(not data.is_empty(),"Readable death checkpoint")
				if not data.is_empty():
					check(await Save.restore(game,data),"Real checkpoint restores")
					game.set_process(false);game.tick_timer.stop();game.run_save_path="user://bill-death.loop"
					check(is_equal_approx(game.bill_npc.death_entry_seconds,saved_entry),"Lowered entry phase persists through disk restore")
					check(game.bill_npc.dead and game.bill_npc.direction==direction and game.bill_npc.helmet_equipped==gear,"Mortality identity persists")
					check(grid._get_human_frame_source("death-ground",direction).get_image().get_data()==expected,"Exact death pose pixels restore")
			terminal_textures.append(row[-1])
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1000,400);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(1000,400);bg.color=Color("22343e");view.add_child(bg)
		for i in terminal_textures.size():
			var texture: Texture2D=terminal_textures[i];var sprite:=Sprite2D.new();sprite.texture=texture;sprite.centered=false;sprite.scale=Vector2.ONE*82/148; sprite.position=Vector2(125+(i/2)*250,100+(i%2)*200)-Vector2(128,224)*82/148;view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/bill-death-ground-lowered-mortality-candidate-native-v1/loaded-water-carry.png")==OK,"Fresh native family contact")
		view.queue_free()
	game.set_process(false);game.tick_timer.stop();game.queue_free();await process_frame;await process_frame
	print("BILL LOWERED MORTALITY CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
