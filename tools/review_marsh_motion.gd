extends SceneTree
## Interactive native review of authored timing against the frozen pre-repair art.
class Review extends Node2D:
	var player
	var contract: Dictionary
	var baseline: Dictionary
	var groups: Array
	var group_index: int=0
	var elapsed: float=0.0
	var running:=true
	var old_textures: Dictionary={}
	var selected: Array=[]
	var capture:=false
	var capture_busy:=false
	var signature: String=""
	var samples: Array=[]
	var capture_index:=0
	var wall_started: int=0
	var group_started: int=0
	const CAPTURE_ROOT="res://output/marsh-animation-audit/motion-review/"
	func segment_seconds(key: String) -> float:
		if key.begins_with("idle-"):return player.cycle_seconds(key)*2.0
		return player.cycle_seconds(key)*(2.0 if contract[key].loop else 1.0)+(.8 if key.begins_with("death-") else 0.0)
	func _process(delta: float) -> void:
		if capture_busy:return
		if capture:elapsed=float(Time.get_ticks_msec()-group_started)/1000.0
		elif running:elapsed+=delta
		var longest:=0.0
		selected=[]
		for column in groups[group_index].columns:
			var total:=0.0
			for key in column.keys:total+=segment_seconds(key)
			longest=maxf(longest,total)
			var cursor:=fposmod(elapsed,total)
			var key: String=column.keys.back()
			for candidate in column.keys:
				key=candidate
				if cursor<segment_seconds(key):break
				cursor-=segment_seconds(key)
			var spec: Dictionary=contract[key]
			var phase: float=fposmod(cursor,player.cycle_seconds(key)) if spec.loop else minf(cursor,player.cycle_seconds(key)-.00001)
			var slot:=0
			var cumulative:=0.0
			for duration in spec.durations:
				cumulative+=float(duration)/1000.0
				if phase<cumulative:break
				slot+=1
			slot=mini(slot,spec.files.size()-1)
			var path: String=baseline[key].files[slot]
			if not old_textures.has(path):
				var im:=Image.new();im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://"+path));old_textures[path]=ImageTexture.create_from_image(im)
			selected.append({"label":column.label,"key":key,"slot":slot,"spec":spec,"new":player.frame_at_elapsed(key,phase),"old":old_textures[path]})
		queue_redraw()
		if capture:
			var current:=str(group_index)+":"+str(selected.map(func(s):return [s.key,s.slot]))
			if signature!=current:
				signature=current;capture_busy=true;save_sample.call_deferred()
			elif elapsed>=longest:
				group_index+=1;elapsed=0;signature="";group_started=Time.get_ticks_msec()
				if group_index>=groups.size():
					var file:=FileAccess.open(CAPTURE_ROOT+"samples.json",FileAccess.WRITE)
					file.store_string(JSON.stringify({"samples":samples,"groups":groups.size(),"wallSeconds":float(Time.get_ticks_msec()-wall_started)/1000.0,"policy":"Advancing native scene clock; captures when selected poses change; two cycles of authored loops. Before/after source and revised station size."},"\t"));file.close()
					print("MARSH LIVE MOTION: ",groups.size()," groups / ",capture_index," pose-change captures")
					get_tree().quit()
	func save_sample() -> void:
		await RenderingServer.frame_post_draw
		var prefix: String="supplement" if "--supplement" in OS.get_cmdline_user_args() else "group"
		var filename: String=prefix+"-%02d-%04d.png"%[group_index,capture_index]
		get_tree().root.get_texture().get_image().save_png(CAPTURE_ROOT+filename)
		samples.append({"group":group_index,"title":groups[group_index].title,"elapsed":elapsed,"wallMsec":Time.get_ticks_msec()-wall_started,"file":filename,"poses":selected.map(func(s):return {"key":s.key,"slot":s.slot})})
		capture_index+=1;capture_busy=false
	func _unhandled_key_input(event: InputEvent) -> void:
		if not event.is_pressed():return
		if event.keycode==KEY_RIGHT:group_index=(group_index+1)%groups.size();elapsed=0
		elif event.keycode==KEY_LEFT:group_index=posmod(group_index-1,groups.size());elapsed=0
		elif event.keycode==KEY_SPACE:running=not running
		elif event.keycode==KEY_R:elapsed=0
		elif event.keycode==KEY_ESCAPE:get_tree().quit()
	func _draw() -> void:
		if group_index>=groups.size():return
		draw_rect(Rect2(0,0,1280,720),Color("293b40"))
		draw_string(ThemeDB.fallback_font,Vector2(16,24),"Marsh: "+groups[group_index].title+" | Left/Right: group | Space: pause | R: restart | Esc: close",HORIZONTAL_ALIGNMENT_LEFT,-1,18)
		for c in range(selected.size()):
			var s: Dictionary=selected[c];var x: float=160+c*320
			draw_string(ThemeDB.fallback_font,Vector2(x-145,52),s.key+" / frame "+str(s.slot),HORIZONTAL_ALIGNMENT_LEFT,-1,16)
			for row in range(3):
				var scale: float=65.28/float(s.spec.standingHeight) if row==2 else 1.0
				var anchor:=Vector2(x,232+row*220)
				var tex: Texture2D=s.old if row==1 else s.new
				draw_line(anchor-Vector2(145,0),anchor+Vector2(145,0),Color("839597"))
				draw_string(ThemeDB.fallback_font,anchor+Vector2(-145,22),["After / source size","Before / source size","After / station size"][row],HORIZONTAL_ALIGNMENT_LEFT,-1,14)
				draw_texture_rect(tex,Rect2(anchor-Vector2(s.spec.pivot[0],s.spec.pivot[1])*scale,tex.get_size()*scale),false)
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	root.title="Marsh motion review"
	root.size=Vector2i(1280,720);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
	var view:=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	view.contract=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-consistency-review-v1/runtime-contract.json")).states
	view.baseline=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-master-repair-v1/baseline-contract.json")).states
	view.groups=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-consistency-review-v1/groups.json"))
	var supplements: Array=[]
	for family in ["cargo-unload","salvage"]:
		var columns: Array=[]
		for d in ["south","north","east","west"]:columns.append({"label":d,"keys":["idle-"+d,family+"-"+d,"idle-"+d]})
		supplements.append({"title":family+" supplemental","columns":columns})
	var travel_columns: Array=[]
	for d in ["east","west"]:travel_columns.append({"label":d,"keys":["idle-"+d,"walk-start-"+d,"walk-step-"+d,"walk-stop-"+d,"idle-"+d]})
	supplements.append({"title":"Travel handoffs supplemental","columns":travel_columns})
	if "--supplement" in OS.get_cmdline_user_args():view.groups=[view.groups[0]]+supplements
	else:view.groups.append_array(supplements)
	view.player=load("res://scripts/crew_sprite_player.gd").new()
	var catalog: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-v2/catalog.json"))
	for path in catalog.body:view.player.load_manifest("res://character/marsh-v2/"+str(path),true)
	view.capture="--capture" in OS.get_cmdline_user_args();view.wall_started=Time.get_ticks_msec();view.group_started=view.wall_started
	if view.capture:DirAccess.make_dir_recursive_absolute(Review.CAPTURE_ROOT)
	root.add_child(view)
