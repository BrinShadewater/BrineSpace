extends RefCounted
## Local authoring overrides; independent of expedition saves.
static var path := "user://room_layouts.json"
static var defaults_path := "res://rooms/full-wall-v1/default-layouts.json"
static var loaded := false
static var data: Dictionary={}
static var revision:=0
static var geometry_revision:=0
static func ensure_loaded() -> void:
	if loaded: return
	loaded=true
	revision+=1
	if FileAccess.file_exists(path):
		var parsed=JSON.parse_string(FileAccess.get_file_as_string(path))
		if parsed is Dictionary and parsed.get("version",0)==1 and parsed.get("layouts") is Dictionary:
			if navigation_stamp(data)!=navigation_stamp(parsed.layouts): geometry_revision+=1
			data=parsed.layouts
static func key(asset: String, q: int) -> String: return asset+"/"+str(posmod(q,4))
static var authored_cache: Dictionary={}
static var authored_cache_path:=""
static func invalidate_authored() -> void:
	authored_cache_path=""
static func authored_positions(asset: String, q: int) -> Dictionary:
	if authored_cache_path!=defaults_path:
		var previous:=authored_cache
		authored_cache_path=defaults_path; authored_cache={}
		if FileAccess.file_exists(defaults_path):
			var parsed=JSON.parse_string(FileAccess.get_file_as_string(defaults_path))
			if parsed is Dictionary and parsed.get("version",0)==1 and parsed.get("layouts") is Dictionary: authored_cache=parsed.layouts
		if previous!=authored_cache: revision+=1
		if navigation_stamp(previous)!=navigation_stamp(authored_cache): geometry_revision+=1
	return authored_cache.get(key(asset,q),{}).duplicate(true)
static func positions(asset: String, q: int) -> Dictionary:
	ensure_loaded()
	var result:=authored_positions(asset,q)
	result.merge(data.get(key(asset,q),{}).duplicate(true),true)
	return result
static func save_layout(asset: String, q: int, positions_to_save: Dictionary) -> Error:
	ensure_loaded()
	var next:=data.duplicate(true)
	if positions_to_save.is_empty(): next.erase(key(asset,q))
	else: next[key(asset,q)]=positions_to_save.duplicate(true)
	return write_data(next)
static func write_data(next: Dictionary) -> Error:
	var file:=FileAccess.open(path+".tmp",FileAccess.WRITE)
	if file==null: return FileAccess.get_open_error()
	file.store_string(JSON.stringify({"version":1,"layouts":next},"\t"))
	file.close()
	var error:=DirAccess.rename_absolute(ProjectSettings.globalize_path(path+".tmp"),ProjectSettings.globalize_path(path))
	if error==OK:
		if next!=data: revision+=1
		if navigation_stamp(next)!=navigation_stamp(data): geometry_revision+=1
		data=next
	return error
static func move_prop(prop: Dictionary, at: Vector2) -> void:
	var shift: Vector2=at-prop.rect.position
	prop.rect.position=at
	prop.sort_y=prop.rect.end.y
	if prop.has("art_offset"): prop.art_offset+=shift
static func apply(room, asset: String) -> bool:
	room.set_meta("layout_asset",asset)
	if room.has_meta("layout_editor_preview"): return false
	var selected:=positions(asset,room.quarter)
	var signature:=hash([asset,room.quarter,selected,room.props])
	if room.get_meta("layout_apply_signature",-1)==signature: return false
	# Only restore props this authoring layer previously removed; dynamic room props stay authoritative.
	var removed_by_quarter: Dictionary=room.get_meta("layout_removed_ids",{})
	var originals: Dictionary=room.get_meta("layout_copy_sources",{}).get(room.quarter,{})
	for id in removed_by_quarter.get(room.quarter,[]):
		if selected.has(id) and selected[id]==null: continue
		if not originals.has(id): continue
		var present:=false
		for prop in room.props:
			if str(prop.id)==id: present=true; break
		if not present: room.props.append(originals[id].duplicate(true))
	var removed: Array=[]
	for prop in room.props:
		if selected.has(str(prop.id)) and selected[str(prop.id)]==null: removed.append(str(prop.id))
	for id in removed_by_quarter.get(room.quarter,[]):
		if selected.has(id) and selected[id]==null and id not in removed: removed.append(id)
	removed_by_quarter[room.quarter]=removed; room.set_meta("layout_removed_ids",removed_by_quarter)
	preload("res://scripts/room_asset_library.gd").apply(room,selected)
	copies(room,selected)
	preload("res://scripts/room_asset_library.gd").apply_variants(room,selected)
	room.props=room.props.filter(func(prop): return not (selected.has(str(prop.id)) and selected[str(prop.id)]==null))
	# Common decorations stay in Studio; live rooms contain their specialist equipment only.
	room.props=room.props.filter(func(prop): return not is_common_decoration(prop))
	for prop in room.props:
		var axes=selected.get("flip/"+str(prop.id),[false,false])
		if not axes is Array or axes.size()!=2: axes=[false,false]
		prop.layout_flip=Vector2(-1 if axes[0] else 1,-1 if axes[1] else 1)
		prop.layout_hidden=selected.get("hidden/"+str(prop.id),false)
		if prop.has("flush_region"): continue
		if not prop.has("layout_default"): prop.layout_default=prop.rect.position
		var at: Vector2=prop.layout_default
		var value=selected.get(str(prop.id))
		if value is Array and value.size()==2 and (value[0] is float or value[0] is int) and (value[1] is float or value[1] is int):
			at=Vector2(value[0],value[1])
			if not at.is_finite(): continue
		resize_prop(prop,selected.get("size/"+str(prop.id),[1.0,1.0]))
		move_prop(prop,at)
		prop.sort_y+=float(selected.get("order/"+str(prop.id),0))*512.0
		if prop.get("validate_directional_layout",false):
			# Studio defaults to free placement, including older saves that omit the flag.
			# Match its authored sizes/positions; only reject completely detached stale art.
			if selected.get("__free_placement",true) and Rect2(-240,-300,480,540).intersects(room.prop_visual_bounds(prop)):
				continue
			# Constrained layouts retain the directional clearance guard.
			var envelope := Rect2(-180,-198,360,378)
			if prop.get("wall_mount",false):
				var half: float=(room.Geometry.CELL+room.Geometry.WALL)*0.5
				envelope=Rect2(-half,-half,half*2,half*2)
			var valid := envelope.encloses(room.prop_visual_bounds(prop))
			for side in range(4):
				if not room.Geometry.has_port(room.layout[0],side): continue
				var lane := Rect2(-36,-180,72,180) if side==0 else (Rect2(0,-36,180,72) if side==1 else (Rect2(-36,0,72,180) if side==2 else Rect2(-180,-36,180,72)))
				if prop.rect.intersects(lane): valid=false
			if not valid:
				resize_prop(prop,[1.0,1.0])
				move_prop(prop,prop.layout_default)

	room.set_meta("layout_apply_signature",hash([asset,room.quarter,selected,room.props]))
	return true

static func is_common_decoration(prop: Dictionary) -> bool:
	if prop.get("registration",{}).get("dressing",false): return true
	for field in ["id","copy_source","variant_source","portable_id"]:
		if str(prop.get(field,"")).begins_with("library/common-"): return true
	return false

static func surface_positions(room: Node) -> Dictionary:
	if room.has_meta("layout_draft"): return room.get_meta("layout_draft")
	return positions(str(room.get_meta("layout_asset","")),room.quarter)

static func resize_prop(prop: Dictionary, value) -> void:
	if prop.has("flush_region"): return
	if not prop.has("layout_original_size"):
		prop.layout_original_size=prop.rect.size
		prop.layout_original_lift=float(prop.get("visual_y_offset",0.0))
	var scale_value:=1.0
	if value is Array and value.size()==2 and (value[0] is float or value[0] is int):
		if is_finite(float(value[0])): scale_value=clampf(float(value[0]),0.25,2.0)
	prop.rect.size=prop.layout_original_size*scale_value
	if prop.has("visual_y_offset"): prop.visual_y_offset=prop.layout_original_lift*scale_value
	prop.sort_y=prop.rect.end.y

static func flip_axes(room: Node, id: String) -> Vector2:
	var value=surface_positions(room).get("flip/"+id,[false,false])
	if not value is Array or value.size()!=2: return Vector2.ONE
	return Vector2(-1 if value[0] else 1,-1 if value[1] else 1)

static func draw_flip(room, canvas: CanvasItem, prop: Dictionary, origin: Vector2, scale_value: float) -> void:
	# Dictionary.get evaluates its fallback even when the cached value exists.
	var axes: Vector2=prop.layout_flip if prop.has("layout_flip") else flip_axes(room,str(prop.id))
	var center: Vector2=room.prop_visual_bounds(prop).get_center()
	canvas.draw_set_transform(origin+(center-center*axes)*scale_value,0,axes*scale_value)

static func save_many(layouts: Dictionary) -> Error:
	ensure_loaded()
	var next:=data.duplicate(true)
	for id in layouts:
		if layouts[id].is_empty(): next.erase(id)
		else: next[id]=layouts[id].duplicate(true)
	return write_data(next)

static func copies(room, values: Dictionary) -> void:
	var catalogs: Dictionary=room.get_meta("layout_copy_sources",{})
	var sources: Dictionary=catalogs.get(room.quarter,{})
	for original in room.props:
		if not original.has("copy_source") and not original.get("library_asset",false): sources[str(original.id)]=original.duplicate(true)
	catalogs[room.quarter]=sources; room.set_meta("layout_copy_sources",catalogs)
	room.props=room.props.filter(func(prop): return not prop.has("copy_source"))
	for id in values:
		if not str(id).begins_with("copy/") or not values[id] is Array: continue
		var source: String=str(values.get("source/"+id,""))
		for original in sources.values():
			if str(original.id)!=source: continue
			var prop: Dictionary=original.duplicate(true)
			prop.id=id; prop.copy_source=source
			room.props.append(prop)
			break

static var asset_paths: Dictionary={}
static func asset_for(room) -> String:
	if "room_id" in room: return "room-"+str(room.room_id)
	if asset_paths.is_empty():
		for entry in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json")):
			asset_paths[entry.view]=entry.asset
	return str(asset_paths.get(room.get_script().resource_path,""))

static func surface_copies(items: Array, values: Dictionary) -> Array:
	var result: Array=items.duplicate(true)
	for id in values:
		if not str(id).begins_with("copy/") or not values[id] is Array: continue
		var source: String=str(values.get("source/"+id,""))
		for original in items:
			if str(original.id)!=source: continue
			var item: Dictionary=original.duplicate(true)
			item.id=id
			var at:=Vector2(values[id][0],values[id][1])
			if item.has("at"):
				item.rect.position+=at-item.at; item.at=at
			else: item.rect.position=at
			result.append(item)
			break
	return result

static func navigation_stamp(layouts: Dictionary) -> int:
	var relevant: Dictionary={}
	for layout in layouts:
		var entries: Dictionary={}
		for key in layouts[layout]:
			var id:=str(key)
			if id=="__free_placement" or (not id.contains("/") and not id.begins_with("__")) or id.begins_with("library/") or id.begins_with("copy/") or id.begins_with("source/") or id.begins_with("portable/") or id.begins_with("size/") or id.begins_with("flip/") or id.begins_with("hidden/"):
				if id.begins_with("hidden/light/") or id.begins_with("hidden/riser/") or id.begins_with("hidden/decor/"): continue
				entries[id]=layouts[layout][key]
		if not entries.is_empty(): relevant[layout]=entries
	return hash(relevant)
