extends RefCounted
## Textured raised hull; end returns exist only at exposed riser boundaries.
const Riser=preload("res://rooms/whole-room/riser_geometry.gd")
const Hull=preload("res://assets/riser-wall-kit-style-v2/wall_sprites.gd")
const Fittings=preload("res://assets/wall-dressing-style-v2/wall_sprites.gd")
const Decor=preload("res://rooms/whole-room/decoration_props.gd")
const Catalog=preload("res://rooms/whole-room/riser_catalog.gd")
static var brine_texture: Texture2D

static func draw_into(canvas: CanvasItem, room_id: String, cell := Vector2i.ZERO, adjoining_left := false, adjoining_right := false, wall_view = null) -> void:
	if room_id=="brine_core":
		if brine_texture==null:
			var image:=Image.new()
			preload("res://scripts/safe_image.gd").load_png(image, "res://assets/brine-riser-v1/source.png")
			brine_texture=ImageTexture.create_from_image(image)
		# Use the upper service face at its own aspect, excluding the tall lower cabinets.
		canvas.draw_texture_rect_region(brine_texture,Rect2(-192,Riser.TOP,384,Riser.HEIGHT),Rect2(0,100,2007,342))
		canvas.draw_texture_rect_region(brine_texture,Rect2(-196,Riser.CAP_TOP,392,7),Rect2(0,0,2007,100))
	elif room_id=="airlock":
		preload("res://rooms/underwater/airlock-v4/fittings.gd").draw_wall(canvas,cell)
	else:
		Catalog.face(canvas,room_id,Rect2(-192,Riser.TOP,384,Riser.HEIGHT))
		# Department-specific mounts; windows retain their native aspect ratio.
		var edits: Dictionary={} if wall_view==null else preload("res://scripts/room_layout_store.gd").surface_positions(wall_view)
		for item in (decorations(room_id,edits) if wall_view!=null and wall_view.has_meta("layout_editor_preview") else []):
			if edits.get("hidden/"+item.id,false): continue
			var rect: Rect2=item.rect
			canvas.draw_rect(Rect2(rect.position+Vector2(2,3),rect.size),Color(0,0,0,.13))
			var flip=edits.get("flip/"+item.id,[false,false])
			var u0:=1.0 if flip[0] else 0.0
			var v0:=1.0 if flip[1] else 0.0
			canvas.draw_polygon(PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)]),PackedColorArray([Color(.73,.79,.78)]),PackedVector2Array([Vector2(u0,v0),Vector2(1-u0,v0),Vector2(1-u0,1-v0),Vector2(u0,1-v0)]),item.texture)

		Catalog.cap(canvas,room_id,Rect2(-196,Riser.CAP_TOP,392,7))
		canvas.draw_line(Vector2(-192,Riser.TOP+1),Vector2(192,Riser.TOP+1),Color("23363a"),2)
		canvas.draw_rect(Rect2(-192,-197,384,5),Color("26383b"))
	for left in [true,false]:
		if (left and adjoining_left) or (not left and adjoining_right): continue
		var edge_x := -192.0 if left else 192.0
		# A continuous structural backing closes transparent bevels and the
		# different draw offsets used by each room's wall/cap artwork.
		# Extend beneath the low corner so the two assemblies overlap.
		var joint_color := Color(profile(room_id).tint).darkened(.22)
		canvas.draw_rect(Rect2(edge_x-8,Riser.CAP_TOP-3,16,Riser.HEIGHT+17),joint_color)
		# Reuse the room's actual vertical wall material, extending its corner up.
		if wall_view!=null:
			var saved=wall_view.painter
			wall_view.painter=canvas
			wall_view.draw_wall(Rect2(edge_x-8,Riser.TOP,16,Riser.HEIGHT),false)
			wall_view.draw_cap(Rect2(edge_x-8,Riser.CAP_TOP,16,10))
			wall_view.painter=saved
		else:
			canvas.draw_texture_rect(Hull.texture("structural_rib"),Rect2(edge_x-8,Riser.CAP_TOP,16,Riser.HEIGHT+6),false,Color(.68,.76,.77))
	if wall_view!=null and preload("res://tools/modular_room_geometry.gd").has_port(wall_view.layout[0],0):
		preload("res://rooms/whole-room/room_door.gd").draw_riser_door(canvas,0.0,brine_texture if room_id=="brine_core" else null,preload("res://rooms/doors/department_door.gd").department({"id":room_id}))

static func profile(room_id: String) -> Dictionary:
	if room_id=="brine_core": return {"tint":"c1c5bb","mounts":[]}
	# Mount tuples: source, left edge, maximum width. All sit inside the riser.
	if room_id in ["crew_hab","crew_lounge"]:
		return {"tint":"ab9b83","mounts":[["picture_ocean",-150,38],["ocean_window_medium",-62,76],["wall_planter",65,34],["analog_clock",132,25]]}
	if room_id in ["hydroponics_bay","biodome","mycelium_nursery","biomass_digester"]:
		return {"tint":"899c85","mounts":[["pressure_gauge",-153,28],["ocean_window_panoramic",-79,102],["wall_planter",61,42],["small_access_cover",133,26]]}
	if room_id in ["med_bay","med_center","med_office","clone_lab","cryo_chamber","quarantine_cell"]:
		return {"tint":"a3b1ac","mounts":[["emergency_box",-144,32],["ocean_porthole_small",-24,33],["com_panel",98,37]]}
	if room_id in ["research_lab","xeno_lab","bio_lab","anomaly_lab"]:
		return {"tint":"8e9ca6","mounts":[["sample_display",-151,43],["ocean_twin_portholes",-40,72],["monitor_single",110,41]]}
	if room_id in ["listening_post","radio_lab","command_center"]:
		return {"tint":"768b91","mounts":[["com_handset",-151,26],["ocean_window_panoramic",-71,103],["status_display_wide",84,61]]}
	if room_id in ["brine_core","holographic_core","data_archive","gravity_loom","isolation_vault"]:
		return {"tint":"7e8998","mounts":[["reinforced_access_panel",-148,42],["monitor_dual",-37,72],["com_panel",112,32]]}
	return {"tint":"7c8988","mounts":[["tool_rack",-154,45],["ocean_porthole_small",-31,33],["pressure_gauge",64,27],["small_access_cover",129,28]]}

static func decorations(room_id: String, edits: Dictionary={}) -> Array:
	var result: Array=[]
	if not Decor.WALL_DECORATIONS_ENABLED: return result
	if room_id=="airlock": return result
	var mounts: Array=profile(room_id).mounts
	for i in range(mounts.size()):
		var mount: Array=mounts[i]
		var id: String="riser/"+str(i)+"/"+str(mount[0])
		# Room-specific faces already contain fittings; retain explicitly placed mounts.
		if Catalog.catalog().has(room_id) and not edits.has(id): continue
		var texture: Texture2D=Hull.texture(mount[0]) if Hull.catalog().has(mount[0]) else Fittings.texture(mount[0])
		var box:=Rect2(Vector2(float(mount[1]),-235)+Riser.MOUNT_SHIFT,Vector2(float(mount[2]),34))
		var dimensions:=Vector2(texture.get_size())
		dimensions*=minf(box.size.x/dimensions.x,box.size.y/dimensions.y)
		var rect:=Rect2(box.get_center()-dimensions/2,dimensions)
		var value=edits.get(id)
		if value is Array and value.size()==2: rect.position=Vector2(value[0],value[1])
		result.append({"id":id,"asset":str(mount[0]),"texture":texture,"rect":rect})
	result=preload("res://scripts/room_layout_store.gd").surface_copies(result,edits)
	result.sort_custom(func(a,b): return float(edits.get("order/"+str(a.id),0))<float(edits.get("order/"+str(b.id),0)))
	return result.filter(func(item): return not (edits.has(item.id) and edits[item.id]==null))
