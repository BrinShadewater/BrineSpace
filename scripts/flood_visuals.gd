extends RefCounted
const SurfaceShader = preload("res://scripts/flood_surface.gdshader")
const SubmersionShader = preload("res://scripts/flood_submersion.gdshader")
const Corridor = preload("res://rooms/underwater/corridor_geometry.gd")
const Geometry = preload("res://tools/modular_room_geometry.gd")

static func shape(room: Dictionary) -> PackedVector2Array:
	if room.id in ["corridor","corner","tee_corridor"]:
		var points := PackedVector2Array()
		for point in Corridor.floor_for(room.id=="corner",room.id=="tee_corridor"):
			points.append(Geometry.turn(point,Corridor.rotation(room)))
		return points
	return PackedVector2Array([Vector2(-180,-180),Vector2(180,-180),Vector2(180,180),Vector2(-180,180)])

static func update_surfaces(grid,game,rooms: Array,size: float) -> void:
	var visible := {}
	var clock: float = game.get_visual_time_seconds()
	for room in rooms:
		var water := float(room.get("water_level",1.0 if room.get("flooded",false) else 0.0))
		if water<=0.001: continue
		visible[room.pos]=true
		if not grid.flood_surfaces.has(room.pos):
			var surface := Polygon2D.new()
			surface.material=ShaderMaterial.new()
			surface.material.shader=SurfaceShader
			grid.surface_passes[grid.Surface.FLOOR].add_child(surface)
			grid.flood_surfaces[room.pos]=surface
		var surface: Polygon2D=grid.flood_surfaces[room.pos]
		var key := [room.id,room.get("rotation",0)]
		if surface.get_meta("shape_key",[])!=key:
			surface.polygon=shape(room)
			surface.set_meta("shape_key",key)
		surface.position=(Vector2(room.pos)+Vector2.ONE*0.5)*size
		surface.scale=Vector2.ONE*size/384.0
		surface.material.set_shader_parameter("depth",water)
		surface.material.set_shader_parameter("clock",clock)
		surface.show()
	for cell in grid.flood_surfaces.keys():
		if not game.occupied.has(cell):
			grid.flood_surfaces[cell].queue_free()
			grid.flood_surfaces.erase(cell)
		elif not visible.has(cell): grid.flood_surfaces[cell].hide()

static func prop_material(slot: Node2D,prop: Dictionary,water: float,clock: float,origin: Vector2,scale: float) -> void:
	if water<=0.001:
		if slot.material!=null:
			slot.material=null
			slot.remove_meta("flood_parameters")
		return
	if slot.material==null:
		slot.material=ShaderMaterial.new()
		slot.material.shader=SubmersionShader
		slot.remove_meta("flood_parameters")
	var line: Vector2=origin+Vector2(0,prop.rect.end.y-water*76.0)*scale
	var transform := slot.get_global_transform()
	line=transform*line
	var parameters := [line.y,scale*transform.get_scale().y,water]
	if slot.get_meta("flood_parameters",[])!=parameters:
		slot.material.set_shader_parameter("waterline_y",parameters[0])
		slot.material.set_shader_parameter("world_scale",parameters[1])
		slot.material.set_shader_parameter("depth",water)
		slot.set_meta("flood_parameters",parameters)
	slot.material.set_shader_parameter("clock",clock)

static func draw_crew_shadow(canvas,foot: Vector2,water: float) -> void:
	var depth := clampf(water,0,1)
	var width := lerpf(6,15,smoothstep(0.25,0.85,depth))
	for layer in range(3):
		var radius := 1.0+layer*0.45
		var points := PackedVector2Array()
		for i in range(20):
			var angle := TAU*i/20.0
			points.append(foot+Vector2(cos(angle)*width,sin(angle)*width*0.36)*radius+Vector2(0,depth*5))
		canvas.draw_colored_polygon(points,Color(0.01,0.04,0.05,lerpf(0.10,0.018,depth)/(1+layer)))

static func crew_waterline(foot_y: float,water: float,swimming: bool) -> float:
	# Standing sprites use feet as pivot; swimmers use shoulders.
	return foot_y-lerpf(-3,25,clampf((water-0.55)/0.45,0,1)) if swimming else foot_y-water/0.55*42.0

static func draw_crew(canvas,texture: Texture2D,rect: Rect2,foot: Vector2,water: float,clock: float) -> void:
	if water<=0.001:
		canvas.draw_texture_rect(texture,rect,false)
		return
	var swimming: bool=texture.get_meta("crew_water_pose",false)
	if texture.get_meta("companion_surface",false):
		# Buoyant companions remain at the surface, even in a full compartment.
		var fraction:float=float(texture.get_meta("companion_surface_line",73.0))/float(texture.get_height())
		var line:float=rect.position.y+rect.size.y*fraction
		var size:=Vector2(texture.get_size())
		canvas.draw_texture_rect_region(texture,Rect2(rect.position,Vector2(rect.size.x,rect.size.y*fraction)),Rect2(Vector2.ZERO,Vector2(size.x,size.y*fraction)))
		canvas.draw_texture_rect_region(texture,Rect2(Vector2(rect.position.x,line),Vector2(rect.size.x,rect.size.y*(1-fraction))),Rect2(Vector2(0,size.y*fraction),Vector2(size.x,size.y*(1-fraction))),Color(.35,.7,.73,.48))
		draw_crew_wake(canvas,Vector2(foot.x,line),texture,clock,10)
		return
	if swimming:
		var submersion := clampf((water-0.55)/0.45,0,1)
		canvas.draw_texture_rect(texture,rect,false,Color(0.37,0.71,0.74,lerpf(0.70,0.23,submersion)))
		var facing: String=texture.get_meta("crew_water_facing","east")
		var offset: Vector2={"east":Vector2(22,-6),"west":Vector2(-22,-6),"north":Vector2(0,-12),"south":Vector2(0,14)}.get(facing,Vector2.ZERO)
		if texture.get_meta("crew_water_kind","")=="tread": offset=Vector2(0,-13)
		var head := foot+offset
		if water<0.85:
			var points := PackedVector2Array()
			var uv := PackedVector2Array()
			for i in range(24):
				var angle := TAU*i/24.0
				var point := head+Vector2(cos(angle)*13,sin(angle)*12)
				points.append(point)
				uv.append((point-rect.position)/rect.size)
			canvas.draw_polygon(points,PackedColorArray([Color(1,1,1,1-submersion*0.5)]),uv,texture)
			draw_crew_wake(canvas,head+Vector2(0,5),texture,clock,14.0)
		else:
			for i in range(3):
				var phase := fposmod(clock*0.7+i*0.33,1.0)
				canvas.draw_arc(head+Vector2(sin(clock*2+i)*3,-phase*23),1+phase,0,TAU,10,Color(0.6,0.8,0.78,(1-phase)*0.65),0.7,true)
		return
	var line := crew_waterline(foot.y,water,swimming)+sin(clock*2.0)*0.55
	var fraction := clampf((line-rect.position.y)/rect.size.y,0,1)
	var tex := Vector2(texture.get_size())
	if fraction>0:
		canvas.draw_texture_rect_region(texture,Rect2(rect.position,Vector2(rect.size.x,rect.size.y*fraction)),Rect2(Vector2.ZERO,Vector2(tex.x,tex.y*fraction)))
	if fraction<1:
		canvas.draw_texture_rect_region(texture,Rect2(Vector2(rect.position.x,line),Vector2(rect.size.x,rect.end.y-line)),Rect2(Vector2(0,tex.y*fraction),Vector2(tex.x,tex.y*(1-fraction))),Color(0.30,0.66,0.70,0.35 if water<0.85 else 0.22))
	draw_crew_wake(canvas,Vector2(foot.x,line),texture,clock,8.0)

static func draw_crew_wake(canvas,contact: Vector2,texture: Texture2D,clock: float,width: float) -> void:
	var facing: String=texture.get_meta("crew_water_facing","south")
	var direction: Vector2={"east":Vector2.RIGHT,"west":Vector2.LEFT,"north":Vector2.UP,"south":Vector2.DOWN}.get(facing,Vector2.DOWN)
	var side := Vector2(-direction.y,direction.x)
	var kind: String=texture.get_meta("crew_water_kind","")
	var moving := kind in ["walk","swim"]
	# Two separated, tapered disturbances leave the front and center open.
	# Moving poses trail behind the body; idle/treading only stirs nearby water.
	for bank in [-1,1]:
		var previous := Vector2.ZERO
		for i in range(9):
			var t := i/8.0
			var pulse := sin(clock*3.1+bank*1.7-t*4)
			var lateral := width*(0.58+t*0.45)+pulse*0.6
			var behind := lerpf(-2.0,20.0 if moving else 6.0,t)
			var offset: Vector2 = side*lateral*float(bank)-direction*behind
			offset.y*=0.38
			var point: Vector2 = contact+offset
			if i>0:
				var alpha := sin(PI*(t-0.0625))*0.28*(0.85+sin(clock*2+bank)*0.15)
				canvas.draw_line(previous,point,Color(0.62,0.76,0.72,alpha),0.7,true)
			previous=point

static func draw_door_currents(canvas,game,room: Dictionary,center: Vector2,scale: float,time: float) -> void:
	if room.get("isolated",false): return
	var water := float(room.get("water_level",0))
	for direction in [Vector2i.RIGHT,Vector2i.DOWN]:
		var cell: Vector2i=room.pos+direction
		if not game.occupied.has(cell): continue
		var neighbor: Dictionary=game.occupied[cell]
		var difference := water-float(neighbor.get("water_level",0))
		if maxf(water,float(neighbor.get("water_level",0)))<=0.015:
			game.grid_view.door_wet_history.erase([room.pos,cell])
			continue
		if neighbor.get("isolated",false): continue
		if not game._placed_rooms_connected(room,neighbor,direction): continue
		var aperture := float(game.grid_view._door_frame_for_pair(game,room.pos,cell))/float(game.grid_view.DOOR_OPEN_FRAMES-1)
		var key: Array=[room.pos,cell]
		var wet=preload("res://rooms/doors/door_water.gd")
		var state: Dictionary=wet.advance(game.grid_view.door_wet_history.get(key,{}),roundi(aperture*9),time)
		game.grid_view.door_wet_history[key]=state
		wet.draw(canvas,center+Vector2(direction)*192*scale,Vector2(direction),aperture,difference,maxf(water,float(neighbor.get("water_level",0))),float(state.closing_until)>time,time,scale)
		if absf(difference)<0.015: continue
		if aperture<=0: continue
		var flow := Vector2(direction)*signf(difference)
		var across := Vector2(-flow.y,flow.x)
		var mouth := center+Vector2(direction)*192*scale
		for i in range(3):
			var phase := fposmod(time*(0.6+absf(difference))+i/3.0,1.0)
			var point := mouth+flow*(phase-0.5)*26*scale
			var alpha := sin(phase*PI)*minf(0.5,absf(difference)*2)*aperture
			canvas.draw_polyline(PackedVector2Array([point-flow*2*scale-across*5*scale,point,point-flow*2*scale+across*5*scale]),Color(0.56,0.83,0.81,alpha),maxf(0.7,scale),true)

static func draw_leak(canvas,origin: Vector2,scale: float,severity: float,water: float,time: float) -> void:
	if severity<=0: return
	# Stable fractured metal, with a narrow bright bevel against a dark opening.
	var fracture := PackedVector2Array()
	var shape: Array
	if severity<=0.35:
		shape=[Vector2(-3,-3),Vector2(0,1),Vector2(-2,5),Vector2(0,9)]
	elif severity<=0.7:
		shape=[Vector2(-13,0),Vector2(-7,2),Vector2(-3,-1),Vector2(2,4),Vector2(0,9),Vector2(9,7),Vector2(14,9)]
	else:
		shape=[Vector2(-8,-5),Vector2(-3,-2),Vector2(-5,2),Vector2(1,5),Vector2(-2,10),Vector2(3,14)]
		canvas.draw_colored_polygon(PackedVector2Array([origin+Vector2(-6,0)*scale,origin+Vector2(4,3)*scale,origin+Vector2(5,10)*scale,origin+Vector2(-3,12)*scale]),Color(0.025,0.05,0.06,0.95))
	for point in shape:
		fracture.append(origin+point*scale)
	canvas.draw_polyline(fracture,Color(0.035,0.065,0.075,0.95),maxf(1,scale*(1.1+severity*2.1)),true)
	var bevel := PackedVector2Array()
	for point in fracture: bevel.append(point+Vector2(1,0)*scale)
	canvas.draw_polyline(bevel,Color(0.65,0.72,0.68,0.65),maxf(0.7,scale*0.7),true)
	canvas.draw_polyline(PackedVector2Array([origin+Vector2(-5,2)*scale,origin+Vector2(-11,5)*scale,origin+Vector2(-13,3)*scale]),Color(0.05,0.09,0.10,0.85),maxf(0.8,scale),true)
	var mouth := origin+Vector2(0,9)*scale
	var reach := (19+severity*26)*(1-water*0.30)
	var impact := mouth+Vector2(6,reach)*scale
	# A tapered curved stream and broken highlights read as pressurized water.
	var stream := PackedVector2Array()
	for i in range(9):
		var t := i/8.0
		stream.append(mouth+Vector2(6*t+sin(time*8-t*6)*t*1.2,reach*t*t)*scale)
	canvas.draw_polyline(stream,Color(0.36,0.67,0.70,0.28),maxf(1,scale*(2+severity*3)),true)
	canvas.draw_polyline(stream,Color(0.68,0.86,0.84,0.65),maxf(0.7,scale),true)
	for i in range(7):
		var phase := fposmod(time*(1.2+severity)+i*0.137,1.0)
		var spread := sin(i*7.13)*phase*(3+severity*6)
		var point := mouth+Vector2(6*phase+spread,reach*phase*phase)*scale
		canvas.draw_line(point,point+Vector2(spread*0.08,1.5+phase*2)*scale,Color(0.68,0.88,0.86,sin(phase*PI)*0.7),maxf(0.7,scale*0.8),true)
	for i in range(3):
		var phase := fposmod(time*0.85+i/3.0,1.0)
		var ripple := PackedVector2Array()
		for j in range(19):
			var angle := TAU*j/18.0
			ripple.append(impact+Vector2(cos(angle)*(3+phase*15),sin(angle)*(1+phase*5))*scale)
		canvas.draw_polyline(ripple,Color(0.56,0.81,0.78,(1-phase)*0.32*severity),maxf(0.7,scale*0.7),true)

static func draw_repair_torch(canvas,game,room: Dictionary,center: Vector2,scale: float,time: float) -> void:
	var job: Dictionary=room.get("leak_repair",{})
	if str(job.get("worker","")).is_empty() or game.paused: return
	var actor=game.get(str(job.worker)+"_npc")
	if actor.state=="weld": return # Authored dry weld already includes the torch.
	if actor.dead or actor.goal!="hull-repair" or actor.state not in ["weld","repair"] or not actor.path.is_empty(): return
	var foot: Vector2=center+(actor.foot-(Vector2(room.pos)+Vector2.ONE*0.5)*384)*scale
	var tip := foot+Vector2(5,-22)*scale
	canvas.draw_line(foot+Vector2(5,-12)*scale,tip,Color(0.23,0.28,0.25),maxf(1,scale*2),true)
	canvas.draw_line(tip,tip+Vector2(0,-6)*scale,Color(0.4,0.86,0.98,0.8),maxf(1,scale*2),true)
	canvas.draw_circle(tip+Vector2(0,-7)*scale,(1.5+sin(time*37)*0.5)*scale,Color(1,0.9,0.58,0.9))
	for i in range(5):
		var phase := fposmod(time*2.5+i*0.19,1.0)
		var spark := tip+Vector2(sin(i*13.0)*phase*12,-6+phase*phase*15)*scale
		canvas.draw_line(spark,spark+Vector2(0,1.4)*scale,Color(1,0.72,0.32,(1-phase)*0.85),maxf(0.6,scale*0.7),true)

static func draw_front(canvas,game,rooms: Array,size: float) -> void:
	var scale := size/384.0
	for room in rooms:
		var water := float(room.get("water_level",1.0 if room.get("flooded",false) else 0.0))
		var center: Vector2=(Vector2(room.pos)+Vector2.ONE*0.5)*size
		var time: float=game.get_visual_time_seconds()
		draw_door_currents(canvas,game,room,center,scale,time)
		draw_repair_torch(canvas,game,room,center,scale,time)
		if water<=0.001: continue
		if room.id not in ["corridor","corner","tee_corridor"]:
			# Visible water depth on the front cutaway, tied to the same physical height.
			var height := water*52.0*scale
			var bottom := center.y+180*scale
			canvas.draw_rect(Rect2(center.x-180*scale,bottom-height,360*scale,height),Color(0.08,0.34,0.40,0.23+water*0.12))
			var surface := PackedVector2Array()
			for i in range(41):
				var x := -180.0+i*9.0
				surface.append(Vector2(center.x+x*scale,bottom-height+sin(x*0.085+time*1.4)*scale))
			canvas.draw_polyline(surface,Color(0.48,0.75,0.70,0.65),maxf(1,scale*1.2),true)
			draw_leak(canvas,center+Vector2(-70,-184)*scale,scale,float(room.get("hull_crack",0)),water,time)
		var gauge := Rect2(center+Vector2(-175,-170)*scale,Vector2(4,72)*scale)
		if room.id in ["corridor","corner","tee_corridor"]: gauge=Rect2(center+Vector2(-24,-24)*scale,Vector2(4,48)*scale)
		canvas.draw_rect(gauge,Color("0a2027"))
		canvas.draw_rect(Rect2(Vector2(gauge.position.x,gauge.end.y-gauge.size.y*water),Vector2(gauge.size.x,gauge.size.y*water)),Color("db8870") if water>=0.85 else Color("75bab7"))
		for mark in [0.25,0.55,0.85]:
			var y: float=gauge.end.y-gauge.size.y*mark
			canvas.draw_line(Vector2(gauge.position.x-2*scale,y),Vector2(gauge.end.x+2*scale,y),Color(0.65,0.83,0.8,0.8),maxf(1,scale))
