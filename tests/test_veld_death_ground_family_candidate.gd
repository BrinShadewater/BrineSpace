extends SceneTree
## Combined resolution/player proof; no normal mortality or disk Continue claim.
const Player=preload("res://scripts/crew_sprite_player.gd")
const PACKS={"bare":"res://character/veld-death-ground-family-v1/bare-manifest.json","helmet":"res://character/veld-death-ground-family-v1/helmet-manifest.json"}
var checks:=0
var failures:=0
func check(ok:bool,why:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init()->void:call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var p=Player.new();p.load_manifest(PACKS.bare)
	check(p.load_equipment_manifest("diving-helmet",PACKS.helmet),"Combined equipment pairing")
	check(p.frames.size()==4 and p.equipment_frames["diving-helmet"].size()==4,"Four directions both gears resolve")
	var all_frames:=[]
	for gear in ["bare","helmet"]:
		var equipment:String="" if gear=="bare" else "diving-helmet"
		var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACKS[gear]))
		for direction in ["east","west","north","south"]:
			var key:String="death-ground-"+direction
			var row:Array=p.frames[key] if gear=="bare" else p.equipment_frames[equipment][key]
			var state:Dictionary=m.states.filter(func(s):return s.id==key)[0]
			check(row.size()==6 and is_equal_approx(p.cycle_seconds(key,equipment),1.42),"Finite combined cycle")
			all_frames.append_array(row)
			var elapsed:=0.0
			for i in 6:
				var texture:Texture2D=row[i]
				check(texture.get_image().get_data()==Image.load_from_file(state.frameFiles[i]).get_data(),"Combined whole-path source pixels")
				check(texture.get_meta("crew_pivot")==Vector2(128,224) and texture.get_meta("crew_standing_height")==148.0,"Fixed body registration")
				check(not texture.get_meta("crew_water_pose") and texture.get_meta("crew_water_kind")=="death-ground" and texture.get_meta("crew_water_facing")==direction,"Dry camera metadata")
				check(p.frame_at_elapsed(key,elapsed+.001,equipment)==texture,"Authored frame boundary")
				elapsed+=float(state.frameDurationsMs[i])/1000
			check(p.frame_at_elapsed(key,4.5,equipment)==row[-1],"Held corpse")
			check(p.frame_at_elapsed(key,-.5,equipment)==row[0],"Clamped entrance")
			for clock in [0.0,17.43]:
				p.current_key="";p.motion.clear();p.last_time=-1
				var first=p.frame("death-ground",direction,clock,Vector2.ZERO,equipment)
				check(first==row[0],"Independent direction/gear entrance")
				var saved=p.snapshot();check(p.valid_snapshot(saved),"Combined player snapshot")
				p.restore_snapshot(saved);check(p.frame("death-ground",direction,clock,Vector2.ZERO,equipment)==first,"Paused same-clock restore")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1536,2048);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(1536,2048);bg.color=Color("202a30");view.add_child(bg)
		var sprites:=[]
		for i in all_frames.size():
			var sprite:=Sprite2D.new();sprite.texture=all_frames[i];sprite.centered=false;sprite.position=Vector2((i%6)*256,(i/6)*256);view.add_child(sprite);sprites.append(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-death-ground-family-candidate-v1/native-contact.png")==OK,"Native148 full family")
		for i in sprites.size():
			sprites[i].scale=Vector2.ONE*82/148.0;sprites[i].position=Vector2((i%6)*256+128,(i/6)*256+224)-Vector2(128,224)*sprites[i].scale
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-death-ground-family-candidate-v1/native-small.png")==OK,"Native82 full family")
		view.queue_free()
	print("VELD FAMILY DRY DEATH CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
