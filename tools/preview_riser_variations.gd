extends "res://tools/preview_riser_room.gd"
## All-room wall-art review, isolated by the same launcher as the accepted study.
const PACK = "res://assets/room-risers-v4/registrations.json"
var registrations: Dictionary = {}
var entries: Array = []
var choice: OptionButton
var selected_index := 0
var decorations: Dictionary = {}
var decor_textures: Dictionary = {}
var fitting_profiles: Dictionary = {}
var integrated: Dictionary = {}
var integrated_textures: Dictionary = {}
var integrated_enabled := true
var decorations_enabled := true
var north_mode := 0 # Room ports, closed interior, exposed ocean.
var north_choice: OptionButton
var room_ports: Array = []
var corridor_quarter := 0

func run() -> void:
	integrated=JSON.parse_string(FileAccess.get_file_as_string("res://assets/room-risers-v4/integrated-v1/registrations.json"))
	for key in integrated: integrated_textures[key]=png(integrated[key].source)
	fitting_profiles=JSON.parse_string(FileAccess.get_file_as_string("res://assets/room-risers-v4/fitting-profiles.json"))
	top_margin=270.0
	center_fraction=0.62
	registrations = JSON.parse_string(FileAccess.get_file_as_string(PACK))
	decorations=JSON.parse_string(FileAccess.get_file_as_string("res://assets/room-risers-v4/panel-decorations.json")).rooms
	for key in decorations:
		for slot in ["left","right","center","ocean_left","ocean_right","ocean_center"]:
			var path: String=decorations[key][slot]
			if not decor_textures.has(path): decor_textures[path]=png(path)
	for entry in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json")):
		if registrations.has(entry.room): entries.append(entry)
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--room="):
			entries=entries.filter(func(entry): return entry.room==arg.trim_prefix("--room="))
	entries.sort_custom(func(a,b): return str(a.room)<str(b.room))
	# Preview-only texture cache uses accepted local exports with unchanged canvases.
	var source_map: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/room-risers-v4/preview-props.json"))
	for source in source_map:
		if FileAccess.file_exists(source_map[source]): Library.source_textures[source]=png(source_map[source])
	await super.run()
	if OS.get_cmdline_user_args().has("--verify"): return
	root.title="BrineSpace — room riser variations"
	var row := HBoxContainer.new()
	control_box.add_child(row)
	button(row,"Previous",func(): select_room(posmod(selected_index-1,entries.size())))
	choice=OptionButton.new()
	for entry in entries: choice.add_item(str(entry.room).replace("_"," ").capitalize())
	choice.item_selected.connect(select_room)
	row.add_child(choice)
	button(row,"Next",func(): select_room(posmod(selected_index+1,entries.size())))
	button(row,"Door / window reserves",func(): guides=not guides)
	var details_row:=HBoxContainer.new()
	control_box.add_child(details_row)
	north_choice=OptionButton.new()
	for label in ["North: room door layout","North: closed interior","North: exposed ocean"]: north_choice.add_item(label)
	north_choice.item_selected.connect(func(index): north_mode=index; apply_north_state())
	details_row.add_child(north_choice)
	button(details_row,"Decorations on / off",func(): decorations_enabled=not decorations_enabled)
	button(details_row,"Integrated / separate",func(): integrated_enabled=not integrated_enabled)
	button(details_row,"Rotate corridor",func(): corridor_quarter=posmod(corridor_quarter+1,4))
	var initial:=0
	for index in range(entries.size()):
		if entries[index].room=="reactor": initial=index
	select_room(initial)
	await capture("v4-interactive")

func select_room(index: int) -> void:
	selected_index=index
	if choice!=null: choice.select(index)
	var entry: Dictionary=entries[index]
	room_id=entry.room
	var database=preload("res://scripts/room_database.gd")
	var definition: Dictionary=database.get_room(room_id)
	preview_ports.clear()
	for direction in database.LAYOUTS[definition.layout].doors:
		preview_ports.append(["north","east","south","west"].find(direction))
	room_ports=preview_ports.duplicate()
	segment_only=room_id in ["corridor","corner","tee_corridor"]
	height=35.0 if segment_only else 79.0
	corridor_quarter=0
	if is_instance_valid(room): room.queue_free()
	room=load(entry.view).new()
	if "room_id" in room: room.room_id=room_id
	room.embedded=true
	root.add_child(room)
	room.hide()
	room.configure_embedded(0,[0,1,2,3],true,elapsed)
	Store.apply(room,entry.asset)
	Library.strip_retired(room)
	room.configure_embedded(0,preview_ports,true,elapsed)
	room.set_meta("layout_editor_preview",true)
	room.set_meta("layout_draft",Store.positions(entry.asset,0))
	room.set_meta("raised_north_visible",true)
	wall=png(registrations[room_id].source)
	if segment_only:
		var art=preload("res://rooms/underwater/corridor_wall_art.gd")
		var records: Dictionary=art.catalog()
		var key: String=art.key(room_id!="corridor",0)
		var reg: Dictionary=registrations[room_id]
		var blank: Array=reg.face.duplicate()
		blank[0]+=blank[2]*0.40
		blank[2]*=0.18
		records[key]={"source":reg.source,"face":reg.face,"cap":reg.cap,"fitted_caps":true,"low":blank,"return":blank}
		art.textures[key]=wall

	actor.signature.clear()
	actor.mode=0 if segment_only else 2
	actor.rebuild(room,room_id,0)
	apply_north_state()
	revised=true
	title_label.text=room_id.replace("_"," ").to_upper()+" / RISER VARIATION"
	update_note()
	canvas.queue_redraw()

func apply_north_state() -> void:
	preview_ports=room_ports.duplicate()
	if room_id=="brine_core":
		if not preview_ports.has(0): preview_ports.append(0)
	elif north_mode!=0: preview_ports.erase(0)
	room.configure_embedded(0,preview_ports,true,elapsed)
	actor.signature.clear()
	actor.rebuild(room,room_id,0)
	if is_instance_valid(note_label): update_note()

func update_note() -> void:
	if room_id=="brine_core":
		note_label.text="BRINE Core: permanent north door; side monitor banks."
	elif segment_only:
		note_label.text="Actual corridor hull; 35-unit risers, bevelled ends and open junctions. Rotate to inspect each facing."
	else:
		note_label.text="Exposed north hull: ocean windows." if north_mode==2 else ("North connection: centre bay reserved for the door." if preview_ports.has(0) else "Closed north wall: room-specific decorations fill all three panels.")

func draw_corridor_study(target: CanvasItem, at: Vector2, factor: float) -> void:
	var geometry=preload("res://rooms/underwater/corridor_geometry.gd")
	var dressing=preload("res://rooms/underwater/corridor_dressing.gd")
	var turn=preload("res://tools/modular_room_geometry.gd")
	var hull: PackedVector2Array=geometry.hull_for(room_id=="corner",room_id=="tee_corridor")
	var q: int=geometry.rotation({"id":room_id,"rotation":corridor_quarter})
	room.configure_embedded(corridor_quarter,room_ports,true,elapsed)
	room.render_into(target,at,factor,true)
	target.draw_set_transform(at,0,Vector2.ONE*factor)
	dressing.draw_risers(target,hull,q,0,1.0)
	# Only true screen-north wall runs receive upright fittings. Side returns
	# and concave junctions retain the canonical hull renderer's low profile.
	if not revised or not decorations_enabled or not integrated_enabled: return
	var record: Dictionary=integrated[room_id]
	var texture: Texture2D=integrated_textures[room_id]
	var face: Array=record.face
	var exits:=corridor_exit_directions(hull,q)
	var wall_run := 0
	for i in range(hull.size()):
		var a: Vector2=turn.turn(hull[i],q)
		var b: Vector2=turn.turn(hull[(i+1)%hull.size()],q)
		if absf(a.y-b.y)>0.01 or b.x-a.x<60 or dressing.is_north_entry(a,b): continue
		var width: float=b.x-a.x-12
		# Route symbols are geometry-driven paint, not rotated baked illustrations.
		# Leave the original raster arrow/map bays out of the shape assembly.
		var sign_at:=Vector2(a.x+6+width*(0.35 if width>180 else 0.5),a.y-16)
		draw_route_marking(target,sign_at,exits)
		if width>180 or wall_run>0:
			var crop:=Rect2(face[0]+face[2]*0.69,face[1],face[2]*0.25,face[3])
			var fitting_width:=crop.size.x*31.0/crop.size.y
			var x: float=a.x+6+width*(0.78 if width>180 else 0.5)-fitting_width*0.5
			if width<=180:
				# Small second arm carries the emergency fitting rather than a duplicate sign.
				var blank: Array=registrations[room_id].face
				target.draw_texture_rect_region(wall,Rect2(a.x,a.y-31,b.x-a.x,31),Rect2(blank[0]+blank[2]*0.4,blank[1],blank[2]*0.18,blank[3]))
			target.draw_texture_rect_region(texture,Rect2(x,a.y-31,fitting_width,31),crop)
		wall_run+=1

func corridor_exit_directions(hull: PackedVector2Array, q: int) -> Array[Vector2]:
	var result: Array[Vector2]=[]
	var turn=preload("res://tools/modular_room_geometry.gd")
	for i in range(hull.size()):
		var a: Vector2=turn.turn(hull[i],q)
		var b: Vector2=turn.turn(hull[(i+1)%hull.size()],q)
		var middle: Vector2=(a+b)*0.5
		if absf(middle.x)>=191.99: result.append(Vector2(signf(middle.x),0))
		elif absf(middle.y)>=191.99: result.append(Vector2(0,signf(middle.y)))
	return result

func draw_route_marking(target: CanvasItem, center: Vector2, exits: Array[Vector2]) -> void:
	var ink:=Color("c4bca7")
	for direction in exits:
		var side:=Vector2(-direction.y,direction.x)
		target.draw_line(center,center+direction*8,ink,2.2,true)
		target.draw_colored_polygon(PackedVector2Array([center+direction*13,center+direction*7+side*4,center+direction*7-side*4]),ink)
	target.draw_circle(center,2.0,ink)

func draw_riser(target: CanvasItem) -> void:
	if not registrations.has(room_id):
		super.draw_riser(target)
		return
	var reg: Dictionary=registrations[room_id]
	var face: Array=reg.face
	# Preserve a 92-unit replaceable centre in furnished and corridor studies.
	var edge:=200.0 if segment_only else 184.0
	var top:=-258.0 if segment_only else -255.0
	for span in [[0.0,0.385,-edge,edge-46.0],[0.385,0.23,-46.0,92.0],[0.615,0.385,46.0,edge-46.0]]:
		var sample: Array=face
		var texture: Texture2D=wall
		if integrated_active() and not (span[2]==-46.0 and preview_ports.has(0)):
			sample=integrated[room_id].face
			texture=integrated_textures[room_id]
		target.draw_texture_rect_region(texture,Rect2(span[2],top,span[3],height),Rect2(sample[0]+sample[2]*span[0],sample[1],sample[2]*span[1],sample[3]))
	if segment_only:
		var cap: Array=reg.cap
		target.draw_texture_rect_region(wall,Rect2(-200,-268,400,10),Rect2(cap[0],cap[1],cap[2],cap[3]))
		draw_panel_decorations(target)
		return
	# The replacement cap pass owns returns and corners as well as long edges.
	draw_panel_decorations(target)

func draw_cap_strip(target: CanvasItem, rect: Rect2, vertical := false, flip_depth := false) -> void:
	var cap: Array=registrations[room_id].cap
	var source:=Rect2(cap[0],cap[1],cap[2],cap[3])
	var length:=rect.size.y if vertical else rect.size.x
	var thickness:=rect.size.x if vertical else rect.size.y
	# Keep the source's pixel density and bevel thickness; crop length, never
	# stretch a tiny square tile into a long structural beam.
	var source_length:=minf(source.size.x,length*source.size.y/thickness)
	source.position.x+=(source.size.x-source_length)*0.5
	source.size.x=source_length
	if vertical or flip_depth:
		var points:=PackedVector2Array([rect.position,Vector2(rect.position.x,rect.end.y),rect.end,Vector2(rect.end.x,rect.position.y)])
		if not vertical: points=PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)])
		var near_y:=source.end.y if flip_depth else source.position.y
		var far_y:=source.position.y if flip_depth else source.end.y
		var uv:=PackedVector2Array([Vector2(source.position.x,near_y),Vector2(source.end.x,near_y),Vector2(source.end.x,far_y),Vector2(source.position.x,far_y)])
		for i in range(4): uv[i]/=Vector2(wall.get_size())
		target.draw_polygon(points,PackedColorArray([Color.WHITE]),uv,wall)
	else:
		target.draw_texture_rect_region(wall,rect,source)

func draw_wall_tops(target: CanvasItem) -> void:
	for side in range(4):
		var vertical:=side==1 or side==3
		var start:=-255.0 if vertical else -184.0
		var finish:=181.0 if vertical else 184.0
		var spans: Array=[[start,finish]]
		if preview_ports.has(side): spans=[[start,-46.0],[46.0,finish]]
		for span in spans:
			var rect:=Rect2(span[0],-271 if side==0 else 181,span[1]-span[0],16)
			if vertical: rect=Rect2(184 if side==1 else -200,span[0],16,span[1]-span[0])
			draw_cap_strip(target,rect,vertical,side==1 or side==2)
	# Replace the legacy jamb finish at the canonical 72-unit door aperture.
	# Keep these in the shell pass so props/crew still occlude them correctly.
	var geometry=preload("res://tools/modular_room_geometry.gd")
	for edge in room.edges:
		if not edge.open: continue
		if edge.horizontal and edge.center.y<0: continue # Raised north door owns its frame.
		for jamb in geometry.jamb_rects(edge):
			var rect: Rect2=jamb
			rect.position.y-=3.0
			var vertical: bool=not edge.horizontal
			draw_cap_strip(target,rect,vertical,edge.center.x>0 if vertical else true)
	# Fitted mitres continue both inward bevels through the corner, without
	# reusing a rounded beam-end sprite with transparent exterior wedges.
	for x in [-200,184]:
		for y in [-271,181]:
			draw_cap_corner(target,Vector2(x,y),x>0,y>0)

func draw_cap_corner(target: CanvasItem, at: Vector2, east: bool, south: bool) -> void:
	var cap: Array=registrations[room_id].cap
	var depth: float=cap[3]
	# Quiet metal between structural fasteners, at exactly the straight cap scale.
	var source:=Rect2(cap[0]+cap[2]*0.2,cap[1],depth,depth)
	var local:=PackedVector2Array([Vector2(0,0),Vector2(16,0),Vector2(16,16),Vector2(0,16)])
	var points:=PackedVector2Array()
	for p in local:
		points.append(at+Vector2(16-p.x if east else p.x,16-p.y if south else p.y))
	var uv:=PackedVector2Array([source.position,Vector2(source.end.x,source.position.y),source.end,Vector2(source.position.x,source.end.y)])
	for i in range(4): uv[i]/=Vector2(wall.get_size())
	# The diagonal joins horizontal and vertical material planes; both bevels
	# meet at the inner vertex and the outside silhouette remains fully covered.
	target.draw_polygon(PackedVector2Array([points[0],points[1],points[2]]),PackedColorArray([Color.WHITE]),PackedVector2Array([uv[0],uv[1],uv[2]]),wall)
	target.draw_polygon(PackedVector2Array([points[0],points[2],points[3]]),PackedColorArray([Color.WHITE]),PackedVector2Array([uv[0],uv[2],uv[1]]),wall)

func fit_decoration(target: CanvasItem, path: String, bounds: Rect2, center_slot := false) -> void:
	var tex: Texture2D=decor_textures[path]
	var profile: Dictionary=fitting_profiles[path]
	var r: Array=profile.region
	var source:=Rect2(r[0],r[1],r[2],r[3])
	var anchor:=Vector2(profile.anchor[0],profile.anchor[1])
	var limits: Array=profile.center_size if center_slot else profile.side_size
	var factor:=minf(limits[0]/source.size.x,limits[1]/source.size.y)
	factor=minf(factor,bounds.size.x/(2.0*source.size.x*maxf(anchor.x,1.0-anchor.x)))
	factor=minf(factor,bounds.size.y/(2.0*source.size.y*maxf(anchor.y,1.0-anchor.y)))
	var dimensions:=source.size*factor
	var destination:=Rect2(bounds.get_center()-dimensions*anchor,dimensions)
	assert(bounds.grow(0.01).encloses(destination),"Wall fitting escaped its reserved panel")
	target.draw_texture_rect_region(tex,destination,source)

func integrated_active() -> bool:
	return integrated_enabled and decorations_enabled and integrated.has(room_id) and (north_mode!=2 or room_id=="brine_core")

func draw_panel_decorations(target: CanvasItem) -> void:
	if integrated_active(): return
	if not decorations_enabled or not decorations.has(room_id): return
	var data: Dictionary=decorations[room_id]
	var exterior:=north_mode==2 and not preview_ports.has(0)
	fit_decoration(target,data.ocean_left if exterior else data.left,Rect2(-141,-246,72,31))
	fit_decoration(target,data.ocean_right if exterior else data.right,Rect2(69,-246,72,31))
	if not preview_ports.has(0):
		fit_decoration(target,data.ocean_center if exterior else data.center,Rect2(-42,-251,84,71),true)

func draw_guides(target: CanvasItem) -> void:
	if segment_only:
		super.draw_guides(target)
		return
	target.draw_rect(Rect2(-46,-255,92,79),Color("e7ba69"),false,1.0)
	for x in [-141,69]: target.draw_rect(Rect2(x,-246,72,31),Color("5cb8d8"),false,1.0)

func verify() -> void:
	assert(is_zero_approx(NewDoor.travel(0.0)) and is_equal_approx(NewDoor.travel(1.0),1.0))
	var previous_travel:=0.0
	for step in range(101):
		var current_travel:=NewDoor.travel(float(step)/100.0)
		assert(current_travel>=previous_travel and current_travel<=1.0,"Door motion must not reverse or overshoot")
		previous_travel=current_travel
	var reviewed:=0
	for index in range(entries.size()):
		north_mode=0
		select_room(index)
		door_amount=0.0
		door_target=0.0
		guides=false
		await capture("v4-"+room_id)
		if not segment_only:
			var travelled:=0.0
			for step in range(40):
				var before: Vector2=actor.foot
				actor.advance(0.1)
				if not actor.segment_clear(before,actor.foot): clearance_failures+=1
				travelled+=before.distance_to(actor.foot)
			assert(travelled>40.0,"Expected a usable walk route in "+room_id)
			print("ROOM REVIEW %s: props=%d walk=%.1f nodes=%d"%[room_id,room.props.size(),travelled,actor.graph.get_point_count()])
			door_amount=1.0
			door_target=1.0
			await capture("v4-"+room_id+"-open")
		if segment_only:
			for rotation in range(4):
				corridor_quarter=rotation
				var geometry=preload("res://rooms/underwater/corridor_geometry.gd")
				var hull: PackedVector2Array=geometry.hull_for(room_id=="corner",room_id=="tee_corridor")
				var directions:=corridor_exit_directions(hull,geometry.rotation({"id":room_id,"rotation":rotation}))
				assert(directions.size()==room_ports.size(),"Route marking exit count differs from room doors")
				for port in room_ports:
					assert(directions.has([Vector2.UP,Vector2.RIGHT,Vector2.DOWN,Vector2.LEFT][posmod(port+rotation,4)]),"Arrow points away from actual door")
				await capture("v4-"+room_id+"-shape-"+str(rotation))
			corridor_quarter=0
		if room_id in ["brine_core","corridor","corner","tee_corridor"]:
			var was_running:=running
			running=false
			for frame in range(25):
				door_amount=float(frame)/24.0
				door_target=door_amount
				await capture("door-v2-"+room_id+"-"+str(frame).pad_zeros(2))
			running=was_running
		north_mode=1
		apply_north_state()
		assert(preview_ports.has(0)==(room_id=="brine_core"))
		await capture("v4-"+room_id+"-decorated")
		north_mode=2
		apply_north_state()
		assert(preview_ports.has(0)==(room_id=="brine_core"))
		await capture("v4-"+room_id+"-ocean")
		reviewed+=1
	assert(clearance_failures==0)
	print("RISER PREVIEW PASS: %d room designs captured; clearance_failures=%d; corridor designs use actual hulls with four rotation captures"%[reviewed,clearance_failures])
	quit()
