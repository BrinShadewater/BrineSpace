extends "res://tests/test_veld_seated_south_candidate.gd"
const BREATH="res://character/veld-seated-south-breathing-v1/"
const BREATH_OUT="res://output/veld-seated-south-breathing-v1/"
func _init()->void:
	var path="res://tests/test_veld_seated_south_breathing.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Explicit scratch APPDATA")
	if failures:quit(2);return
	var grid=CandidateGrid.new();grid._load_replacement_crew_animations()
	var player=grid.veld_player
	player.load_manifest(PACK+"bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet",PACK+"helmet-manifest.json"),"Static paired sources")
	player.load_manifest(BREATH+"bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet",BREATH+"helmet-manifest.json"),"Paired held override")
	var actor=load("res://scripts/veld_npc.gd").new()
	actor.active=true;actor.dead=false;actor.state="idle";actor.direction="south";actor.movement_medium="dry";actor.bunk_motion.clear()
	var context=BreathingContext.new(actor,grid);var review:Array=[]
	for equipped in [false,true]:
		actor.helmet_equipped=equipped
		var gear:String="diving-helmet" if equipped else ""
		var pool:Dictionary=player.equipment_frames[gear] if equipped else player.frames
		var row:Array=pool["sit-idle-south"]
		var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BREATH+("helmet-manifest.json" if equipped else "bare-manifest.json")))
		var clip:Dictionary=manifest.states[0]
		check(row.size()==6,"Six held source slots")
		for slot in 6:
			var texture:Texture2D=row[slot]
			check(texture.get_image().get_data()==Image.load_from_file(BREATH+clip.frameFiles[slot]).get_data(),"Exact exported held pixels")
			check(texture.get_meta("crew_pivot")==Vector2(128,224) and texture.get_meta("crew_standing_height")==148.0,"Canonical ruler/pivot")
			check(texture.get_meta("crew_seat_contact_depth",false),"Seat contact mark")
			for cycle in [0,1]:
				var elapsed:float=slot*.6+cycle*3.6+.031
				check(player.frame_at_elapsed("sit-idle-south",fmod(elapsed,3.6),gear)==texture,"Explicit elapsed lookup within cycle")
				actor.stage="life_seated";actor.timer=7.4-elapsed;actor.goal="fatigue"
				var saved=actor.snapshot();check(actor.valid_veld_snapshot(saved),"Actor held snapshot admission")
			player.current_key="";player.motion.clear();player.last_time=-1
			check(player.frame("sit-idle","south",91.3,Vector2.ZERO,gear)==row[0],"Fresh loop starts at neutral")
			var saved_player=player.snapshot();check(player.valid_snapshot(saved_player),"Player snapshot validates")
			player.restore_snapshot(saved_player);check(player.frame("sit-idle","south",91.3,Vector2.ZERO,gear)==row[0],"Paused player snapshot restore")
		check(row[0].get_image().get_data()==pool["sit-down-south"][-1].get_image().get_data(),"Down to held exact neutral")
		check(row[-1].get_image().get_data()==pool["sit-rise-south"][0].get_image().get_data(),"Held to rise exact neutral")
		player.current_key="";player.motion.clear();player.last_time=-1
		actor.stage="life_seated";actor.timer=7.4;context.clock=400.0
		check(grid._get_veld_live_frame_source(context)==row[0],"Held hook starts at neutral")
		for cycle in [0,1]:
			for slot in 6:
				context.clock=400.0+cycle*3.6+slot*.6+.031
				var texture:Texture2D=grid._get_veld_live_frame_source(context)
				check(texture==row[slot],"Production held visual clock: cycle%d slot%d"%[cycle,slot])
				check(grid._get_veld_live_frame_source(context)==texture,"Paused source remains stable")
		context.clock=407.201
		check(grid._get_veld_live_frame_source(context)==row[0],"Third cycle seam returns to neutral")
		review.append_array(row)
	var view:=SubViewport.new();view.size=Vector2i(1536,820);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
	var background:=ColorRect.new();background.size=Vector2(1536,820);background.color=Color("202a30");view.add_child(background)
	for small in 2:
		for slot in review.size():
			var sprite:=Sprite2D.new();sprite.texture=review[slot];sprite.centered=false;sprite.scale=Vector2.ONE*(148 if small==0 else 82)/148.0
			sprite.position=Vector2((slot%6)*256+128,230+(slot/6)*180+small*330)-Vector2(128,224)*sprite.scale;view.add_child(sprite)
	await RenderingServer.frame_post_draw
	check(view.get_texture().get_image().save_png(BREATH_OUT+"native.png")==OK,"Actual held native148/82 capture")
	context=null;actor=null;grid.free();view.queue_free()
	print("VELD SEATED SOUTH BREATHING: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)

class BreathingContext extends RefCounted:
	var veld_npc
	var grid_view
	var clock:=400.0
	func _init(actor,grid):veld_npc=actor;grid_view=grid
	func get_visual_time_seconds():return clock
	func get_dr_veld_position():return veld_npc.foot
