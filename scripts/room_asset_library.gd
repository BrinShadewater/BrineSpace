extends RefCounted
## Registered artwork only; no unprocessed source images enter the room renderer.
static var catalog: Dictionary={}
static var source_textures: Dictionary={}
const STATION_PROPS := "res://rooms/station-props-v2/props.json"
# [world offset, opacity] layers of the station-prop contact shadow, darkest nearest.
const FLOOR_PIECE_DEPTH := 100000.0
const CONTACT_SHADOW := [[Vector2(1.5,2.0),0.22],[Vector2(2.5,3.5),0.14],[Vector2(3.5,5.0),0.08]]
# Rooms that keep their pre-v2 art for now (owner, 2026-09-24). Every other room shows
# only station props, plus the live drone and dock in drone bays.
const LEGACY_ART_ROOMS := ["brine_core","corridor","corner","tee_corridor"]
# Built-in machinery the game drives (airlock cycle, cryo wake-ups): kept live like the
# drone docks until replacement art is wired to the same behaviour.
const LIVE_MACHINERY := ["pressure_chamber","cryo_pod_0","cryo_pod_1"]
static func is_station_prop(id: String) -> bool:
	return base_id(id).begins_with("library/sp-")
static func role_of(prop: Dictionary) -> String:
	var id:=base_id(str(prop.get("variant_source",prop.get("copy_source",prop.get("id","")))))
	return str(entries().get(id,{}).get("role",""))
# Built-in view props and pre-v2 library props leave redesigned rooms. The drone and
# its dock are live machinery (animation, charging, routes), not dressing.
static func keeps_in_room(room_id: String, prop: Dictionary) -> bool:
	if room_id.is_empty() or room_id in LEGACY_ART_ROOMS: return true
	var id:=str(prop.get("id",""))
	if id.ends_with("_rov") or id.ends_with("_hatch") or id in LIVE_MACHINERY: return true
	return is_station_prop(str(prop.get("copy_source",prop.get("variant_source",id))))
# Several views re-add built-in props after the layout pass (legacy restorations), so
# callers strip again once a view is configured and before it draws.
static func strip_retired(view) -> void:
	if view==null or not "props" in view: return
	var store=load("res://scripts/room_layout_store.gd")
	var room_id: String=store.room_id_for(view,store.asset_for(view))
	if room_id.is_empty() or room_id in LEGACY_ART_ROOMS: return
	view.props=view.props.filter(func(prop): return keeps_in_room(room_id,prop))
static func entries() -> Dictionary:
	if not catalog.is_empty(): return catalog
	# Station props v2 (2026-09-24): cut from the owner's room designs. These are the
	# only props the Studio offers; the older sources below stay loadable for the rooms
	# and site scenery that still use them (BRINE Core, corridors, seabed dressing).
	var station: Variant=JSON.parse_string(FileAccess.get_file_as_string(STATION_PROPS))
	if station is Array:
		for entry in station:
			catalog["library/"+str(entry.id)]={
				"data":entry,"label":str(entry.label),"width":float(entry.display_width),
				"group":"station","category":str(entry.category),
				"default_rooms":entry.get("default_rooms",[]),"role":str(entry.get("role",""))}
	for file in DirAccess.get_files_at("res://rooms/full-wall-v1/registrations"):
		if not file.ends_with(".json"): continue
		var data=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/registrations/"+file))
		if not data is Dictionary or not data.has("pieces"): continue
		var id: String="library/"+file.trim_suffix(".json")
		catalog[id]={"data":data,"label":data.get("label",file.trim_suffix(".json").replace("-"," ").capitalize()),"default_rooms":data.get("default_rooms",[])}
		if data.has("display_width"): catalog[id].width=float(data.display_width)
	for entry in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/common-assets.json")):
		catalog["library/common-"+entry.id]={"data":entry.data,"label":entry.label,"width":entry.width,"group":"common","category":entry.get("category","wall"),"theme":str(entry.get("theme",""))}
	# Tileset props arrive as one bulk file rather than 8000 registrations: the
	# loop above reads a file per entry, which is fine for 220 and not for 8229.
	# The id prefix is deliberate - RoomLayoutStore.is_common_decoration() drops
	# anything under library/common-, so these would never reach a live room.
	var bulk: String="res://rooms/tileset-library/props.json"
	if FileAccess.file_exists(bulk):
		var parsed: Variant=JSON.parse_string(FileAccess.get_file_as_string(bulk))
		if parsed is Array:
			for entry in parsed:
				catalog["library/tileset-"+str(entry.id)]={
					"data":entry,"label":entry.get("label",entry.id),
					"width":float(entry.get("display_width",48.0)),
					"group":"tileset","category":entry.get("category","prop"),
					"tileset":entry.get("tileset",""),
					"title":str(entry.get("title",""))}
	return catalog
# Props the library merged away keep working: a layout that placed the old id draws
# the prop that absorbed it. Without this a merge silently emptied placed props out
# of the owner's rooms (three went missing from the Research Lab).
static var aliases: Dictionary={}
static var aliases_loaded:=false
static func base_id(id: String) -> String:
	var base:=id.split("#")[0]
	if not base.begins_with("library/tileset-"): return base
	if not aliases_loaded:
		aliases_loaded=true
		var path:="res://rooms/tileset-library/merged.json"
		if FileAccess.file_exists(path):
			var parsed: Variant=JSON.parse_string(FileAccess.get_file_as_string(path))
			if parsed is Dictionary: aliases=parsed
	var short:=base.trim_prefix("library/tileset-")
	return "library/tileset-"+str(aliases[short]) if aliases.has(short) else base

# One authored side wall serves both side walls: the opposite wall reuses the same
# raster with its geometry mirrored about the region's own centre line. The pivot
# sits on that line, so width, height and outline are unchanged and only an
# asymmetric interior moves - which is the point, and the part that would break
# placement and clearance if the art flipped and the polygons did not.
# Side walls only. A vertical mirror would put a worktop under its cabinets.
static func mirror_registration(registration: Dictionary) -> Dictionary:
	var mirrored: Dictionary=registration.duplicate(true)
	var axis: float=registration.pivot.x*2.0
	var pieces: Array=[]
	for polygon in registration.pieces:
		var points:=PackedVector2Array()
		# Reversed so mirrored polygons keep the winding of the authored ones.
		for i in range(polygon.size()-1,-1,-1): points.append(Vector2(axis-polygon[i].x,polygon[i].y))
		pieces.append(points)
	mirrored.pieces=pieces
	mirrored.mirrored=true
	mirrored.mirror_axis=axis
	return mirrored

# Mirrored geometry samples the unmirrored source pixel, so the raster flips with
# the polygons. Every registration draw path routes its UVs through this.
static func source_uv(registration: Dictionary, point: Vector2) -> Vector2:
	if not registration.get("mirrored",false): return point
	return Vector2(float(registration.mirror_axis)-point.x,point.y)

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
		for metadata in ["copy_source","wall_mount","split_wall","custom_library_draw"]:
			if original.has(metadata): replacement[metadata]=original[metadata]
		replacement.sort_y=base_sort_y(replacement)
		room.props[i]=replacement
# Props draw in order of this depth. An L-shaped corner console sorts by the front of its
# wall arm, not the tip of the arm running down the side wall, which drew crew standing in
# front of the corner behind it (owner playtest).
static func base_sort_y(prop: Dictionary) -> float:
	# Hatches, pads and rugs lie on the deck: under every crew member and prop.
	if prop.get("floor_piece",false): return prop.rect.end.y-FLOOR_PIECE_DEPTH
	if prop.has("corner") and not prop.get("collision_boxes",[]).is_empty():
		var arm: Array=prop.collision_boxes[0]
		return prop.rect.position.y+prop.rect.size.y*(float(arm[1])+float(arm[3]))
	return prop.rect.end.y
static func template(id: String) -> Dictionary:
	id=base_id(id)
	var all:=entries()
	if not all.has(id): return {}
	if all[id].has("template"): return all[id].template
	var data: Dictionary=all[id].data
	if image_jobs.has(data.source):
		finish_texture(data.source,true)
	if not source_textures.has(data.source):
		# Sheets retired to the owner's Desktop (station props v2, step 8a) leave
		# stale placements in old saves and layouts: skip them without an error.
		if not FileAccess.file_exists(data.source): return {}
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
	if data.has("operating_screens"): registration.operating_screens=data.operating_screens.duplicate(true)
	if data.has("operating_screen_color"): registration.operating_screen_color=data.operating_screen_color
	if data.has("reading_lamp"): registration.reading_lamp=data.reading_lamp.duplicate(true)
	if data.has("turbine_effects"): registration.turbine_effects=data.turbine_effects.duplicate(true)
	if data.has("cooktop_ring"): registration.cooktop_ring=data.cooktop_ring.duplicate(true)
	if data.has("status_point"): registration.status_point=data.status_point.duplicate(true)
	if data.get("mirror_horizontal",false): registration=mirror_registration(registration)
	var prop: Dictionary={"id":id,"library_asset":true,"full_wall":true,"rect":Rect2(Vector2.ZERO,size),"center":Vector2.ZERO,"sort_y":size.y,"registration":registration,"library_texture":texture}
	if data.has("collision_boxes"): prop.collision_boxes=data.collision_boxes.duplicate(true)
	if data.has("footprint"):
		# Floor footprint as fractions of the rect; the equipment shadow shades this
		# instead of the full art box. Mirrored art mirrors its footprint.
		var f: Array=data.footprint.duplicate()
		if registration.get("mirrored",false): f[0]=1.0-float(f[0])-float(f[2])
		prop.footprint=f
	if data.has("corner"): prop.wall_mount=true; prop.corner=data.corner
	if data.get("floor_piece",false): prop.floor_piece=true; prop.collision_boxes=[]
	prop.sort_y=base_sort_y(prop)
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
		prop.rect.position=at; prop.sort_y=base_sort_y(prop)
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
	# Station props are cut without their painted shadows (owner, 2026-09-24): lay a
	# soft contact shadow from the prop's own silhouette, stacked offsets fading out.
	if is_station_prop(str(prop.get("copy_source",prop.get("variant_source",prop.id)))) and not prop.get("floor_piece",false):
		for step in CONTACT_SHADOW:
			for polygon in reg.pieces:
				var shadow_points:=PackedVector2Array()
				var shadow_uv:=PackedVector2Array()
				for point in polygon:
					shadow_points.append(anchor+(point-reg.pivot)*scale_value+step[0])
					shadow_uv.append(source_uv(reg,point)/Vector2(tex.get_size()))
				room.painter.draw_polygon(shadow_points,PackedColorArray([Color(0,0,0,step[1])]),shadow_uv,tex)
	for polygon in reg.pieces:
		var points:=PackedVector2Array()
		var uv:=PackedVector2Array()
		for point in polygon:
			points.append(anchor+(point-reg.pivot)*scale_value)
			uv.append(source_uv(reg,point)/Vector2(tex.get_size()))
		room.painter.draw_polygon(points,PackedColorArray([Color.WHITE]),uv,tex)
	draw_operating_screens(room,reg,anchor,scale_value)

static func draw_operating_screens(room, reg: Dictionary, anchor: Vector2, scale_value: float) -> void:
	if reg.has("operating_screens") and room.operating:
		for index in range(reg.operating_screens.size()):
			var screen: Array=reg.operating_screens[index]
			var trace:=PackedVector2Array()
			for step in range(9):
				var point:=Vector2(screen[0]+screen[2]*step/8.0,screen[1]+screen[3]*(0.5+0.22*sin(step*1.7+room.machine_clock*3+index)))
				point=source_uv(reg,point)
				trace.append(anchor+(point-reg.pivot)*scale_value)
			var color:=Color(str(reg.operating_screen_color)) if reg.has("operating_screen_color") else Color(.13,.75,.78,.8)
			room.painter.draw_polyline(trace,color,maxf(.55,scale_value*1.4))

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

# One cached complementary atlas pair preserves the original UV geometry exactly.
# These are presentation copies; source textures, collision and owner data stay intact.
static var bunk_layer_cache: Dictionary={}
static func bunk_layers(prop: Dictionary) -> Array:
	if base_id(str(prop.get("variant_source",prop.get("copy_source",prop.id))))!="library/tileset-mb2-14":return []
	var texture: Texture2D=prop.library_texture
	var key:=texture.get_instance_id()
	if not bunk_layer_cache.has(key):
		var back:=texture.get_image()
		var front:=Image.create(back.get_width(),back.get_height(),false,Image.FORMAT_RGBA8)
		for region in [Rect2i(177,883,49,141),Rect2i(10,783,14,241),Rect2i(24,997,153,18)]:
			if not Rect2i(Vector2i.ZERO,back.get_size()).encloses(region):return []
			front.blit_rect(back,region,region.position)
			back.fill_rect(region,Color.TRANSPARENT)
		bunk_layer_cache[key]=[ImageTexture.create_from_image(back),ImageTexture.create_from_image(front)]
	var layers: Array=[]
	for i in range(2):
		var layer:=prop.duplicate()
		layer.library_texture=bunk_layer_cache[key][i]
		layers.append({"kind":"prop","sort_y":float(prop.sort_y)+i*0.02,"prop":layer})
	return layers

static var exterior_assets: Dictionary={}
static var exterior_loaded := false
static func is_exterior(id: String) -> bool:
	if not exterior_loaded:
		exterior_loaded=true
		var parsed=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/tileset-library/exterior.json"))
		if parsed is Dictionary: exterior_assets=parsed.get("assets",{})
	return exterior_assets.has(base_id(id).trim_prefix("library/tileset-"))
