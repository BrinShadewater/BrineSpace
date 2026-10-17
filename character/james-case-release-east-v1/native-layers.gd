extends SceneTree
const OUT="res://character/james-case-release-east-v1/"
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	check(OS.get_environment("APPDATA").contains("brine-james-native-"),"Scratch APPDATA required")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile required")
	if failures:quit(1);return
	root.size=Vector2i(960,600);root.content_scale_mode=Window.CONTENT_SCALE_MODE_DISABLED
	RenderingServer.set_default_clear_color(Color("303b40"))
	var stage:=Node2D.new();root.add_child(stage)
	var player=preload("res://scripts/crew_sprite_player.gd").new()
	player.load_manifest(OUT+"bare-manifest.json",false,false)
	check(player.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json"),"Paired candidate loads")
	var reg:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"registration.json"))
	var scale82:=82.0/148.0
	var cases:=[];var bodies:=[];var anchors:=[]
	for i in range(2):
		var anchor:=Vector2(300,190+i*190);anchors.append(anchor)
		var body:=Sprite2D.new();body.centered=false;body.scale=Vector2.ONE*scale82;body.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;stage.add_child(body);bodies.append(body)
		var c:=Sprite2D.new();c.centered=false;c.texture=ImageTexture.create_from_image(Image.load_from_file(OUT+"case.png"));c.scale=Vector2.ONE*scale82;c.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;c.position=anchor+(Vector2(reg.casePosition[0],reg.casePosition[1])-Vector2(128,128))*scale82;stage.add_child(c);cases.append(c)
		var label:=Label.new();label.text=("bare" if i==0 else "helmet")+" / native82 / staged independent layers";label.position=Vector2(20,140+i*190);stage.add_child(label)
	var durations:Array=[50,80,60,80,80,70,60];var elapsed:=0.0;var captures:=[]
	for slot in range(7):
		for i in range(2):
			var gear:String="" if i==0 else "diving-helmet"
			var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+("bare" if i==0 else "helmet")+"-manifest.json"))
			var f:String=OUT.path_join(manifest.states[0].frameFiles[slot])
			var texture:Texture2D=player.frame_at_elapsed("swim-case-release-east",elapsed+.000001,gear)
			check(texture!=null,"Candidate source exists")
			if texture==null:continue
			check(texture.get_image().get_data()==Image.load_from_file(f).get_data(),"Native source boundary matches declared slot")
			bodies[i].texture=texture
			bodies[i].position=anchors[i]-Vector2(128,128)*scale82-Vector2(72*elapsed/(384*.17/148)*scale82,0)
			check(cases[i].position==anchors[i]+(Vector2(reg.casePosition[0],reg.casePosition[1])-Vector2(128,128))*scale82,"Case position stays independent of moving body")
			if slot>0:check(bodies[i].position.x<anchors[i].x-128*scale82,"Body moves during finite release")
		await process_frame;await RenderingServer.frame_post_draw
		var file:String="native-layer-%02d.png"%slot
		check(root.get_texture().get_image().save_png(OUT+file)==OK,"Native capture saved")
		captures.append({"file":file,"slot":slot,"elapsed":elapsed,"casePositions":[[cases[0].position.x,cases[0].position.y],[cases[1].position.x,cases[1].position.y]]})
		elapsed+=float(durations[slot])/1000.0
	for gear in ["","diving-helmet"]:
		var a:Texture2D=player.frame_at_elapsed("swim-case-release-east",elapsed+.000001,gear)
		var b:Texture2D=player.frame_at_elapsed("swim-case-release-east",elapsed*3,gear)
		check(a==b,"Finite source holds exact empty terminal")
	var evidence={"checks":checks,"failures":failures,"durationSeconds":elapsed,"resolvedUserDataDir":OS.get_user_data_dir(),"scratchAppData":OS.get_environment("APPDATA"),"captures":captures,"scope":"Native CrewSpritePlayer paired staged seven-slot sources and independent Sprite2D case/body positions at82px ruler. Offline return translation; no normal expedition dispatch/world-save/Continue/persistence/obstruction proof."}
	var stream:=FileAccess.open(OUT+"native-layers-evidence.json",FileAccess.WRITE);stream.store_string(JSON.stringify(evidence,"\t"));stream.close()
	stage.free();print("JAMES RELEASE LAYERS: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
