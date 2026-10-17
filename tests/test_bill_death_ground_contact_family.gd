extends SceneTree
const BASE="res://character/bill-death-ground-contact-family-v1/manifest.json"
const HELMET="res://character/bill-death-ground-contact-family-v1/helmet-manifest.json"
const SAFE=preload("res://scripts/safe_image.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	print("BILL DEATH GROUND FAMILY profile: "+OS.get_user_data_dir())
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(2);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	player.load_manifest(BASE,true);check(player.load_equipment_manifest("diving-helmet",HELMET),"Compatible paired family equipment loaded")
	if failures:quit(2);return
	var view:=SubViewport.new();view.size=Vector2i(1536,3072);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
	var bg:=ColorRect.new();bg.size=Vector2(1536,3072);bg.color=Color("22343e");view.add_child(bg)
	for g in 2:
		var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BASE if g==0 else HELMET));check(m.states.size()==6 and m.status=="staged_candidate","Four original and two axial lateral states")
		for d in 6:
			var state:Dictionary=m.states[d];var gear:="" if g==0 else "diving-helmet";var row:Array=player.frames[state.id] if g==0 else player.equipment_frames[gear][state.id]
			check(row.size()==6,"Six finite slots");check(row[0].get_meta("crew_lowered_death_entry",false) and row[0].get_meta("crew_death_contact_choice",false),"Explicit contact-aware candidate metadata");var elapsed:=0.0
			for i in 6:
				var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Literal frame loads")
				check(row[i].get_image().get_data()==raw.get_data(),"Exact assembled pixels")
				check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Shared density/pivot")
				check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_depth_offset")==0.0 and row[i].get_meta("crew_water_kind")=="death-ground","Dry metadata")
				check(player.frame_at_elapsed(state.id,elapsed+float(state.frameDurationsMs[i])/2000,gear)==row[i],"Authored finite phase")
				elapsed+=float(state.frameDurationsMs[i])/1000
				var sprite:=Sprite2D.new();sprite.texture=row[i];sprite.centered=false;sprite.position=Vector2(i*256,(d*2+g)*256);view.add_child(sprite)
			check(is_equal_approx(elapsed,2) and player.frame_at_elapsed(state.id,2,gear)==row[-1] and player.frame_at_elapsed(state.id,99,gear)==row[-1],"Finite terminal holds without resurrection")
	await RenderingServer.frame_post_draw
	check(view.get_texture().get_image().save_png("res://output/bill-death-ground-contact-family-native-v1/loaded-water-carry.png")==OK,"Native paired cardinal review")
	view.queue_free();grid.free();print("BILL DEATH GROUND FAMILY: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
