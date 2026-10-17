extends SceneTree
## Native candidate-only playback. Run exclusively with isolated APPDATA.
const MANIFESTS = {"v12":"res://character/veld-animation-pilot-v12/manifest.json","v11":"res://character/veld-animation-pilot-v11/manifest.json","v10":"res://character/veld-animation-pilot-v10/manifest.json","v9":"res://character/veld-animation-pilot-v9/manifest.json","v8":"res://character/veld-animation-pilot-v8/manifest.json","v7":"res://character/veld-animation-pilot-v7/manifest.json","v6":"res://character/veld-animation-pilot-v6/manifest.json","v5":"res://character/veld-animation-pilot-v5/manifest.json","v3":"res://character/veld-animation-pilot-v3/manifest.json","v4":"res://character/veld-animation-pilot-v4/manifest.json"}
const OUTPUTS = {"v12":"res://character/veld-animation-pilot-v12/native-review","v11":"res://character/veld-animation-pilot-v11/native-review","v10":"res://character/veld-animation-pilot-v10/native-review","v9":"res://character/veld-animation-pilot-v9/native-review","v8":"res://character/veld-animation-pilot-v8/native-review","v7":"res://character/veld-animation-pilot-v7/native-review","v6":"res://character/veld-animation-pilot-v6/native-review","v5":"res://character/veld-animation-pilot-v5/native-review","v3":"res://character/veld-animation-pilot-v3/native-review","v4":"res://character/veld-animation-pilot-v4/native-review"}
var checks := 0
var failures := 0
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
class Review extends Node2D:
	var player
	var walk: Texture2D
	var west_walk: Texture2D
	var elapsed := 0.0
	var travel := 0.0
	var west_travel := 0.0
	func _draw() -> void:
		draw_rect(Rect2(0,0,1560,700),Color("192127"))
		draw_string(ThemeDB.fallback_font,Vector2(30,35),"VELD / NATIVE SPRITE PLAYER / CANDIDATE",HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
		for row in range(2):
			var k: float = 1.0 if row == 0 else 45.0/148.0
			var baseline: float = 290.0 if row == 0 else 500.0
			for x in range(20,1540 if player.frames.has("walk-west") else 1080,20):
				draw_line(Vector2(x,baseline),Vector2(x,baseline+10),Color("52656d"))
			draw_line(Vector2(20,baseline),Vector2(1540 if player.frames.has("walk-west") else 1080,baseline),Color("84949a"))
			var keys: Array = ["idle-south","idle-east","walk-east","interact-east"] if player.frames.has("idle-east") else ["idle-south","walk-east","interact-east"]
			if player.frames.has("walk-west"):keys.append_array(["idle-west","walk-west"])
			if player.frames.has("idle-north"):keys.append("idle-north")
			for col in range(keys.size()):
				var key: String = keys[col]
				var tex: Texture2D = walk if key=="walk-east" else (west_walk if key=="walk-west" else player.frame_at_elapsed(key,fmod(elapsed,player.cycle_seconds(key))))
				var anchor := Vector2(125+col*(220 if keys.size()==7 else (260 if keys.size()==6 else (275 if keys.size()==4 else 340))),baseline)
				if key=="walk-east":anchor.x+=travel*k
				if key=="walk-west":anchor.x+=(70.0-west_travel)*k
				draw_texture_rect(tex,Rect2(anchor-Vector2(92,172)*k,Vector2(184,184)*k),false)
				draw_string(ThemeDB.fallback_font,Vector2(40+col*(220 if keys.size()==7 else (260 if keys.size()==6 else (275 if keys.size()==4 else 340))),baseline+42),key,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
		draw_string(ThemeDB.fallback_font,Vector2(30,600),"Top: 148 px standing. Bottom: 45 px. Walk uses distance-driven runtime phase.",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	if not FileAccess.file_exists("res://tools/review_veld_pilot.gd.uid"):
		var uid_file=FileAccess.open("res://tools/review_veld_pilot.gd.uid",FileAccess.WRITE)
		uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var revision: String = "v12" if "--v12" in OS.get_cmdline_user_args() else "v11" if "--v11" in OS.get_cmdline_user_args() else "v10" if "--v10" in OS.get_cmdline_user_args() else "v9" if "--v9" in OS.get_cmdline_user_args() else "v8" if "--v8" in OS.get_cmdline_user_args() else "v7" if "--v7" in OS.get_cmdline_user_args() else "v6" if "--v6" in OS.get_cmdline_user_args() else "v5" if "--v5" in OS.get_cmdline_user_args() else ("v4" if "--v4" in OS.get_cmdline_user_args() else "v3")
	var out: String = OUTPUTS[revision]
	DirAccess.make_dir_recursive_absolute(out)
	root.size=Vector2i(1560 if revision in ["v7","v8","v9","v10","v11","v12"] else 1100,700)
	root.content_scale_size=Vector2i.ZERO
	var p=preload("res://scripts/crew_sprite_player.gd").new()
	p.load_manifest(MANIFESTS[revision])
	check(p.frames.size()==(7 if revision in ["v8","v9","v10","v11","v12"] else 6 if revision=="v7" else (3 if revision=="v3" else 4)),"Expected states loaded")
	for key in p.frames:
		var elapsed:=0.0
		for i in range(p.frames[key].size()):
			var duration:float=p.timing[key].durations[i]/1000.0
			check(p.frame_at_elapsed(key,elapsed+duration*.5)==p.frames[key][i],"Frame timing "+key)
			check(p.frames[key][i].get_size()==Vector2(184,184),"Frame dimensions")
			elapsed+=duration
	if revision in ["v5","v6","v7","v8","v9","v10","v11","v12"]:
		for index in [0,5]:
			check(p.frames["interact-east"][index].get_image().get_data()==p.frames["idle-east"][0].get_image().get_data(),"Exact inspection/idle join")
	if revision in ["v5","v6","v7","v8","v9","v10","v11","v12"]:
		check(p.frame_at_elapsed("interact-east",p.cycle_seconds("interact-east")+0.1)==p.frames["idle-east"][0] or p.frame_at_elapsed("interact-east",p.cycle_seconds("interact-east")+0.1).get_image().get_data()==p.frames["idle-east"][0].get_image().get_data(),"Completed inspection holds neutral idle artwork")
	var west_player=preload("res://scripts/crew_sprite_player.gd").new()
	if revision in ["v7","v8","v9","v10","v11","v12"]:
		west_player.load_manifest(MANIFESTS[revision])
		west_player.frame("walk","west",0.0,Vector2.ZERO)
	var sheet=Review.new()
	sheet.player=p
	sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(sheet)
	var cycle:float=p.cycle_seconds("walk-east")
	var capture_span:float=maxf(cycle,p.cycle_seconds("interact-east"))
	var stride:float=p.strides.walk
	p.frame("walk","east",0.0,Vector2.ZERO)
	for i in range(24):
		var t:float=capture_span*(i+0.1)/24.0 # Sample inside frames, away from floating-point boundaries.
		var distance:float=stride*t/cycle
		sheet.elapsed=t
		sheet.travel=distance/.17*148.0
		sheet.walk=p.frame("walk","east",t,Vector2(distance,0))
		check(absf(p.phase-t)<0.000001,"Distance phase error below one microsecond")
		check(sheet.walk==p.frame_at_elapsed("walk-east",fmod(t,cycle)),"Distance-driven phase matches timed frame")
		if revision in ["v7","v8","v9","v10","v11","v12"]:
			var west_distance:float=float(west_player.strides.get("walk-west",stride))*t/cycle
			sheet.west_travel=west_distance/.17*148.0
			sheet.west_walk=west_player.frame("walk","west",t,Vector2(-west_distance,0))
			check(sheet.west_walk==west_player.frame_at_elapsed("walk-west",fmod(t,cycle)),"Leftward distance playback")
		sheet.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(out.path_join("frame-%03d.png"%i))
	var file=FileAccess.open(out.path_join("checks.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":24,"captureDurationMs":roundi(capture_span*1000.0),"scope":"Native sprite-player candidate; no production selection or station occlusion test"},"  "))
	print("VELD NATIVE checks=",checks," failures=",failures)
	quit(1 if failures else 0)
