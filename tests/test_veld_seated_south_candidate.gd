extends SceneTree
const PACK="res://character/veld-seated-south-coherent-v1/"
const OUT="res://output/veld-seated-south-candidate-v1/"
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:
	var path="res://tests/test_veld_seated_south_candidate.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Explicit scratch APPDATA")
	if failures:quit(2);return
	var grid=CandidateGrid.new();grid._load_replacement_crew_animations()
	var player=grid.veld_player
	player.load_manifest(PACK+"bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet",PACK+"helmet-manifest.json"),"Paired candidate load")
	var actor=load("res://scripts/veld_npc.gd").new()
	actor.active=true;actor.dead=false;actor.state="idle";actor.direction="south";actor.movement_medium="dry";actor.bunk_motion.clear()
	var context=ActorContext.new(actor,grid)
	var review:Array=[]
	for equipped in [false,true]:
		actor.helmet_equipped=equipped
		var gear:String="diving-helmet" if equipped else ""
		var pool:Dictionary=player.equipment_frames[gear] if equipped else player.frames
		var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK+("helmet-manifest.json" if equipped else "bare-manifest.json")))
		for clip in manifest.states:
			var row:Array=pool[clip.id]
			check(row.size()==clip.frameFiles.size(),"Candidate source slots")
			var elapsed:=0.0
			for slot in row.size():
				var texture:Texture2D=row[slot]
				check(texture.get_image().get_data()==Image.load_from_file(PACK+clip.frameFiles[slot]).get_data(),"Exact exported source pixels")
				check(texture.get_meta("crew_pivot")==Vector2(128,224) and texture.get_meta("crew_standing_height")==148.0,"Canonical canvas/pivot/ruler")
				check(not texture.get_meta("crew_water_pose"),"Dry seated metadata")
				check(player.frame_at_elapsed(clip.id,elapsed+.001,gear)==texture,"Timeline slot boundary")
				elapsed+=float(clip.frameDurationsMs[slot])/1000.0
			check(player.frame_at_elapsed(clip.id,4.0,gear)==row[-1],"Finite terminal or held seat")
			var action:String=clip.id.trim_suffix("-south")
			for clock in [0.0,91.3]:
				player.current_key="";player.motion.clear();player.last_time=-1
				var texture=player.frame(action,"south",clock,Vector2.ZERO,gear)
				check(texture==row[0],"Fresh action clock starts at source entry")
				var saved=player.snapshot();check(player.valid_snapshot(saved),"Player checkpoint validates")
				player.restore_snapshot(saved);check(player.frame(action,"south",clock,Vector2.ZERO,gear)==texture,"Paused same-clock player restore")
		var down:Array=pool["sit-down-south"];var rising:Array=pool["sit-rise-south"]
		for slot in 6:check(down[slot].get_image().get_data()==rising[5-slot].get_image().get_data(),"Exact reverse seated pose")
		review.append_array(down)
		for elapsed in [0.0,.079999,.08,.18,.32,.48,.64,.799]:
			actor.stage="life_sit";actor.timer=.8-elapsed;actor.goal="fatigue"
			var before:Texture2D=grid._get_veld_live_frame_source(context)
			check(actor.valid_veld_snapshot(actor.snapshot()),"Lowering actor snapshot admission")
			check(is_equal_approx(actor.action_elapsed(),elapsed),"Actual Veld sitting clock")
			var retained:float=actor.interrupted_sit_rise_seconds(context)
			actor.stage="life_rise";actor.timer=retained;actor.goal=""
			check(grid._get_veld_live_frame_source(context).get_image().get_data()==before.get_image().get_data(),"Interrupted rise retains actual displayed pose")
			check(actor.valid_veld_snapshot(actor.snapshot()),"Interrupted rise actor snapshot admission")
		actor.stage="life_seated";actor.timer=7.4;actor.goal="fatigue"
		check(grid._get_veld_live_frame_source(context).get_image().get_data()==down[-1].get_image().get_data(),"Actual held seated controller source")
	var view:=SubViewport.new();view.size=Vector2i(1536,820);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
	var background:=ColorRect.new();background.size=Vector2(1536,820);background.color=Color("202a30");view.add_child(background)
	for small in 2:
		for slot in review.size():
			var sprite:=Sprite2D.new();sprite.texture=review[slot];sprite.centered=false;sprite.scale=Vector2.ONE*(148 if small==0 else 82)/148.0
			sprite.position=Vector2((slot%6)*256+128,230+(slot/6)*180+small*330)-Vector2(128,224)*sprite.scale;view.add_child(sprite)
	await RenderingServer.frame_post_draw
	check(view.get_texture().get_image().save_png(OUT+"native.png")==OK,"Actual player paired148/82 capture")
	context=null;actor=null;grid.free();view.queue_free()
	print("VELD SEATED SOUTH CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)

class ActorContext extends RefCounted:
	var veld_npc
	var grid_view
	func _init(actor,grid):veld_npc=actor;grid_view=grid
	func get_visual_time_seconds():return 91.3
	func get_dr_veld_position():return veld_npc.foot

class CandidateGrid extends "res://scripts/grid_canvas.gd":
	# The controlled fixture has no main scene; held-pose selection still needs
	# a declared world ruler. Production source selection/loader stay inherited.
	func _cell_size()->float:return 384.0

