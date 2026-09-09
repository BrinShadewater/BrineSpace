extends RefCounted
## Shared source registration and placement; original room shells remain authoritative.
const Geometry = preload("res://tools/modular_room_geometry.gd")
var art: ImageTexture
var registration: Dictionary
var profiles := {}
var asset_id: String
var placement_reports := {}
var side_views := {}
var activity_layout: Dictionary={}

func _init(id: String) -> void:
	asset_id=id
	activity_layout=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/activity-layouts.json")).get(id,{})
	var data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/registrations/"+id+".json"))
	var image := Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes(data.source))==OK)
	art=ImageTexture.create_from_image(image)
	registration=decode_registration(data)
	for side in ["west","east","south"]:
		var path: String = "res://rooms/full-wall-v1/registrations/side-"+id+"-"+side+".json"
		if not FileAccess.file_exists(path): continue
		var side_data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
		var side_image := Image.new()
		assert(side_image.load_png_from_buffer(FileAccess.get_file_as_bytes(side_data.source))==OK)
		side_views[side]={"art":ImageTexture.create_from_image(side_image),"registration":decode_registration(side_data)}

func decode_registration(data: Dictionary) -> Dictionary:
	var r: Array=data.region
	var pieces: Array=[]
	for polygon in data.pieces:
		var points := PackedVector2Array()
		for point in polygon: points.append(Vector2(point[0],point[1]))
		pieces.append(points)
	return {"wall_mount":data.has("wall_contact"),"pieces":pieces,"pivot":Vector2(r[0]+r[2]*0.5,r[1]+r[3]),"width":float(r[2]),"height":float(r[3]),"outline":[Vector2(r[0],r[1]),Vector2(r[0]+r[2],r[1]),Vector2(r[0]+r[2],r[1]+r[3]),Vector2(r[0],r[1]+r[3])]}

func owns(prop: Dictionary) -> bool:
	return prop.get("full_wall",false)

func bounds(prop: Dictionary) -> Rect2:
	var height: float=prop.rect.size.x*prop.registration.height/prop.registration.width
	return Rect2(prop.rect.position.x,prop.rect.end.y-height+float(prop.get("visual_y_offset",0.0)),prop.rect.size.x,height)

func apply(room) -> void:
	if asset_id in ["pressure-manifold-wall","deepwater-listening-wall"] and room.quarter==0:
		preload("res://scripts/room_layout_store.gd").apply(room,asset_id)
		return # Retain the accepted q0 originals.
	for prop in room.props:
		if owns(prop):
			preload("res://scripts/room_layout_store.gd").apply(room,asset_id)
			return
	var north: bool=Geometry.has_port(room.layout[0],0)
	var south: bool=Geometry.has_port(room.layout[0],2)
	var side := ""
	var source: Dictionary=registration
	var new_directional: bool = asset_id in ["research-analysis-wall","medical-treatment-wall","pressure-manifold-wall","deepwater-listening-wall","xeno-containment-wall","emergency-isolation-wall","tidal-condensation-wall","biodome-habitat-wall","thermal-control-wall","anomaly-containment-wall","radio-signal-wall"] and room.quarter%2==1 and not (Geometry.has_port(room.layout[0],1) and Geometry.has_port(room.layout[0],3))
	if (north and south) or new_directional:
		side="west" if not Geometry.has_port(room.layout[0],3) else "east"
		if not Geometry.has_port(room.layout[0],1) and (room.quarter==2 or (asset_id in ["radio-signal-wall","quarantine-specimen-wall"] and room.quarter==3)): side="east"
		if not side_views.has(side):
			restore_profiles(room)
			return
		source=side_views[side].registration
	var south_bank: bool=side.is_empty() and north and not south and side_views.has("south")
	if south_bank: source=side_views.south.registration
	var width := 344.0
	if not north: width=minf(width,134.0*source.width/source.height)
	if not side.is_empty(): width=minf(120.0,344.0*source.width/source.height)
	var height: float=width*source.height/source.width
	# Authored directional sources face into the room from their mounting wall.
	var bottom := -174.0+height if not north else 174.0
	var x := -width*0.5
	var depth := height if not north else 42.0
	if south_bank and source.get("wall_mount",false):
		bottom=(Geometry.CELL-Geometry.WALL)*0.5
		depth=height
	if not side.is_empty():
		var wall_inner: float=Geometry.CELL*0.5-Geometry.WALL*0.5 if source.get("wall_mount",false) else 174.0
		x=-wall_inner if side=="west" else wall_inner-width
		bottom=height*0.5
		depth=height
	var prop := {"id":"full_wall_"+asset_id,"full_wall":true,"wall_mount":source.get("wall_mount",false),"side_view":side,"validate_directional_layout":new_directional or (asset_id in ["tidal-condensation-wall","biodome-habitat-wall","thermal-control-wall","salvage-disassembly-wall","construction-fabrication-wall","anomaly-containment-wall","radio-signal-wall"] and not side.is_empty()),"rect":Rect2(x,bottom-depth,width,depth),"center":Vector2.ZERO,"sort_y":bottom,"registration":source}
	if south_bank: prop.side_view="south"
	# Every new rollout bank uses safe draft fallback, including horizontal poses.
	if asset_id in ["salvage-disassembly-wall","construction-fabrication-wall","anomaly-containment-wall","radio-signal-wall","shield-pressure-wall","quarantine-specimen-wall","medical-diagnostic-wall","medical-records-wall","biomass-processing-wall"]:
		prop.validate_directional_layout=true
	# Lift artwork into the low north crown; collision remains on the floor.
	prop["visual_y_offset"] = -22.0 if not north and side.is_empty() else 0.0
	var fleet: String={"drone-service-wall":"mining","salvage-disassembly-wall":"salvage","construction-fabrication-wall":"construction"}.get(asset_id, "")
	var replaced: Array=[]
	if "life_items" in room:
		for item in room.life_items:
			if item.rect.get_center().y<0 and not item.get("dressing",false): replaced.append(item.id)
	if asset_id=="mycelium-cultivation-wall": replaced.append_array(["rack","reservoir"])
	if asset_id=="pressure-manifold-wall": replaced.append("flush_back")
	# The live mining vehicle and its launch hatch keep their existing deployment behavior.
	if not fleet.is_empty():
		replaced.erase(fleet+"_rov")
		replaced.erase(fleet+"_hatch")
	var kept: Array=[]
	var displaced: Array=[]
	var visual := bounds(prop).grow(5)
	var initial_props: Array=room.props.duplicate()
	if fleet in ["salvage","construction"]:
		initial_props.sort_custom(func(a,b): return int(a.id in [fleet+"_rov",fleet+"_hatch"])>int(b.id in [fleet+"_rov",fleet+"_hatch"]))
	for existing in initial_props:
		if asset_id in ["quarantine-specimen-wall","medical-diagnostic-wall","medical-records-wall"]:
			displaced.append(existing)
			continue
		if existing.id in replaced:
			displaced.append(existing)
			continue
		if not fleet.is_empty() and existing.id in [fleet+"_rov",fleet+"_hatch"]:
			# Operational vehicle and launch aperture remain present, separate from the service robot.
			var at := Vector2(112,118) if existing.id==fleet+"_rov" else Vector2(-112,118)
			if not side.is_empty(): at=Vector2(112 if side=="west" else -112,-100 if existing.id==fleet+"_rov" else 118)
			existing.rect.position=at-existing.rect.size*0.5
			if fleet!="mining": existing.relocated=true
			existing.sort_y=existing.rect.end.y
			kept.append(existing)
			continue
		var hits_reserved := false
		if fleet in ["salvage","construction"]:
			for reserved in kept:
				if room.prop_visual_bounds(existing).grow(7).intersects(room.prop_visual_bounds(reserved)): hits_reserved=true
		if hits_reserved or room.prop_visual_bounds(existing).intersects(visual):
			displaced.append(existing)
			continue
		if not fleet.is_empty() and room.prop_visual_bounds(existing).intersects(Rect2(-170,40,340,134)):
			displaced.append(existing)
			continue
		kept.append(existing)
	kept.append(prop)
	var moved: Array=[]
	for item in kept:
		if item.get("relocated",false): moved.append(item.id)
	var unplaced: Array=[]
	if asset_id=="quarantine-specimen-wall":
		displaced.sort_custom(func(a,b): return int(a.id=="quarantine_berth")>int(b.id=="quarantine_berth"))
	if asset_id=="medical-diagnostic-wall":
		displaced.sort_custom(func(a,b): return int(a.id in ["medical_treatment","medical_imaging"])>int(b.id in ["medical_treatment","medical_imaging"]))
	if asset_id=="medical-records-wall":
		displaced.sort_custom(func(a,b): return int(a.id in ["office_exam","office_consultation"])>int(b.id in ["office_exam","office_consultation"]))
	for old in displaced:
		# Baked perimeter slices have fixed drawing coordinates; never translate their blockers alone.
		if old.has("flush_region"):
			unplaced.append(old.id)
			continue
		var candidate := vacant_placement(room,old,kept)
		if candidate.is_empty(): unplaced.append(old.id)
		else:
			kept.append(candidate)
			moved.append(old.id)
	# Author activity targets, then resolve clearance at each orientation.
	var targets: Dictionary=activity_layout.get("targets",{})
	var movable: Array=[]
	var anchored: Array=[]
	for item in kept:
		if targets.has(item.id) and not item.has("flush_region"): movable.append(item)
		else: anchored.append(item)
	movable.sort_custom(func(a,b): return room.prop_visual_bounds(a).get_area()>room.prop_visual_bounds(b).get_area())
	var pending: Array=movable.duplicate()
	for item in movable:
		pending.erase(item)
		var desired: Array=targets[item.id]
		var target: Vector2=Geometry.turn(Vector2(desired[0],desired[1]),room.quarter)
		var candidate:=vacant_placement(room,item,anchored+pending,target)
		if candidate.is_empty(): anchored.append(item)
		else:
			anchored.append(candidate)
			if item.id not in moved: moved.append(item.id)
	kept=anchored
	placement_reports[room.quarter]={"relocated":moved,"no_clear_space":unplaced,"activity":activity_layout.get("purpose","")}
	room.props=kept
	# Remove service leads whose furniture was replaced; retain supported details on survivors.
	var ids: Array=[]
	for existing in kept: ids.append(existing.id)
	for name in ["dressing","cryo_dressing","center_dressing","office_dressing"]:
		if not name in room: continue
		var dressing=room.get(name)
		if dressing==null: continue
		if not profiles.has(name): profiles[name]=dressing.profile.duplicate(true)
		dressing.profile=profiles[name].duplicate(true)
		# The saved profile remains complete; active attachments follow surviving hosts.
		for key in ["furniture","mats","supported"]:
			var active: Array=[]
			for item in dressing.profile.get(key,[]):
				var host_id: String=str(item.id if key=="furniture" else item.host)
				if host_id in ids: active.append(item)
			dressing.profile[key]=active
		for key in ["routes","surface_routes"]:
			var routes: Array=[]
			for route in dressing.profile.get(key,[]):
				if route.from.host in ids and route.to.host in ids and route.from.host not in moved and route.to.host not in moved: routes.append(route)
			dressing.profile[key]=routes
	preload("res://scripts/room_layout_store.gd").apply(room,asset_id)

func vacant_placement(room, original: Dictionary, occupied: Array, target:=Vector2.INF) -> Dictionary:
	var before: Rect2=room.prop_visual_bounds(original)
	var best := {}
	var best_distance := INF
	for y in range(-168,169,12):
		for x in range(-168,169,12):
			var shift := Vector2(x,y)-before.position
			var art_bounds := Rect2(before.position+shift,before.size)
			var ground := Rect2(original.rect.position+shift,original.rect.size)
			if not Rect2(-174,-174,348,348).encloses(art_bounds): continue
			if not Rect2(-174,-174,348,348).encloses(ground): continue
			var blocked := false
			for side in range(4):
				if not Geometry.has_port(room.layout[0],side): continue
				var lane := Rect2(-42,-180,84,180) if side==0 else (Rect2(0,-42,180,84) if side==1 else (Rect2(-42,0,84,180) if side==2 else Rect2(-180,-42,180,84)))
				if ground.intersects(lane): blocked=true; break
			if blocked: continue
			for other in occupied:
				if art_bounds.grow(7).intersects(room.prop_visual_bounds(other)) or ground.grow(7).intersects(other.rect): blocked=true; break
			var distance: float=shift.length_squared() if target==Vector2.INF else art_bounds.get_center().distance_squared_to(target)
			if blocked or distance>=best_distance: continue
			var candidate: Dictionary=original.duplicate(true)
			candidate.rect=ground
			candidate.sort_y=ground.end.y
			if candidate.has("art_offset"): candidate.art_offset+=shift
			candidate.relocated=true
			best=candidate
			best_distance=distance
	return best

func restore_profiles(room) -> void:
	for name in profiles:
		var dressing=room.get(name)
		if dressing!=null: dressing.profile=profiles[name].duplicate(true)

func draw(room, prop: Dictionary) -> void:
	var selected: Dictionary=prop.registration
	var texture: ImageTexture=prop.library_texture if prop.get("library_asset",false) else (art if prop.get("side_view","").is_empty() else side_views[prop.side_view].art)
	var scale: float=prop.rect.size.x/selected.width
	var anchor := Vector2(prop.rect.get_center().x,prop.rect.end.y+float(prop.get("visual_y_offset",0.0)))
	for polygon in selected.pieces:
		var points := PackedVector2Array()
		var uv := PackedVector2Array()
		for point in polygon:
			points.append(anchor+(point-selected.pivot)*scale)
			uv.append(point/Vector2(texture.get_size()))
		room.painter.draw_polygon(points,PackedColorArray([Color.WHITE]),uv,texture)
