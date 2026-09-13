extends SceneTree
## Selected crew gait: distance cadence, independent reference pixels and native scale.
class Review extends Node2D:
	var body: Texture2D
	var helmet: Texture2D
	var travel:=0.0
	var heading:=1.0
	var has_helmet:=true
	var vertical:=false
	func _draw() -> void:
		draw_rect(Rect2(0,0,1000,360),Color("293b40"))
		for col in range(3 if has_helmet else 2):
			var scale:=1.0 if col==0 else 65.28/148.0
			var texture: Texture2D=helmet if col==2 else body
			var start:=80 if heading>0 else 260
			var anchor:=Vector2(start+col*320+heading*fposmod(travel*384*scale/(65.28/148.0),220),290)
			if vertical:
				anchor=Vector2(160+col*320,240+heading*fposmod(travel*384*scale/(65.28/148.0),60))
			draw_line(Vector2(col*320,290),Vector2(col*320+310,290),Color("839597"))
			for mark in range(10):draw_line(Vector2(col*320+mark*32,290),Vector2(col*320+mark*32,297),Color("839597"))
			draw_texture_rect(texture,Rect2(anchor-texture.get_meta("crew_pivot")*scale,texture.get_size()*scale),false)
			draw_string(ThemeDB.fallback_font,Vector2(col*320+8,32),["Source density","Station scale","Fitted helmet"][col],HORIZONTAL_ALIGNMENT_LEFT,-1,16)
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	var args:=OS.get_cmdline_user_args()
	if "fullbody-study" in args:
		await fullbody_study()
		return
	var actor: String=args[0] if not args.is_empty() and args[0] in ["veld","branforth","marsh"] else "veld"
	var direction: String="east"
	for option in ["west","north","south"]:
		if option in args:direction=option
	var state: String="run" if "run" in args else "walk"
	if "carry" in args:state="carry"
	var output: String="res://output/crew-replacement-2026-09-12/%s/%s-native/%s/"%[actor,state,direction]
	for arg in args:
		if arg.begins_with("review-revision="):
			var revision:=arg.trim_prefix("review-revision=")
			assert(revision.is_valid_int() and int(revision)>0,"Review revision must be a positive integer")
			output=output.trim_suffix("/")+"-revision-"+str(int(revision))+"/"
	var reference_label: String=direction if state=="walk" else state+"-"+direction
	var reference_root: String="res://character/crew-gait-v2/review/%s-%s-local-01/"%[actor,reference_label]
	if state=="carry":reference_root="res://character/crew-action-detail-v2/review/marsh-carry-"+direction+"-local-01/"
	var rig: Dictionary
	if actor in ["veld","branforth"] and state=="walk" and direction in ["south","north"]:
		rig={"recipe":{"durations":[170,130,150,170,130,150]},"strideDistanceCells":0.12 if actor=="veld" else 0.128}
	else:
		rig=JSON.parse_string(FileAccess.get_file_as_string(reference_root+("recipe.json" if state=="carry" else "rig.json")))
	root.size=Vector2i(1000,360);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=grid.get(actor+"_player")
	if not player.strides.has(state+"-"+direction):
		push_error("Selected gait stride override is missing: "+actor+" "+state+"-"+direction)
		grid.free();quit(1);return
	var references: Array=[]
	var helmet_references: Array=[]
	var identity_corrected: bool=actor=="veld" and direction in ["east","west","south","north"] and state=="walk"
	var identity_root: String="res://character/veld-identity-correction-v1/review/"+("east-chain-01/" if direction=="east" else "directional-movement-01/")
	var whole_body: bool=actor=="veld" and direction in ["east","west","south","north"] and state=="walk"
	if whole_body:identity_root="res://character/veld-identity-correction-v1/review/"+("walk-video-cycle-01/" if direction=="east" else "walk-"+direction+"-video-cycle-01/")
	if actor=="branforth" and direction in ["east","west","north","south"] and state=="walk":
		whole_body=true
		identity_corrected=true
		identity_root="res://character/branforth-motion-polish-v1/review/walk-"+direction+"-video-cycle-01/"
		if direction=="west":identity_root="res://character/branforth-motion-polish-v1/review/walk-west-video-cycle-02/"
	if actor=="marsh" and direction in ["east","west","north","south"] and state=="walk":
		whole_body=true
		identity_corrected=true
		identity_root="res://character/marsh-motion-polish-v1/review/walk-"+direction+"-video-cycle-01/"
	var preservation_failures:=0
	var durations: Array=rig.recipe.durations
	if actor=="branforth" and state=="walk" and direction=="west":durations=[130,170,150,200,150,100]
	var cycle:=0.0
	for duration in durations:cycle+=float(duration)/1000.0
	for i in range(durations.size()):
		var image:=Image.new()
		if not whole_body:image.load_png_from_buffer(FileAccess.get_file_as_bytes(reference_root+("carry-" if state=="carry" else "")+"%03d.png"%i))
		if identity_corrected:
			var corrected:=Image.new()
			corrected.load_png_from_buffer(FileAccess.get_file_as_bytes(identity_root+"walk-%s-%03d.png"%[direction,i]))
			corrected=corrected.get_region(Rect2i(36,52,184,184))
			if not whole_body and image.get_region(Rect2i(0,68,184,116)).get_data()!=corrected.get_region(Rect2i(0,68,184,116)).get_data():
				preservation_failures+=1;push_error("Identity edit changed original gait below collar")
			image=corrected
			if actor!="marsh":
				var fitted:=Image.new()
				fitted.load_png_from_buffer(FileAccess.get_file_as_bytes(identity_root+"helmet-walk-%s-%03d.png"%[direction,i]))
				helmet_references.append(fitted.get_region(Rect2i(36,52,184,184)))
		references.append(image)
	var stride: float=rig.strideDistanceCells
	if whole_body and direction in ["east","west"]:stride=(102.0 if direction=="east" else 108.0)*65.28/148.0/384.0
	if whole_body and actor=="branforth":stride=(106.0 if direction=="east" else 108.0)*65.28/148.0/384.0 if direction in ["east","west"] else 0.128
	if whole_body and actor=="marsh":stride=(96.0 if direction=="east" else 126.0)*65.28/148.0/384.0 if direction in ["east","west"] else 0.128
	var failures:=preservation_failures
	if not is_equal_approx(player.strides[state+"-"+direction],stride):failures+=1;push_error("Selected stride differs from source rig")
	if actor=="marsh" and not player.equipment_frames.get("diving-helmet",{}).is_empty():failures+=1;push_error("Marsh must remain without helmet variants")
	var review:=Review.new();review.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(review)
	review.heading=1.0 if direction in ["east","south"] else -1.0
	review.vertical=direction in ["north","south"]
	review.has_helmet=actor!="marsh"
	DirAccess.make_dir_recursive_absolute(output)
	for i in range(60):
		var distance:=i*.04*(.14 if state=="run" else .08)
		var position:=Vector2(0,distance*review.heading) if review.vertical else Vector2(distance*review.heading,0)
		review.body=player.frame(state,direction,i*.04,position)
		review.helmet=player.frame(state,direction,i*.04,position,"diving-helmet") if review.has_helmet else review.body
		# Vector2 stores the actual supplied position at engine precision. Using
		# the unrounded scalar can predict the other side of an exact boundary.
		var elapsed:=fposmod(position.length()/stride*cycle,cycle);var index:=0
		for slot in range(durations.size()-1):
			var duration: float=float(durations[slot])/1000.0
			if elapsed<duration:break
			elapsed-=duration;index+=1
		if review.body.get_image().get_data()!=references[index].get_data():failures+=1;push_error("Selected walk differs at sample "+str(i))
		if identity_corrected and review.has_helmet and review.helmet.get_image().get_data()!=helmet_references[index].get_data():failures+=1;push_error("Selected fitted identity differs at sample "+str(i))
		review.travel=distance;review.queue_redraw()
		await process_frame;await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(output+"frame-%03d.png"%i)
	grid.free()
	print("CREW WALK NATIVE: %s %s %s: 60 selected distance-driven samples, %d failures"%[actor,state,direction,failures])
	quit(1 if failures else 0)

func fullbody_study() -> void:
	var base: String="res://character/veld-identity-correction-v1/review/walk-east-fullbody-01/"
	var video_study: bool="video-cycle" in OS.get_cmdline_user_args()
	if video_study:
		base="res://character/veld-identity-correction-v1/review/walk-video-cycle-01/"
	var recipe: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(base+"registration.json"))
	var player=preload("res://scripts/crew_sprite_player.gd").new()
	var frames: Array=[]
	for i in range(6):
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes(base+"walk-east-%03d.png"%i))!=OK:quit(1);return
		var texture:=ImageTexture.create_from_image(image)
		texture.set_meta("crew_pivot",Vector2(128,224));texture.set_meta("crew_standing_height",148.0)
		frames.append(texture)
	player.frames["walk-east"]=frames
	player.timing["walk-east"]={"durations":recipe.durations,"loop":true,"seconds":0.9}
	var view:=Review.new();view.has_helmet=false;root.size=Vector2i(1000,360)
	root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
	root.add_child(view)
	var study_strides: Array=[76.0,122.0]
	if video_study:study_strides=[76.0,102.0,122.0]
	for stride in study_strides:
		var out: String="res://output/crew-replacement-2026-09-12/veld/fullbody-walk-study-%d/"%int(stride)
		if video_study:
			out="res://output/crew-replacement-2026-09-12/veld/video-walk-study-%d/"%int(stride)
		if DirAccess.make_dir_recursive_absolute(out)!=OK:quit(1);return
		player.strides={"walk":stride*65.28/148.0/384.0}
		player.current_key="";player.last_time=-1
		var trace: Array=[]
		for i in range(90):
			var seconds: float=i*0.025
			# Same actor speed in both studies; only stride/cadence differs.
			var distance: float=seconds*0.1
			view.body=player.frame("walk","east",seconds,Vector2(distance,0));view.travel=distance
			view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			if root.get_texture().get_image().save_png(out+"frame-%03d.png"%i)!=OK:quit(1);return
			trace.append({"time":seconds,"distanceCells":distance,"slot":frames.find(view.body),"strideSourcePixels":stride})
		FileAccess.open(out+"trace.json",FileAccess.WRITE).store_string(JSON.stringify(trace,"\t"))
	print("FULLBODY WALK STUDY: %d native distance-driven captures at equal movement speed; visual/contact acceptance pending"%(90*study_strides.size()))
	quit(0)
