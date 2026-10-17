extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const PACKS={"bare":"res://character/veld-rest-east-coherent-v1/bare-manifest.json","helmet":"res://character/veld-rest-east-coherent-v1/helmet-manifest.json"}
var checks:=0
var failures:=0
func check(ok:bool,why:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init()->void:call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var p=Player.new()
	p.load_manifest(PACKS.bare);check(p.frames.has("lie-down-east"),"Actual bare candidate loads")
	check(p.load_equipment_manifest("diving-helmet",PACKS.helmet),"Actual paired helmet candidate loads")
	var all_frames:=[]
	for gear in ["bare","helmet"]:
		var equipment:String="" if gear=="bare" else "diving-helmet"
		var row:Array=p.frames["lie-down-east"] if gear=="bare" else p.equipment_frames[equipment]["lie-down-east"]
		var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACKS[gear]));var s:Dictionary=m.states[0]
		check(row.size()==6 and is_equal_approx(p.cycle_seconds("lie-down-east",equipment),1.84),"Original finite cycle")
		all_frames.append_array(row)
		var elapsed:=0.0
		for i in 6:
			var texture:Texture2D=row[i]
			check(texture.get_image().get_data()==Image.load_from_file(PACKS[gear].get_base_dir().path_join(s.frameFiles[i])).get_data(),"Exact loaded exported pixels")
			check(texture.get_meta("crew_pivot")==Vector2(128,224) and texture.get_meta("crew_standing_height")==148.0,"Dry registration and ruler")
			check(not texture.get_meta("crew_water_pose") and texture.get_meta("crew_water_kind")=="rest" and texture.get_meta("crew_water_facing")=="east","Dry directional metadata")
			check(p.frame_at_elapsed("lie-down-east",elapsed+.001,equipment)==texture,"Authored slot at boundary")
			elapsed+=float(s.frameDurationsMs[i])/1000
		check(p.frame_at_elapsed("lie-down-east",4.5,equipment)==row[-1],"Finite terminal corpse does not loop")
		check(p.frame_at_elapsed("lie-down-east",-.5,equipment)==row[0],"Negative phase clamps to entry")
		for clock in [0.0,17.43]:
			p.current_key="";p.motion.clear();p.last_time=-1
			var first=p.frame("lie-down","east",clock,Vector2.ZERO,equipment)
			check(first==row[0],"Actual player enters from arbitrary visual clock")
			var saved=p.snapshot();check(p.valid_snapshot(saved),"Candidate player snapshot validates")
			p.restore_snapshot(saved);check(p.frame("lie-down","east",clock,Vector2.ZERO,equipment)==first,"Paused same-clock restore")
		var clips:Dictionary=p.frames if gear=="bare" else p.equipment_frames[equipment]
		var rising:Array=clips["get-up-east"];var sleeping:Array=clips["sleep-east"]
		check(rising.size()==6 and is_equal_approx(p.cycle_seconds("get-up-east",equipment),1.84),"Authored reversed rise cycle")
		for i in 6:check(rising[i].get_image().get_data()==row[5-i].get_image().get_data(),"Actual rise resolves exact reversed source")
		check(p.frame_at_elapsed("get-up-east",3.0,equipment)==rising[-1],"Rise holds exact standing terminal")
		check(sleeping.size()==1 and sleeping[0].get_image().get_data()==row[-1].get_image().get_data(),"Closed-eye sleeping endpoint resolves")
		check(p.frame_at_elapsed("sleep-east",9.0,equipment)==sleeping[0],"Held sleep does not change pose")
		for action in ["get-up","sleep"]:
			p.current_key="";p.motion.clear();p.last_time=-1
			var first=p.frame(action,"east",17.43,Vector2.ZERO,equipment)
			check(first==clips[action+"-east"][0],"Actual role entrance")
			var saved=p.snapshot();check(p.valid_snapshot(saved),"Role snapshot validates")
			p.restore_snapshot(saved);check(p.frame(action,"east",17.43,Vector2.ZERO,equipment)==first,"Paused role restore exact")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1536,820);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(1536,820);bg.color=Color("202a30");view.add_child(bg)
		for scale_row in 2:
			for i in all_frames.size():
				var sprite:=Sprite2D.new();sprite.texture=all_frames[i];sprite.centered=false;sprite.scale=Vector2.ONE*(148 if scale_row==0 else 82)/148.0;sprite.position=Vector2((i%6)*256+128,230+(i/6)*180+scale_row*330)-Vector2(128,224)*sprite.scale;view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-rest-east-candidate-v1/native-contact.png")==OK,"Native148/82 paired finite poses")
		view.queue_free()
	print("VELD EAST REST CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)



