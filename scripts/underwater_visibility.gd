extends RefCounted
## World-cell light sources shared by fog, survey memory and future detection.
const Field = preload("res://scripts/wreck_field.gd")
const MAX_LIGHTS := 48
var material := ShaderMaterial.new()
var mask := Image.create(40,40,false,Image.FORMAT_RGBA8)
var mask_texture: ImageTexture
var last_survey := -1000
var silt_position := Vector2(-100,-100)
var silt_time := -1000.0

func _init() -> void:
	material.shader = preload("res://scripts/underwater_fog.gdshader")
	mask_texture = ImageTexture.create_from_image(mask)
	material.set_shader_parameter("terrain",mask_texture)

func reset() -> void:
	last_survey=-1000
	silt_position=Vector2(-100,-100)
	silt_time=-1000.0

static func valid(value: Variant) -> bool:
	if not value is Dictionary or value.size()>1600: return false
	for cell in value:
		if not cell is Vector2i or cell.x<0 or cell.y<0 or cell.x>=40 or cell.y>=40 or not value[cell] is bool or not value[cell]: return false
	return true

static func clear_ray(field: Dictionary, from: Vector2, to: Vector2) -> bool:
	var steps := maxi(1,ceili(from.distance_to(to)*12))
	for i in range(1,steps):
		var cell := Vector2i(from.lerp(to,float(i)/steps).floor())
		if Field.blocks(field,cell) and cell!=Vector2i(to.floor()): return false # Survey includes the first exposed face.
	return true

static func drone_position(game, drone: Dictionary) -> Vector2:
	var position := Vector2(drone.position)+Vector2.ONE*.5
	if drone.phase=="working" and drone.job=="clear":
		var cell:=Vector2i(drone.target)
		var offsets: Array=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]
		offsets.sort_custom(func(a,b):return Vector2(cell+a).distance_squared_to(Vector2(drone.home))<Vector2(cell+b).distance_squared_to(Vector2(drone.home)))
		for offset in offsets:
			if not Field.blocks(game.wrecks,cell+offset): return Vector2(cell)+Vector2.ONE*.5+Vector2(offset)*.52
	return position

static func sources(game) -> Array:
	var result: Array = []
	# Emitters are expressed in cells, independent of zoom and camera scroll.
	if game.hardware.power and game.hardware.exterior:
		for room in game.placed_rooms:
			# Same rule as the lamp fixtures: no beam in a blackout, and beams flicker with a low reserve.
			var level: float=preload("res://scripts/station_hardware.gd").exterior_light_level(game,room)
			if level<=0.0: continue
			for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
				if game.occupied.has(room.pos+offset) or Field.blocks(game.wrecks,room.pos+offset): continue
				var mount: Vector2=preload("res://scripts/station_hardware.gd").exterior_mount(Vector2(room.pos)+Vector2.ONE*.5,Vector2(offset),1.0)
				result.append({"position":mount,"direction":Vector2(offset),"radius":2.9,"strength":1.0*level,"kind":"station"})
	for drone in game.drone_fleet.drones.values():
		if drone.phase=="docked": continue
		var position := drone_position(game,drone)
		var heading: Vector2 = Vector2(drone.target)+Vector2.ONE*.5-position
		if not drone.get("route",[]).is_empty(): heading=Vector2(drone.route[0])-Vector2(drone.position)
		if heading.length_squared()<.001: heading=Vector2.DOWN
		result.append({"position":position,"direction":heading.normalized(),"radius":1.7,"strength":.95,"kind":"drone"})
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:
		if not actor.active or actor.dead or actor.movement_medium!="exterior": continue
		var heading := Vector2.ZERO
		if "north" in actor.direction: heading.y=-1
		if "south" in actor.direction: heading.y=1
		if "east" in actor.direction: heading.x=1
		if "west" in actor.direction: heading.x=-1
		result.append({"position":actor.foot/384.0,"direction":heading.normalized(),"radius":1.8,"strength":1.0,"kind":"diver"})
	return result

static func strength_at(source: Dictionary, point: Vector2) -> float:
	var offset: Vector2=point-source.position
	var distance := offset.length()
	if distance>=source.radius: return 0.0
	var cone := smoothstep(.45,.9,offset.normalized().dot(source.direction))
	var local := 1.0-smoothstep(.1,.4,distance)
	return maxf(cone,local)*pow(1.0-distance/source.radius,1.5)*source.strength

func draw(canvas: CanvasItem, game, size: float) -> void:
	var lights := sources(game)
	var visual_time: float=game.get_visual_time_seconds()
	for drone in game.drone_fleet.drones.values():
		if drone.phase=="working" and drone.job=="clear" and game.wrecks.get(Vector2i(drone.target),{}).get("kind","")=="basalt":
			silt_position=drone_position(game,drone)
			silt_time=visual_time
	if Time.get_ticks_msec()-last_survey>250:
		last_survey=Time.get_ticks_msec()
		for light in lights:
			var origin := Vector2i(Vector2(light.position).floor())
			for x in range(maxi(0,origin.x-3),mini(40,origin.x+4)):
				for y in range(maxi(0,origin.y-3),mini(40,origin.y+4)):
					var cell:=Vector2i(x,y)
					var point:=Vector2(cell)+Vector2.ONE*.5
					if strength_at(light,point)>.07 and clear_ray(game.wrecks,light.position,point): game.surveyed_water[cell]=true
	mask.fill(Color.BLACK)
	for cell in game.wrecks:
		if Field.blocks(game.wrecks,cell): mask.set_pixelv(cell,Color(1,0,0,1))
	for cell in game.surveyed_water:
		var color:=mask.get_pixelv(cell);color.g=1;mask.set_pixelv(cell,color)
	mask_texture.update(mask)
	var center: Vector2 = (Vector2(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical)+game.grid_scroll.size*.5)/size
	lights.sort_custom(func(a,b):return a.position.distance_squared_to(center)<b.position.distance_squared_to(center))
	var positions := PackedVector4Array()
	var directions := PackedVector4Array()
	for i in range(MAX_LIGHTS):
		var light: Dictionary=lights[i] if i<lights.size() else {}
		positions.append(Vector4(light.position.x,light.position.y,light.radius,light.strength) if not light.is_empty() else Vector4.ZERO)
		directions.append(Vector4(light.direction.x,light.direction.y,0,0) if not light.is_empty() else Vector4.ZERO)
	material.set_shader_parameter("lights",positions)
	material.set_shader_parameter("directions",directions)
	material.set_shader_parameter("light_count",mini(MAX_LIGHTS,lights.size()))
	var glow: Array=preload("res://scripts/seabed_glow.gd").glow_uniforms(game,center)
	material.set_shader_parameter("glows",glow[0])
	material.set_shader_parameter("glow_colors",glow[1])
	material.set_shader_parameter("glow_count",glow[2])
	material.set_shader_parameter("cell_size",size)
	material.set_shader_parameter("clock",game.get_visual_time_seconds())
	material.set_shader_parameter("motion",0.0 if preload("res://scripts/title_settings.gd").reduced_motion else 1.0)
	material.set_shader_parameter("silt",Vector4(silt_position.x,silt_position.y,clampf(1.0-(visual_time-silt_time)/6.0,0,1),0))
	canvas.draw_rect(Rect2(Vector2.ZERO,Vector2.ONE*size*40),Color.WHITE)
