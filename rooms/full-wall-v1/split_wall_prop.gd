extends "res://rooms/full-wall-v1/full_wall_prop.gd"
## Independently authored sections leave the cross-room doorway approach open.
var sections := {}
var placement_passes := 0
var specification: Dictionary

func _init(id: String) -> void:
	super(id)
	specification=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/split-"+id+".json"))
	for direction in ["north","east","south","west"]:
		sections[direction]=[]
		for section in specification.sections:
			var data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/registrations/"+id+"-"+direction+"-"+section+".json"))
			var image := Image.new()
			preload("res://scripts/safe_image.gd").load_png(image, data.source)
			sections[direction].append({"registration":decode_registration(data),"texture":ImageTexture.create_from_image(image),"section":section})

func apply(room) -> void:
	# Configuration runs every frame for shared views. Relocate only changed geometry.
	var signature := hash([asset_id,room.quarter,room.layout,room.props])
	if room.get_meta("split_wall_signature",-1)==signature:
		if preload("res://scripts/room_layout_store.gd").apply(room,asset_id):
			room.set_meta("split_wall_signature",hash([asset_id,room.quarter,room.layout,room.props]))
		return
	placement_passes+=1
	var direction: String=["north","east","south","west"][room.quarter]
	var kept: Array=[]
	var inner: float=(Geometry.CELL-Geometry.WALL)*0.5
	for index in range(2):
		var section: Dictionary=sections[direction][index]
		var reg: Dictionary=section.registration
		var horizontal: bool=direction in ["north","south"]
		var span := 136.0
		var width: float=span if horizontal else minf(100,span*reg.width/reg.height)
		var height: float=width*reg.height/reg.width
		var along: float=-inner if index==0 else inner-span
		var position := Vector2(along,-inner if direction=="north" else inner-height) if horizontal else Vector2(-inner if direction=="west" else inner-width,along)
		kept.append({"id":"full_wall_"+asset_id+"_"+section.section,"full_wall":true,"wall_mount":true,"split_wall":true,"validate_directional_layout":true,"side_view":direction,"rect":Rect2(position,Vector2(width,height)),"sort_y":position.y+height,"registration":reg,"split_texture":section.texture})
	var candidates: Array=room.props.filter(func(item): return not owns(item) and item.id not in specification.replaces)
	candidates.sort_custom(func(a,b): return int(a.id in specification.preserve)>int(b.id in specification.preserve))
	var moved: Array=[]
	var unplaced: Array=[]
	for original in candidates:
		var candidate := vacant_placement(room,original,kept)
		if candidate.is_empty(): unplaced.append(original.id)
		else:
			kept.append(candidate)
			moved.append(original.id)
	room.props=kept
	placement_reports[room.quarter]={"relocated":moved,"no_clear_space":unplaced}
	# Restore the complete source profile before resolving active hosts each rotation.
	for name in ["dressing","cryo_dressing","center_dressing","office_dressing"]:
		if not name in room or room.get(name)==null: continue
		var dressing=room.get(name)
		if not profiles.has(name): profiles[name]=dressing.profile.duplicate(true)
		dressing.profile=profiles[name].duplicate(true)
		var ids: Array=kept.map(func(item): return item.id)
		for key in ["furniture","mats","supported"]:
			dressing.profile[key]=dressing.profile.get(key,[]).filter(func(item): return (item.id if key=="furniture" else item.host) in ids)
		for key in ["routes","surface_routes"]:
			dressing.profile[key]=dressing.profile.get(key,[]).filter(func(route): return route.from.host in ids and route.to.host in ids and route.from.host not in moved and route.to.host not in moved)
	preload("res://scripts/room_layout_store.gd").apply(room,asset_id)
	room.set_meta("split_wall_signature",hash([asset_id,room.quarter,room.layout,room.props]))

func draw(room, prop: Dictionary) -> void:
	if prop.get("library_asset",false):
		preload("res://scripts/room_asset_library.gd").draw(room,prop)
		return
	var reg: Dictionary=prop.registration
	var scale: float=prop.rect.size.x/reg.width
	var anchor := Vector2(prop.rect.get_center().x,prop.rect.end.y)
	for polygon in reg.pieces:
		var points := PackedVector2Array()
		var uv := PackedVector2Array()
		for point in polygon:
			points.append(anchor+(point-reg.pivot)*scale)
			uv.append(preload("res://scripts/room_asset_library.gd").source_uv(reg,point)/Vector2(prop.split_texture.get_size()))
		room.painter.draw_polygon(points,PackedColorArray([Color.WHITE]),uv,prop.split_texture)
