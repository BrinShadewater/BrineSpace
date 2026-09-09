extends RefCounted
## Registered artwork only; no unprocessed source images enter the room renderer.
static var catalog: Dictionary={}
static var source_textures: Dictionary={}
static func entries() -> Dictionary:
	if not catalog.is_empty(): return catalog
	for file in DirAccess.get_files_at("res://rooms/full-wall-v1/registrations"):
		if not file.ends_with(".json"): continue
		var data=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/registrations/"+file))
		if not data is Dictionary or not data.has("pieces"): continue
		var id: String="library/"+file.trim_suffix(".json")
		catalog[id]={"data":data,"label":data.get("label",file.trim_suffix(".json").replace("-"," ").capitalize()),"default_rooms":data.get("default_rooms",[])}
		if data.has("display_width"): catalog[id].width=float(data.display_width)
	for entry in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/common-assets.json")):
		catalog["library/common-"+entry.id]={"data":entry.data,"label":entry.label,"width":entry.width,"group":"common","category":entry.get("category","wall")}
	return catalog
static func base_id(id: String) -> String: return id.split("#")[0]

static func family_variants(asset: String) -> Array:
	var name:=base_id(asset).trim_prefix("library/").trim_prefix("full_wall_").trim_prefix("side-")
	for direction in ["north","east","south","west"]:
		name=name.trim_suffix("-"+direction)
	var result: Array=[]
	for direction in ["north","east","south","west"]:
		var candidate: String="library/"+(name if direction=="north" else "side-"+name+"-"+direction)
		if entries().has(candidate): result.append(candidate)
		for id in entries():
			if str(id).begins_with("library/"+name+"-"+direction+"-"): result.append(id)
	return result

static func apply_variants(room, values: Dictionary) -> void:
	for i in range(room.props.size()):
		var original: Dictionary=room.props[i]
		var id:=str(original.id)
		var chosen:=str(values.get("variant/"+id,""))
		if chosen.is_empty(): continue
		var replacement:=template(chosen).duplicate(true)
		if replacement.is_empty(): continue
		var length: float=float(values.get("variant_extent/"+id,maxf(original.rect.size.x,original.rect.size.y)))
		var factor: float=length/maxf(replacement.rect.size.x,replacement.rect.size.y)
		replacement.rect=Rect2(original.rect.position,replacement.rect.size*factor)
		replacement.id=id
		replacement.variant_source=chosen
		for metadata in ["copy_source","wall_mount","split_wall"]:
			if original.has(metadata): replacement[metadata]=original[metadata]
		replacement.sort_y=replacement.rect.end.y
		room.props[i]=replacement
static func template(id: String) -> Dictionary:
	id=base_id(id)
	var all:=entries()
	if not all.has(id): return {}
	if all[id].has("template"): return all[id].template
	var data: Dictionary=all[id].data
	if image_jobs.has(data.source):
		finish_texture(data.source,true)
	if not source_textures.has(data.source):
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes(data.source))!=OK: return {}
		source_textures[data.source]=ImageTexture.create_from_image(image)
	var texture: Texture2D=source_textures[data.source]
	var r: Array=data.region
	var pieces: Array=[]
	for polygon in data.pieces:
		var points:=PackedVector2Array()
		for point in polygon: points.append(Vector2(point[0],point[1]))
		pieces.append(points)
	var width: float=all[id].get("width",minf(120.0,120.0*float(r[2])/float(r[3])))
	var size:=Vector2(width,width*float(r[3])/float(r[2]))
	var registration: Dictionary={"pieces":pieces,"pivot":Vector2(r[0]+r[2]*0.5,r[1]+r[3]),"width":float(r[2]),"height":float(r[3])}
	var prop: Dictionary={"id":id,"library_asset":true,"full_wall":true,"rect":Rect2(Vector2.ZERO,size),"center":Vector2.ZERO,"sort_y":size.y,"registration":registration,"library_texture":texture}
	if data.has("collision_boxes"): prop.collision_boxes=data.collision_boxes.duplicate(true)
	if data.has("corner"): prop.wall_mount=true; prop.corner=data.corner
	all[id].template=prop
	# The tray publishes only clipped transparent renders, never source-sheet crops.
	return prop
static func apply(room: Node, values: Dictionary) -> void:
	for i in range(room.props.size()-1,-1,-1):
		if room.props[i].get("library_asset",false) and str(room.props[i].id).begins_with("library/"): room.props.remove_at(i)
	for id in values:
		if not str(id).begins_with("library/"): continue
		var value=values[id]
		if not value is Array or value.size()!=2: continue
		var at:=Vector2(value[0],value[1])
		if not at.is_finite(): continue
		var prop: Dictionary=(portable_template(values["portable/"+str(id)]) if values.has("portable/"+str(id)) else template(id)).duplicate(true)
		if prop.is_empty(): continue
		prop.id=id
		if prop.has("art_offset"): prop.art_offset+=at-prop.rect.position
		prop.rect.position=at; prop.sort_y=prop.rect.end.y
		room.props.append(prop)

static func draw(room, prop: Dictionary) -> void:
	if prop.has("portable_view"):
		var source=prop.portable_view
		var previous=source.painter
		source.painter=room.painter; source.operating=room.operating; source.machine_clock=room.machine_clock
		var native:=prop.duplicate()
		native.id=prop.portable_id; native.erase("library_asset")
		source.draw_registered_prop(native)
		source.painter=previous
		return
	var reg: Dictionary=prop.registration
	var tex: Texture2D=prop.library_texture
	var scale_value: float=prop.rect.size.x/reg.width
	var anchor:=Vector2(prop.rect.get_center().x,prop.rect.end.y)
	for polygon in reg.pieces:
		var points:=PackedVector2Array()
		var uv:=PackedVector2Array()
		for point in polygon:
			points.append(anchor+(point-reg.pivot)*scale_value)
			uv.append(point/Vector2(tex.get_size()))
		room.painter.draw_polygon(points,PackedColorArray([Color.WHITE]),uv,tex)

static var portable_views: Dictionary={}
static func portable_template(descriptor: Dictionary) -> Dictionary:
	var key:=str(descriptor.get("view",""))+"/"+str(descriptor.get("room",""))+"/"+str(descriptor.get("quarter",0))
	if not portable_views.has(key):
		# Only room scripts in the local editor catalog may supply portable artwork.
		var allowed:=false
		for entry in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json")):
			if entry.view==descriptor.get("view","") and entry.room==descriptor.get("room",""): allowed=true
		if not allowed: return {}
		var view=load(descriptor.view).new()
		if "room_id" in view: view.room_id=descriptor.room
		view.set_meta("layout_editor_preview",true); view.set_meta("layout_draft",{})
		view.embedded=true
		Engine.get_main_loop().root.add_child(view); view.hide()
		view.configure_embedded(int(descriptor.quarter),[],false,0.0)
		portable_views[key]=view
	var view=portable_views[key]
	for original in view.props:
		if str(original.id)!=str(descriptor.source) or original.has("flush_region"): continue
		var prop: Dictionary=original.duplicate(true)
		prop.library_asset=true; prop.portable_view=view; prop.portable_id=original.id
		if not prop.has("registration"): prop.registration={}
		return prop
	return {}

static func bounds(prop: Dictionary) -> Rect2:
	if prop.has("portable_view"):
		var native:=prop.duplicate()
		native.erase("library_asset"); native.id=prop.portable_id
		return prop.portable_view.prop_visual_bounds(native)
	return prop.rect

# Decode preview PNGs away from the UI thread; GPU textures are created on the main thread.
static var image_jobs: Dictionary={}
static func request_texture(source: String) -> void:
	if source_textures.has(source) or image_jobs.has(source): return
	var result: Dictionary={}
	var task:=WorkerThreadPool.add_task(func():
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes(source))==OK: result.image=image)
	image_jobs[source]={"task":task,"result":result}

static func finish_texture(source: String, wait:=false) -> bool:
	if source_textures.has(source) and not image_jobs.has(source): return true
	if not image_jobs.has(source): return false
	var job: Dictionary=image_jobs[source]
	if not wait and not WorkerThreadPool.is_task_completed(job.task): return false
	WorkerThreadPool.wait_for_task_completion(job.task)
	if job.result.has("image"): source_textures[source]=ImageTexture.create_from_image(job.result.image)
	image_jobs.erase(source)
	return true
