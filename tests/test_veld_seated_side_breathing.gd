extends SceneTree
const OUT="res://output/veld-seated-side-breathing-v1/native.png"
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:
	var uid="res://tests/test_veld_seated_side_breathing.gd.uid"
	if not FileAccess.file_exists(uid):
		var f=FileAccess.open(uid,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	var grid=CandidateGrid.new();grid._load_replacement_crew_animations()
	var player=grid.veld_player
	# Validate each original paired profile before the breathing override changes
	# held slots from one static image to six phases.
	player.load_manifest("res://character/veld-seated-east-coherent-v1/bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/veld-seated-east-coherent-v1/helmet-manifest.json"),"East paired candidate load")
	player.load_manifest("res://character/veld-seated-west-coherent-v1/bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/veld-seated-west-coherent-v1/helmet-manifest.json"),"West paired candidate load")
	player.load_manifest("res://character/veld-seated-side-breathing-v1/bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/veld-seated-side-breathing-v1/helmet-manifest.json"),"Breathing paired candidate load")
	var actor=load("res://scripts/veld_npc.gd").new()
	actor.active=true;actor.dead=false;actor.state="idle";actor.movement_medium="dry";actor.bunk_motion.clear()
	actor.stage="life_seated";actor.timer=7.4;actor.goal="fatigue"
	var context=ActorContext.new(actor,grid);var review:Array=[]
	for equipped in [false,true]:
		actor.helmet_equipped=equipped
		var gear:String="diving-helmet" if equipped else ""
		var pool:Dictionary=player.equipment_frames[gear] if equipped else player.frames
		for direction in ["east","west"]:
			actor.stage="life_seated";actor.timer=7.4;actor.goal="fatigue"
			actor.direction=direction;var row:Array=pool["sit-idle-"+direction]
			check(row.size()==6,"Six loop phases")
			check(is_equal_approx(player.cycle_seconds("sit-idle-"+direction,gear),3.6),"3.6-second cycle")
			check(row[0].get_image().get_data()==pool["sit-down-"+direction][-1].get_image().get_data(),"Exact down-to-held neutral")
			check(row[-1].get_image().get_data()==pool["sit-rise-"+direction][0].get_image().get_data(),"Exact neutral rise join")
			player.current_key="";player.motion.clear();player.last_time=-1;context.clock=91.3
			check(grid._get_veld_live_frame_source(context)==row[0],"Actual held actor begins neutral")
			for cycle in 2:
				for slot in 6:
					context.clock=91.3+cycle*3.6+slot*.6+.001
					var shown:Texture2D=grid._get_veld_live_frame_source(context)
					check(shown==row[slot],"Actual Veld held source follows visual clock over two cycles")
					check(shown.get_meta("crew_pivot")==Vector2(128,224) and shown.get_meta("crew_standing_height")==148.0,"Master calibration")
					check(shown.get_meta("crew_seat_contact_depth",false),"Registered seated depth marker")
					var saved=player.snapshot();check(player.valid_snapshot(saved),"Player snapshot admission")
					player.restore_snapshot(saved)
					check(grid._get_veld_live_frame_source(context)==shown,"Same-clock player restore exact")
					check(actor.valid_veld_snapshot(actor.snapshot()),"Held actor snapshot admission")
			review.append_array(row)
			# A controlled interruption relaxes only the bounded breath. The room
			# resolver/contact and real service guards are reviewed separately.
			for slot in [1,2,3,4]:
				actor.stage="life_seated";actor.timer=7.4;actor.goal="fatigue"
				player.current_key="";player.motion.clear();player.last_time=-1;context.clock=100.0
				grid._get_veld_live_frame_source(context)
				context.clock=100.0+slot*.6+.001
				var before:Image=grid._get_veld_live_frame_source(context).get_image()
				var retained:float=actor.interrupted_sit_rise_seconds(context)
				actor.stage="life_rise";actor.timer=retained;actor.goal=""
				var after:Image=grid._get_veld_live_frame_source(context).get_image()
				var protected:=true;var changed:=0
				for y in 256:
					for x in 256:
						if before.get_pixel(x,y)!=after.get_pixel(x,y):
							changed+=1
							if not (y>149 and y<163 and (x>85 and x<104 if direction=="east" else x>150 and x<174)):protected=false
				check(protected and changed>0,"Interrupted rise relaxes only bounded interior breath")
				check(after.get_data()==pool["sit-rise-"+direction][0].get_image().get_data(),"Interruption enters exact neutral rise source")
				check(actor.valid_veld_snapshot(actor.snapshot()),"Interrupted side actor snapshot admission")
	var view=SubViewport.new();view.size=Vector2i(1536,1024);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
	var bg=ColorRect.new();bg.size=Vector2(1536,1024);bg.color=Color("202a30");view.add_child(bg)
	for slot in review.size():
		for height in [148,82]:
			var sprite=Sprite2D.new();sprite.texture=review[slot];sprite.centered=false;sprite.scale=Vector2.ONE*height/148.0
			sprite.position=Vector2((slot%6)*256+128,(slot/6)*256+224)-Vector2(128,224)*sprite.scale
			if height==82:sprite.position.x+=65
			view.add_child(sprite)
	await RenderingServer.frame_post_draw
	check(view.get_texture().get_image().save_png(OUT)==OK,"Native source drawing")
	context=null;actor=null;grid.free();view.queue_free()
	print("VELD SIDE BREATHING: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
class ActorContext extends RefCounted:
	var veld_npc
	var grid_view
	var clock:=91.3
	func _init(actor,grid):veld_npc=actor;grid_view=grid
	func get_visual_time_seconds():return clock
	func get_dr_veld_position():return veld_npc.foot
class CandidateGrid extends "res://scripts/grid_canvas.gd":
	func _cell_size()->float:return 384.0
