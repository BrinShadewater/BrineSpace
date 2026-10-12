extends RefCounted
## Selected animation layers. Sampling never changes jobs, rewards or movement.
const MANIFESTS={"construction":"res://assets/drone-runtime-2026-09-26/construction.json","mining":"res://assets/drone-runtime-2026-09-26/mining.json","salvage":"res://assets/drone-runtime-2026-09-26/salvage.json"}
const Routes=preload("res://scripts/drone_routes.gd")
const HEADINGS=["east","southeast","south","southwest","west","northwest","north","northeast"]
static var catalogs:Dictionary={}
static var textures:Dictionary={}
static var texture_order:Array[String]=[]
static var texture_bytes:Dictionary={}
static var last_used:Dictionary={}
static var cached_bytes:=0
# Reconnect images still owned by retained canvases without owning their lifetime.
static var weak_images:Dictionary={}
# Keep only byte-proven transparent 1x1 layers; released with the loaded session.
static var invisible_images:Dictionary={}
const INVISIBLE_IMAGE_LIMIT:=64
static var trim_calls:=0
static var trim_removed:=0
const CACHE_BUDGET=268435456
static var active_canvas:CanvasItem
static var image_jobs:Dictionary={}
static var texture_uploads := 0
static var texture_upload_usec := 0
static var last_texture_upload := {}
const FRAME_UPLOAD_EVENT_LIMIT := 8
static var upload_frame := -1
static var frame_upload_count := 0
static var frame_upload_bytes := 0
static var frame_upload_usec := 0
static var frame_upload_max_usec := 0
static var frame_upload_largest_bytes := 0
static var frame_upload_events: Array[Dictionary] = []
static func frame_upload_diagnostics(requested_frame: int = -1) -> Dictionary:
	var current := Engine.get_process_frames() if requested_frame < 0 else requested_frame
	if current != upload_frame:
		return {"frame": current, "uploads": 0, "bytes": 0, "usec": 0,
			"max_usec": 0, "largest_bytes": 0, "events": [], "events_complete": true}
	return {"frame": current, "uploads": frame_upload_count, "bytes": frame_upload_bytes,
		"usec": frame_upload_usec, "max_usec": frame_upload_max_usec,
		"largest_bytes": frame_upload_largest_bytes, "events": frame_upload_events.duplicate(true),
		"events_complete": frame_upload_count <= FRAME_UPLOAD_EVENT_LIMIT}
static func record_frame_upload(event: Dictionary) -> void:
	if upload_frame != int(event.frame):
		upload_frame = int(event.frame)
		frame_upload_count = 0
		frame_upload_bytes = 0
		frame_upload_usec = 0
		frame_upload_max_usec = 0
		frame_upload_largest_bytes = 0
		frame_upload_events.clear()
	frame_upload_count += 1
	frame_upload_bytes += int(event.bytes)
	frame_upload_usec += int(event.usec)
	frame_upload_max_usec = maxi(frame_upload_max_usec, int(event.usec))
	frame_upload_largest_bytes = maxi(frame_upload_largest_bytes, int(event.bytes))
	if frame_upload_events.size() < FRAME_UPLOAD_EVENT_LIMIT:
		frame_upload_events.append(event)
static func cache_diagnostics() -> Dictionary:
	# Reports only: inspect allocation bookkeeping, never read GPU images or evict.
	var recent_bytes := 0
	var stale_bytes := 0
	var visited := 0
	var frame := Engine.get_process_frames()
	for path in texture_bytes:
		if visited >= 4096: break
		visited += 1
		if int(last_used.get(path, -100)) >= frame - 2: recent_bytes += int(texture_bytes[path])
		else: stale_bytes += int(texture_bytes[path])
	# F8/stall reports only: weak lookups distinguish retained live storage from
	# ordinary cache ownership. Metadata only; never read back pixels or hold images.
	var live_bytes:=0
	var encoded_original_bytes:=0
	var uncached_live_bytes:=0
	var live_ids:Dictionary={}
	var live_details:Array[Dictionary]=[]
	var weak_visited:=0
	for path in weak_images:
		if weak_visited>=4096:break
		weak_visited+=1
		var entry:Dictionary=weak_images[path]
		var image:Texture2D=entry.ref.get_ref()
		if image==null:continue
		var id:int=image.get_instance_id()
		if live_ids.has(id):continue
		live_ids[id]=true
		if image is NativeEffect or image is CargoStorage:encoded_original_bytes+=image.original_png.size()
		var bytes:int=entry.bytes
		live_bytes+=bytes
		var cache_owned:bool=textures.has(path) and is_same(textures[path],image)
		if not cache_owned:uncached_live_bytes+=bytes
		if live_details.size()<64:
			live_details.append({"path":path,"bytes":bytes,"size":image.get_size(),
				"cache_owned":cache_owned,"last_use_age_frames":frame-int(last_used.get(path,-100))})
	return {"cargo_storage":cargo_storage_enabled,"cargo_storage_sources":cargo_storage.size(),"cargo_frame_draws":cargo_frame_draws,"cargo_fallback_draws":cargo_fallback_draws,"native_encoded_original_bytes":encoded_original_bytes,"native_mask_draws":native_mask_draws,"native_fallback_draws":native_fallback_draws,"native_mask_sources":effect_storage.size(),"native_effect_storage":native_effect_storage,"cached_decoded_bytes": cached_bytes, "budget_bytes": CACHE_BUDGET,
		"over_budget_bytes": maxi(0, cached_bytes - CACHE_BUDGET), "entries": textures.size(),
		"recent_decoded_bytes": recent_bytes, "stale_decoded_bytes": stale_bytes,
		"classified_entries": visited, "classification_complete": visited == texture_bytes.size(),
		"weak_image_entries":weak_images.size(),"stale_lookup_removals":trim_removed,
		"observed_live_unique_images":live_ids.size(),"observed_live_decoded_bytes":live_bytes,
		"observed_uncached_live_decoded_bytes":uncached_live_bytes,"observed_live_details":live_details,
		"live_lookup_entries_inspected":weak_visited,"live_lookup_scan_complete":weak_visited==weak_images.size(),
		"live_details_complete":live_details.size()==live_ids.size(),
		"live_scope":"Currently live images reachable through bounded weak lookups; decoded storage, not total GPU residency. Details capped at 64, lookup scan at 4096.",
		"uploads": texture_uploads, "upload_usec": texture_upload_usec,
		"frame_uploads": frame_upload_diagnostics(),
		"latest_upload_frame": frame_upload_diagnostics(upload_frame),
		"scope": "Cache bookkeeping; recent means touched within two frames, not GPU residency or an eviction instruction"}
static func request_texture(path:String) -> void:
	if textures.has(path) or restore_live(path) or image_jobs.has(path): return
	var result:Dictionary={}
	var task:=WorkerThreadPool.add_task(func():
		var image:Image=load_native_or_original(path)
		if image!=null:
			result.image=image
			result.invisible=image.is_invisible())
	image_jobs[path]={"task":task,"result":result}

static func finish_texture(path:String) -> bool:
	if textures.has(path) or restore_live(path): return true
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
	var upload_started := Time.get_ticks_usec()
	textures[path]=make_native_texture(path,image)
	var upload_usec := Time.get_ticks_usec() - upload_started
	texture_uploads += 1
	texture_upload_usec += upload_usec
	last_texture_upload = {"frame": Engine.get_process_frames(), "path": path, "bytes": bytes, "size": image.get_size(), "usec": upload_usec,
		"start_usec": upload_started, "end_usec": upload_started + upload_usec}
	record_frame_upload(last_texture_upload)
	textures[path].set_meta("drone_invisible",invisible)
	if invisible and invisible_images.size()<INVISIBLE_IMAGE_LIMIT:invisible_images[path]=textures[path]
	weak_images[path]={"ref":weakref(textures[path]),"bytes":bytes}
	texture_bytes[path]=bytes;cached_bytes+=bytes
	last_used[path]=Engine.get_process_frames()
	texture_order.erase(path);texture_order.append(path)
static func begin(canvas:CanvasItem) -> void:
	if not RenderingServer.frame_post_draw.is_connected(trim_stale):
		RenderingServer.frame_post_draw.connect(trim_stale)
	active_canvas=canvas
	if int(canvas.get_meta("drone_texture_frame",-1))!=Engine.get_process_frames():
		canvas.set_meta("drone_texture_frame",Engine.get_process_frames())
		canvas.set_meta("drone_texture_pins",{})
static func catalog(kind:String) -> Dictionary:
	if not catalogs.has(kind):catalogs[kind]=JSON.parse_string(FileAccess.get_file_as_string(MANIFESTS[kind]))
	return catalogs[kind]
static func texture(path:String) -> Texture2D:
	if not textures.has(path) and not restore_live(path):
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
			image=load_native_or_original(path)
			if image==null:push_error("Drone animation missing: "+path);return null
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
			var left:float=Vector2(d.get("position",goal)).distance_to(goal)/Routes.SPEED
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
	# Keep preparation, residency and clocks unchanged so the next visible frame
	# is ready. Only omit the draw command for byte-verified transparent cells.
	if record.has("emptyFrameRanges"):
		for span in record.emptyFrameRanges:
			if index >= int(span[0]) and index <= int(span[1]): return
	var columns:=int(record.columns)
	if atlas_texture is NativeEffect:
		if native_context_supported(canvas,tint):
			native_mask_draws+=1;tint*=Color(135.0/255.0,139.0/255.0,125.0/255.0,1);atlas_texture=atlas_texture.mask
		else:native_fallback_draws+=1;atlas_texture=atlas_texture.original_texture()
		if atlas_texture==null:return
	elif atlas_texture is CargoStorage:
		# Same quad as the full frame; samples outside the small frame clamp to its transparent border.
		var cargo_frame:Texture2D=atlas_texture.frame(index) if columns==atlas_texture.columns and Vector2i(size)==atlas_texture.cell and cargo_context_supported(canvas) else null
		if cargo_frame!=null:
			cargo_frame_draws+=1
			canvas.draw_texture_rect_region(cargo_frame,rect,Rect2(-Vector2(atlas_texture.box.position),size),tint)
			return
		cargo_fallback_draws+=1;atlas_texture=atlas_texture.original_texture()
		if atlas_texture==null:return
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
	canvas.draw_circle(lamp_at,maxf(.6*world_scale,2.4*scale_value),color,true,-1.0,true)

static func restore_live(path:String)->bool:
	if not weak_images.has(path):return false
	var image:Texture2D=weak_images[path].ref.get_ref()
	if image==null:
		weak_images.erase(path);return false
	textures[path]=image
	texture_bytes[path]=int(weak_images[path].bytes)
	cached_bytes+=int(texture_bytes[path])
	last_used[path]=Engine.get_process_frames()
	texture_order.erase(path);texture_order.append(path)
	return true
static func trim_stale()->void:
	# Upload-only eviction leaves stale sheets resident when activity stops.
	# Drop lookup ownership after rendering; canvas pins keep live commands valid.
	trim_calls+=1
	for path in weak_images.keys():
		if weak_images[path].ref.get_ref()==null:weak_images.erase(path)
	if cached_bytes<=CACHE_BUDGET:return
	for path in texture_order.duplicate():
		if cached_bytes<=CACHE_BUDGET:break
		if int(last_used.get(path,0))>=Engine.get_process_frames()-2:continue
		cached_bytes-=int(texture_bytes[path])
		textures.erase(path);texture_bytes.erase(path);last_used.erase(path)
		texture_order.erase(path);trim_removed+=1


const NativeEffect=preload("res://scripts/drone_effect_storage.gd")
const NativeEffectData=preload("res://scripts/drone_effect_storage_catalog.gd")
const NativeFlood=preload("res://scripts/flood_submersion.gdshader")
static var native_mask_draws:=0
static var native_fallback_draws:=0
# Lossless LA8 storage for single-colour effect sheets. Native pixel evidence exists for
# Windows only; every other platform keeps the original RGBA sheets until checked there.
static var native_effect_storage:=OS.get_name()=="Windows" and not OS.get_cmdline_user_args().has("--reference-effect-storage")
# Generated catalog; a variable so fixtures can supply scratch entries.
static var effect_storage:Dictionary=NativeEffectData.DATA
static func load_native_or_original(path:String)->Image:
	var image:=Image.new()
	var original_bytes:=FileAccess.get_file_as_bytes(path) if FileAccess.file_exists(path) else PackedByteArray()
	if original_bytes.is_empty():return null
	if native_effect_storage and effect_storage.has(path):
		var spec:Dictionary=effect_storage[path]
		var original_hash:=HashingContext.new();original_hash.start(HashingContext.HASH_SHA256);original_hash.update(original_bytes)
		# A changed selected PNG must invalidate its derived storage, even at the same path/dimensions.
		if original_hash.finish().hex_encode()==spec.original_sha256:
			var bytes:=FileAccess.get_file_as_bytes(spec.path) if FileAccess.file_exists(spec.path) else PackedByteArray()
			if not bytes.is_empty():
				var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(bytes)
				if hash.finish().hex_encode()==spec.sha256 and image.load_png_from_buffer(bytes)==OK and image.get_format()==Image.FORMAT_LA8 and image.get_size()==Vector2i(spec.width,spec.height) and not image.has_mipmaps():
					image.set_meta("native_effect_original_png",original_bytes);image.set_meta("native_effect_source",path)
					return image
	if cargo_storage_enabled and cargo_storage.has(path):
		var cargo:Image=load_cargo_storage(path,cargo_storage[path],original_bytes)
		if cargo!=null:return cargo
	image=Image.new()
	return image if image.load_png_from_buffer(original_bytes)==OK else null
static func native_context_supported(canvas:CanvasItem,color:Color)->bool:
	if color.r!=1.0 or color.g!=1.0 or color.b!=1.0:return false
	if canvas.self_modulate.r!=1.0 or canvas.self_modulate.g!=1.0 or canvas.self_modulate.b!=1.0:return false
	var node:Node=canvas
	var effective_filter:=0
	while node is CanvasItem:
		if node.modulate.r!=1.0 or node.modulate.g!=1.0 or node.modulate.b!=1.0:return false
		if effective_filter==0:effective_filter=node.texture_filter
		node=node.get_parent()
	if effective_filter!=CanvasItem.TEXTURE_FILTER_NEAREST:return false
	var material_node:CanvasItem=canvas
	while material_node.use_parent_material and material_node.get_parent() is CanvasItem:material_node=material_node.get_parent()
	var material:Material=material_node.material
	return material==null or (material is ShaderMaterial and material.shader==NativeFlood)
static func make_native_texture(path:String,image:Image)->Texture2D:
	if cargo_storage.has(path) and image.get_meta("drone_cargo_source","")==path and image.has_meta("drone_cargo_original_png"):return make_cargo_texture(path,image)
	if not effect_storage.has(path) or image.get_format()!=Image.FORMAT_LA8 or image.get_meta("native_effect_source","")!=path or not image.has_meta("native_effect_original_png"):return ImageTexture.create_from_image(image)
	var display=NativeEffect.new();display.source=path;display.original_png=image.get_meta("native_effect_original_png");display.width=image.get_width();display.height=image.get_height();display.base_bytes=image.get_data_size();display.mask=ImageTexture.create_from_image(image)
	var ref:WeakRef=weakref(display)
	display.storage_changed=func(bytes:int):
		if not weak_images.has(path) or weak_images[path].ref.get_ref()!=ref.get_ref():return
		weak_images[path].bytes=bytes
		if textures.has(path) and textures[path]==ref.get_ref():cached_bytes+=bytes-int(texture_bytes[path]);texture_bytes[path]=bytes
	display.upload_record=func(bytes:int,usec:int,started:int,size:Vector2i):
		texture_uploads+=1;texture_upload_usec+=usec
		last_texture_upload={"frame":Engine.get_process_frames(),"path":path,"bytes":bytes,"size":size,"usec":usec,"start_usec":started,"end_usec":started+usec,"native_original_fallback":true}
		record_frame_upload(last_texture_upload)
	return display


const CargoStorage=preload("res://scripts/drone_cargo_storage.gd")
const CargoStorageData=preload("res://scripts/drone_cargo_storage_catalog.gd")
static var cargo_frame_draws:=0
static var cargo_fallback_draws:=0
# Cropped cargo frames replace whole-sheet uploads. Scaled drawing can pick a neighbouring
# source row or column (owner-accepted October 11, 2026). Windows only until checked elsewhere.
static var cargo_storage_enabled:=OS.get_name()=="Windows" and not OS.get_cmdline_user_args().has("--reference-cargo-storage")
# Generated catalog; a variable so fixtures can supply scratch entries.
static var cargo_storage:Dictionary=CargoStorageData.DATA
static func load_cargo_storage(path:String,spec:Dictionary,original_bytes:PackedByteArray)->Image:
	var original_hash:=HashingContext.new();original_hash.start(HashingContext.HASH_SHA256);original_hash.update(original_bytes)
	# A changed selected PNG must invalidate its derived storage, even at the same path/dimensions.
	if original_hash.finish().hex_encode()!=spec.original_sha256:return null
	var bytes:=FileAccess.get_file_as_bytes(spec.path) if FileAccess.file_exists(spec.path) else PackedByteArray()
	if bytes.is_empty():return null
	var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(bytes)
	if hash.finish().hex_encode()!=spec.sha256:return null
	var image:=Image.new()
	if image.load_png_from_buffer(bytes)!=OK or image.has_mipmaps():return null
	var rows:int=int(spec.height)/int(spec.cell[1])
	if image.get_size()!=Vector2i(int(spec.box[2])*int(spec.columns),int(spec.box[3])*rows):return null
	image.set_meta("drone_cargo_original_png",original_bytes);image.set_meta("drone_cargo_source",path)
	return image
static func cargo_context_supported(canvas:CanvasItem)->bool:
	var node:Node=canvas
	var effective_filter:=0
	var effective_repeat:=0
	while node is CanvasItem:
		if effective_filter==0:effective_filter=node.texture_filter
		if effective_repeat==0:effective_repeat=node.texture_repeat
		node=node.get_parent()
	if effective_filter!=CanvasItem.TEXTURE_FILTER_NEAREST:return false
	# Samples beyond the small frame must clamp to its border, never wrap.
	if effective_repeat>CanvasItem.TEXTURE_REPEAT_DISABLED:return false
	var material_node:CanvasItem=canvas
	while material_node.use_parent_material and material_node.get_parent() is CanvasItem:material_node=material_node.get_parent()
	var material:Material=material_node.material
	return material==null or (material is ShaderMaterial and material.shader==NativeFlood)
static func make_cargo_texture(path:String,image:Image)->Texture2D:
	var spec:Dictionary=cargo_storage[path]
	var display=CargoStorage.new();display.source=path;display.original_png=image.get_meta("drone_cargo_original_png");display.width=int(spec.width);display.height=int(spec.height)
	display.cropped=image;display.box=Rect2i(int(spec.box[0]),int(spec.box[1]),int(spec.box[2]),int(spec.box[3]));display.cell=Vector2i(int(spec.cell[0]),int(spec.cell[1]));display.columns=int(spec.columns);display.base_bytes=image.get_data_size()
	var ref:WeakRef=weakref(display)
	display.storage_changed=func(bytes:int):
		if not weak_images.has(path) or weak_images[path].ref.get_ref()!=ref.get_ref():return
		weak_images[path].bytes=bytes
		if textures.has(path) and textures[path]==ref.get_ref():cached_bytes+=bytes-int(texture_bytes[path]);texture_bytes[path]=bytes
	display.upload_record=func(bytes:int,usec:int,started:int,size:Vector2i,kind:String):
		texture_uploads+=1;texture_upload_usec+=usec
		last_texture_upload={"frame":Engine.get_process_frames(),"path":path,"bytes":bytes,"size":size,"usec":usec,"start_usec":started,"end_usec":started+usec,"cargo_storage":kind}
		record_frame_upload(last_texture_upload)
	return display
