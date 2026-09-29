extends RefCounted
## Selected animation layers. Sampling never changes jobs, rewards or movement.
const MANIFESTS={"construction":"res://assets/drone-runtime-2026-09-26/construction.json","mining":"res://assets/drone-runtime-2026-09-26/mining.json","salvage":"res://assets/drone-runtime-2026-09-26/salvage.json"}
const HEADINGS=["east","southeast","south","southwest","west","northwest","north","northeast"]
static var catalogs:Dictionary={}
static var textures:Dictionary={}
static var texture_order:Array[String]=[]
static var texture_bytes:Dictionary={}
static var last_used:Dictionary={}
static var cached_bytes:=0
const CACHE_BUDGET=268435456
static var active_canvas:CanvasItem
static var image_jobs:Dictionary={}
static func request_texture(path:String) -> void:
	if textures.has(path) or image_jobs.has(path): return
	var result:Dictionary={}
	var task:=WorkerThreadPool.add_task(func():
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK:
			result.image=image
			result.invisible=image.is_invisible())
	image_jobs[path]={"task":task,"result":result}

static func finish_texture(path:String) -> bool:
	if textures.has(path): return true
	if not image_jobs.has(path): request_texture(path); return false
	var job:Dictionary=image_jobs[path]
	if not WorkerThreadPool.is_task_completed(job.task): return false
	WorkerThreadPool.wait_for_task_completion(job.task)
	image_jobs.erase(path)
	if not job.result.has("image"):
		push_error("Drone animation missing: "+path)
		return false
	cache_image(path,job.result.image,job.result.invisible)
	return true

static func cache_image(path:String,image:Image,invisible:bool=false) -> void:
	# Empty placeholder layers can be enormous atlases. Their pixels never
	# contribute to a frame, so keep one transparent pixel and skip atlas draws.
	if invisible:
		image=Image.create(1,1,false,Image.FORMAT_RGBA8)
		image.fill(Color(0,0,0,0))
	var bytes:=image.get_data_size()
	while cached_bytes+bytes>CACHE_BUDGET and not texture_order.is_empty():
		var oldest:String=texture_order[0]
		if int(last_used.get(oldest,0))>=Engine.get_process_frames()-2:break
		texture_order.pop_front()
		cached_bytes-=int(texture_bytes[oldest]);textures.erase(oldest);texture_bytes.erase(oldest)
	textures[path]=ImageTexture.create_from_image(image)
	textures[path].set_meta("drone_invisible",invisible)
	texture_bytes[path]=bytes;cached_bytes+=bytes
	last_used[path]=Engine.get_process_frames()
	texture_order.erase(path);texture_order.append(path)
static func begin(canvas:CanvasItem) -> void:
	active_canvas=canvas
	if int(canvas.get_meta("drone_texture_frame",-1))!=Engine.get_process_frames():
		canvas.set_meta("drone_texture_frame",Engine.get_process_frames())
		canvas.set_meta("drone_texture_pins",{})
static func catalog(kind:String) -> Dictionary:
	if not catalogs.has(kind):catalogs[kind]=JSON.parse_string(FileAccess.get_file_as_string(MANIFESTS[kind]))
	return catalogs[kind]
static func texture(path:String) -> Texture2D:
	if not textures.has(path):
		var image:=Image.new()
		var invisible:=false
		if image_jobs.has(path):
			var job:Dictionary=image_jobs[path]
			WorkerThreadPool.wait_for_task_completion(job.task)
			image_jobs.erase(path)
			assert(job.result.has("image"),"Drone animation missing: "+path)
			image=job.result.get("image",image)
			invisible=job.result.get("invisible",false)
		else:
			var error:=image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
			assert(error==OK,"Drone animation missing: "+path)
			invisible=image.is_invisible()
		cache_image(path,image,invisible)
	last_used[path]=Engine.get_process_frames()
	texture_order.erase(path);texture_order.append(path)
	if is_instance_valid(active_canvas):active_canvas.get_meta("drone_texture_pins")[path]=textures[path]
	return textures[path]
static func heading(direction:Vector2) -> String:
	return HEADINGS[posmod(roundi(direction.angle()/(PI/4)),8)] if direction.length_squared()>.00001 else "south"
static func cardinal(value:String) -> String:
	return {"northeast":"north","northwest":"north","southeast":"south","southwest":"south"}.get(value,value)
static func sample(d:Dictionary,operating:bool=true) -> Dictionary:
	var kind:String=d.get("kind","construction")
	var m:=catalog(kind)
	var facing:String=d.get("animation_heading","south")
	var phase:String=d.get("phase","docked")
	var clock:float=float(d.get("clock",0))
	var elapsed:float=maxf(0,clock-float(d.get("animation_started",clock))) if d.get("animation_phase",phase)==phase else 0.0
	var state:="idle"
	var fraction:=-1.0
	var loaded:bool=not d.get("cargo",{}).is_empty()
	var lamp:="operational"
	if not operating:state="disabled";lamp="charging"
	elif d.get("route_wait",false):state="blocked";lamp="stopped"
	elif phase in ["outbound","returning"]:
		state="move" if kind=="construction" else "carry" if loaded else "drive" if kind=="mining" else "swim"
		if kind!="construction":
			var goal:Vector2=Vector2(d.get("home",Vector2.ZERO)) if phase=="returning" else Vector2(d.get("target",Vector2.ZERO))
			var left:float=Vector2(d.get("position",goal)).distance_to(goal)/1.5
			if elapsed<.2:state="start";fraction=clampf(elapsed/.2,0,1)
			elif left<.2:state="stop";fraction=1.0-clampf(left/.2,0,1)
			elif kind=="mining" and clock-float(d.get("animation_turn_started",-10))<.25:
				var prior:int=HEADINGS.find(d.get("animation_previous_heading",facing))
				state="steer-right" if posmod(HEADINGS.find(facing)-prior,8)<4 else "steer-left"
				fraction=clampf((clock-float(d.animation_turn_started))/.25,0,1)
	elif phase=="working":
		facing=cardinal(facing)
		var duration:float=maxf(.01,float(d.get("animation_work_duration",6)))
		fraction=clampf(elapsed/duration,0,1)
		if kind=="construction":state="job-weld"
		elif kind=="salvage":state="retrieve"
		else:
			var collection:=minf(4,duration*.5)
			if elapsed>=duration-collection:state="collect";fraction=clampf((elapsed-duration+collection)/collection,0,1)
			else:state="mine";fraction=-1
	elif phase=="docked":
		if float(d.get("battery",12))<11.999:state="charging";lamp="charging"
		elif d.get("job","").is_empty():lamp="stopped"
	elif phase=="docking" and loaded:
		state="unload" if kind=="mining" else "release" if kind=="salvage" else "idle"
		facing=cardinal(facing);fraction=clampf(float(d.get("elapsed",0))/1.2,0,1)
	var key:=state+"-"+facing
	if not m.states.has(key):key=state+"-"+cardinal(facing)
	if not m.states.has(key):key="idle-"+facing
	var clip:Dictionary=m.states[key]
	var count:=int(clip.frameCount)
	var index:int=mini(count-1,int(fraction*count)) if fraction>=0 else posmod(int(clock*float(clip.fps)),count) if clip.get("loop",false) else mini(count-1,int(elapsed*float(clip.fps)))
	if not operating:index=0
	return {"clip":clip,"frame":index,"heading":key.trim_prefix(state+"-") if key.begins_with(state+"-") else facing,"state":state,"lamp":lamp,"loaded":loaded,"time":clock}
# A layer whose sheet is still decoding is skipped for a frame or two; decoding it on the main thread
# cost 44-219 ms per new animation state (owner lag reports, Sept 29).
static func ready(path:String) -> bool:
	return textures.has(path) or finish_texture(path)
static func atlas(canvas:CanvasItem,record:Dictionary,index:int,rect:Rect2,size:Vector2,tint:Color) -> void:
	if not ready(record.path): return
	var atlas_texture:=texture(record.path)
	if atlas_texture.get_meta("drone_invisible",false): return
	var columns:=int(record.columns)
	canvas.draw_texture_rect_region(atlas_texture,rect,Rect2(Vector2(index%columns,index/columns)*size,size),tint)
static func draw(canvas:CanvasItem,d:Dictionary,at:Vector2,world_scale:float,art_scale:float,operating:bool,visual_clock:float,alpha:float=1.0) -> void:
	begin(canvas)
	var kind:String=d.get("kind","construction")
	var m:=catalog(kind);var s:=sample(d,operating);var clip:Dictionary=s.clip
	var size:=Vector2(m.frameWidth,m.frameHeight)
	var scale_value:=float(m.worldUnitsPerPixel)*world_scale*art_scale
	var pivot:=Vector2(m.pivot[0],m.pivot[1])
	var offset:=Vector2.ZERO
	if clip.has("rootOffsets"):
		var v:Array=clip.rootOffsets[s.frame];offset=Vector2(v[0],v[1])*scale_value
	var rect:=Rect2(at-pivot*scale_value+offset,size*scale_value)
	var tint:=Color(1,1,1,alpha)
	var meta:Dictionary=m.headings[s.heading]
	if kind=="salvage" and clip.has("cargoAtlas"):atlas(canvas,clip.cargoAtlas,s.frame,rect,size,tint)
	if kind=="salvage" and s.loaded and s.state not in ["retrieve","release"]:
		if ready(meta.cargoPose):canvas.draw_texture_rect(texture(meta.cargoPose),rect,false,tint)
		if ready(meta.closedPose):canvas.draw_texture_rect(texture(meta.closedPose),rect,false,tint)
	else:atlas(canvas,clip.atlas,s.frame,rect,size,tint)
	if kind=="mining":
		var circumference:float=maxf(.01,float(meta.tyreTravelWorldUnitsPerSecond)*2*art_scale)
		var wheel:=posmod(int(float(d.get("animation_distance",0))/circumference*60),60)
		atlas(canvas,meta.wheelAtlas,wheel,rect,size,tint)
		if clip.has("cargoAtlas"):atlas(canvas,clip.cargoAtlas,s.frame,rect,size,tint)
		elif s.loaded and ready(meta.cargoPose):canvas.draw_texture_rect(texture(meta.cargoPose),rect,false,tint)
	elif kind=="salvage":
		var rotor:=posmod(int(float(d.get("animation_rotor",0))),60)
		atlas(canvas,meta.rotorAtlas,rotor,rect,size,tint)
	if clip.has("effectAtlas"):atlas(canvas,clip.effectAtlas,s.frame,rect,size,tint)
	if kind=="construction" and clip.has("cargoAtlas"):atlas(canvas,clip.cargoAtlas,s.frame,rect,size,tint)
	var mark:Array=clip.get("lamp",meta.lamp)
	var lamp_at:=rect.position+Vector2(mark[0],mark[1])*scale_value
	var color:Color={"operational":Color("309bff"),"stopped":Color("ff302e"),"charging":Color("ffcd2d")}[s.lamp]
	color.a=alpha*(.25+.75*pow(.5+.5*cos(visual_clock*TAU/.85),3))
	canvas.draw_circle(lamp_at,maxf(.6*world_scale,2.4*scale_value),color)
