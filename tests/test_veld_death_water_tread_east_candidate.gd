extends SceneTree
## Candidate source/player proof only; NPC death routing and arbitrary entry remain.
const Player=preload("res://scripts/crew_sprite_player.gd")
const PACKS={"bare":"res://character/veld-death-water-tread-east-coherent-v1/bare-manifest.json","helmet":"res://character/veld-death-water-tread-east-coherent-v1/helmet-manifest.json"}
const KEY="death-water-tread-east"
var checks:=0
var failures:=0
func check(ok:bool,why:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init()->void:call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Isolated profile")
	if failures:quit(1);return
	var player=Player.new();player.load_manifest(PACKS.bare)
	check(player.load_equipment_manifest("diving-helmet",PACKS.helmet),"Candidate equipment pairing")
	var textures:=[]
	for gear in ["bare","helmet"]:
		var equipment:String="" if gear=="bare" else "diving-helmet"
		var row:Array=player.frames[KEY] if gear=="bare" else player.equipment_frames[equipment][KEY]
		var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACKS[gear]));var state:Dictionary=manifest.states[0]
		check(row.size()==6 and not player.timing[KEY].loop,"Finite entrance row")
		check(is_equal_approx(player.cycle_seconds(KEY,equipment),1.56),"Original finite timing")
		var tread=Image.load_from_file("res://character/veld-water-east-coherent-v1/frames/"+gear+"/tread-east/000.png")
		var terminal=Image.load_from_file("res://character/veld-death-water-east-coherent-v1/frames/"+gear+"/death-water-east/005.png")
		check(row[0].get_image().get_data()==tread.get_data(),"Exact selected upright entrance")
		check(row[5].get_image().get_data()==terminal.get_data(),"Exact existing prone corpse endpoint")
		for offset in [0.0,17.43]:
			player.current_key="";player.motion.clear();player.last_time=-1;var elapsed:=0.0
			check(player.frame("death-water-tread","east",offset,Vector2.ZERO,equipment,false)==row[0],"Finite entrance at arbitrary clock")
			for i in 6:
				check(row[i].get_image().get_data()==Image.load_from_file(PACKS[gear].get_base_dir().path_join(state.frameFiles[i])).get_data(),"Exact packaged source")
				check(row[i].get_meta("crew_pivot")==Vector2(128,128) and row[i].get_meta("crew_standing_height")==148.0,"Shared wet plane/ruler")
				check(row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_water_kind")==state.waterKinds[i],"Authored tread/pitch/swim metadata")
				var shown=player.frame("death-water-tread","east",offset+elapsed+.001,Vector2.ZERO,equipment,false)
				check(shown==row[i],"Finite source player slot "+str(i))
				check(player.frame_at_elapsed(KEY,elapsed+.001,equipment)==row[i],"Explicit finite elapsed slot")
				var saved:Dictionary=bytes_to_var(var_to_bytes(player.snapshot()))
				check(player.valid_snapshot(saved),"Candidate player snapshot valid")
				player.restore_snapshot(saved)
				check(player.frame("death-water-tread","east",offset+elapsed+.001,Vector2.ZERO,equipment,false)==shown,"Paused/in-memory restored pose")
				elapsed+=float(state.frameDurationsMs[i])/1000
			check(player.frame("death-water-tread","east",offset+elapsed+3,Vector2.ZERO,equipment,false)==row[5],"Terminal holds beyond finite cycle")
		textures.append_array(row)
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(994,330);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(994,330);bg.color=Color("202a30");view.add_child(bg)
		for i in textures.size():
			var sprite:=Sprite2D.new();sprite.texture=textures[i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2((i%6)*165,(i/6)*165+10);view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-death-water-tread-east-candidate-v1/native-contact.png")==OK,"Native candidate board")
		view.queue_free()
	print("VELD EAST TREAD DEATH PLAYER CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
