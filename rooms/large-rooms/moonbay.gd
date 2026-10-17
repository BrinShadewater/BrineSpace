extends RefCounted
const SurfacePacket=preload("res://scripts/room_surface_packet.gd")
static var batch_surface_primitives:=OS.get_name()=="Windows" and not OS.get_cmdline_user_args().has("--reference-moon-surface-packets")
static func new_surface_packet():
	return SurfacePacket.new() if batch_surface_primitives else null
static func _surface_polygon(canvas:CanvasItem,packet,vertices:PackedVector2Array,color:Color):
	if packet!=null:packet.polygon(vertices,PackedColorArray([color]))
	else:canvas.draw_colored_polygon(vertices,color)
static func _surface_circle(canvas:CanvasItem,packet,center:Vector2,radius:float,color:Color):
	if packet!=null:packet.circle(center,radius,color)
	else:canvas.draw_circle(center,radius,color)

const Common = preload("res://rooms/large-rooms/common.gd")
const WallMaterial = preload("res://rooms/whole-room/department_wall_material.gd")
const DoorFinish = preload("res://rooms/doors/door_finish.gd")
const PaintedDoor = preload("res://rooms/doors/painted_door.gd")
const WaterStrokes=preload("res://scripts/water_stroke_triangles.gd")
static var combine_cached_water_strokes:=not OS.get_cmdline_user_args().has("--reference-water-strokes")
static var combine_dynamic_water_strokes:=not OS.get_cmdline_user_args().has("--reference-dynamic-water-strokes")
const WALL_STYLE := {"material":"data_archive", "art":"res://rooms/large-rooms/art/launch_wall_bank.png", "axis":0.0, "shade":0.35}
const BAY_DOOR_WIDTH := 384.0
const CREW_DOOR_WIDTH := 120.0
const DOOR_SECONDS := 0.8
const SUB_BOUNDS := Rect2(-164,-78,328,156)
const SUB_WET_MODULATE := Color(0.78,0.90,0.92,1.0)
const CENTER_BOUNDS := Rect2(12,168,432,432)
const AIRLOCK_BOUNDS := Rect2(60,-120,114,240)
const LOCKER_RECT := Rect2(274,-112,76,88)
const FEATURES := [
	{"path":"res://assets/station-props-v2/sp-airlock-5.png", "rect":Rect2(-57,228,113,79), "fixed_position":true},
	{"path":"res://assets/station-props-v2/sp-construction_drone_bay-2.png", "rect":Rect2(274,24,76,88), "fixed_position":true},
	{"path":"res://assets/station-props-v2/sp-airlock-4.png", "rect":LOCKER_RECT, "fixed_position":true},
]

static func features_for_rotation(rotation: int) -> Array:
	var result: Array = FEATURES.duplicate(true)
	for feature in result:
		var bounds: Rect2 = feature.rect
		bounds.position = bounds.get_center().rotated(float(posmod(rotation,4))*PI*0.5)-bounds.size*0.5
		bounds.position.y = maxf(bounds.position.y,-300.0)
		feature.rect = bounds
	if posmod(rotation,4) in [1,3]:
		result[0].rect.position.x = -342.5 if posmod(rotation,4)==1 else 229.5
	if posmod(rotation,4)==2: result[2].rect.position.x = -286.0
	return result

static func bay_center(room: Dictionary) -> Vector2:
	return Vector2.LEFT.rotated(float(int(room.get("rotation",0)))*PI*0.5)*156.0

static func boarding_point(room: Dictionary) -> Vector2:
	var inward := -bay_center(room).normalized()
	return bay_center(room)+inward*144.0+inward.orthogonal()*112.0

static func airlock_point(room: Dictionary) -> Vector2:
	return airlock_bounds(room).get_center()

static func exit_point(room: Dictionary) -> Vector2:
	return bay_center(room)-bay_center(room).normalized()*366.0

static func water_at(room: Dictionary, local_point: Vector2) -> float:
	if bay_door_amount(room)>0.0 and wet_door_bounds(room).has_point(local_point): return 1.0
	if airlock_bounds(room).has_point(local_point): return visual_state(room).airlock_water
	if Rect2(bay_center(room)-Vector2.ONE*192,Vector2.ONE*384).has_point(local_point): return 1.0
	return 0.0

static func travel_duration(room: Dictionary, mission: Dictionary) -> float:
	if not room.has("pos") or not mission.has("target"): return 3.0
	return 12.0+float(absi(mission.target.x-room.pos.x)+absi(mission.target.y-room.pos.y))*1.2

static func door_amounts(room: Dictionary) -> Vector2:
	var mission: Dictionary = room.get("moonbay_mission",{})
	var phase := str(mission.get("phase","idle"))
	var progress := float(mission.get("progress",0.0))
	var crew := 0.0
	var ocean := 1.0 if mission.get("ocean_open",false) else 0.0
	match phase:
		"approach": crew = clampf(float(mission.get("cycle_clock",1.0))/DOOR_SECONDS,0,1)
		"seal": crew = 1.0-clampf(progress/DOOR_SECONDS,0,1)
		"unload": crew = clampf(progress/DOOR_SECONDS,0,1)
		"launch": ocean = clampf(progress/DOOR_SECONDS,0,1)
		"outbound": ocean = 1.0-clampf(progress/DOOR_SECONDS,0,1)
		"return": ocean = clampf((progress-travel_duration(room,mission)+DOOR_SECONDS*2.0)/DOOR_SECONDS,0,1)
		"disembark": ocean = 1.0-clampf(progress/DOOR_SECONDS,0,1)
	return Vector2(crew,ocean)

static func bay_door_amount(room: Dictionary) -> float:
	var mission: Dictionary = room.get("moonbay_mission",{})
	var phase := str(mission.get("phase","idle"))
	var progress := float(mission.get("progress",0.0))
	if phase in ["boarding","exit_bay"]: return clampf(progress/DOOR_SECONDS,0,1)
	if phase in ["launch","drain"]: return 1.0-clampf(progress/DOOR_SECONDS,0,1)
	return 0.0

static func warning_state(room: Dictionary) -> Dictionary:
	var mission: Dictionary = room.get("moonbay_mission",{})
	var phase := str(mission.get("phase","idle"))
	var gate := door_amounts(room).y
	var progress := float(mission.get("progress",0.0))
	var moving: bool = phase in ["launch","outbound","disembark"] and progress<DOOR_SECONDS
	if phase=="return":
		var begin := travel_duration(room,mission)-DOOR_SECONDS*2.0
		moving=progress>=begin and progress<begin+DOOR_SECONDS
	return {"yellow":phase in ["approach","seal","flood","boarding","disembark","exit_bay","drain","unload"] or (phase=="outbound" and float(mission.get("chamber_water",0))>0),
		"red":moving,"angle":float(mission.get("cycle_clock",mission.get("progress",0.0)))*TAU*0.75}

static func airlock_bounds(room: Dictionary) -> Rect2:
	var inward := -bay_center(room).normalized()
	var center := bay_center(room)+inward*273.0
	var size := Vector2(114,240) if absf(inward.x)>0.5 else Vector2(240,114)
	return Rect2(center-size*0.5,size)

static func airlock_water_bounds(room: Dictionary) -> Rect2:
	var floor := airlock_bounds(room).grow(-24.0)
	var inward := -bay_center(room).normalized()
	# The shared bay wall is outside the lock rectangle; only the other three
	# walls consume its floor. Include the wet-side threshold up to that wall.
	if inward.x>0.5: floor.position.x-=24.0; floor.size.x+=24.0
	elif inward.x< -0.5: floor.size.x+=24.0
	elif inward.y>0.5: floor.position.y-=24.0; floor.size.y+=24.0
	else: floor.size.y+=24.0
	return floor

static func wet_door_bounds(room: Dictionary) -> Rect2:
	var inward := -bay_center(room).normalized()
	var size := Vector2(28,CREW_DOOR_WIDTH) if absf(inward.x)>0.5 else Vector2(CREW_DOOR_WIDTH,28)
	return Rect2(bay_center(room)+inward*204.0-size*0.5,size)

static func observation_windows(room: Dictionary) -> Array[Rect2]:
	var angle := float(posmod(int(room.get("rotation",0)),4))*PI*0.5
	var result: Array[Rect2]=[]
	for y in [-204.0,204.0]:
		for x in [-104.0,104.0]:
			var size := Vector2(128,24) if posmod(int(room.get("rotation",0)),2)==0 else Vector2(24,128)
			result.append(Rect2(bay_center(room)+Vector2(x,y).rotated(angle)-size*0.5,size))
	for y in [-138.0,138.0]:
		var size := Vector2(24,96) if posmod(int(room.get("rotation",0)),2)==0 else Vector2(96,24)
		result.append(Rect2(bay_center(room)+Vector2(204,y).rotated(angle)-size*0.5,size))
	return result

static func locker_point(room: Dictionary) -> Vector2:
	var rotation := posmod(int(room.get("rotation",0)),4)
	var locker := locker_bounds(room)
	if rotation == 1: return Vector2(locker.position.x-26,locker.position.y+24)
	return Vector2(locker.position.x-26,locker.end.y-12)

static func locker_bounds(room: Dictionary) -> Rect2:
	var props: Array=room.get("studio_props",[]) if room.has("studio_props") else load("res://rooms/large-rooms/studio_view.gd").live_props("moonbay",int(room.get("rotation",0)))
	for prop in props:
		if str(prop.id)=="library/sp-airlock-4" and not prop.get("layout_hidden",false): return prop.rect
	return Rect2()

static func fixed_bounds() -> Array[Rect2]:
	return fixed_bounds_for_rotation(0)

static func fixed_bounds_for_rotation(rotation: int) -> Array[Rect2]:
	var result := Common.fixed_bounds_for_rotation(CENTER_BOUNDS,[],rotation)
	var airlock := airlock_bounds({"rotation":rotation})
	result.append(Rect2(airlock.position+Vector2.ONE*384.0,airlock.size))
	return result

static func visual_state(room: Dictionary) -> Dictionary:
	var mission: Dictionary = room.get("moonbay_mission",{})
	var phase: String = str(mission.get("phase","idle"))
	return {"phase":phase,"sub_present":phase not in ["launch","outbound","work","return"],
		"chamber_water":1.0,"airlock_water":clampf(float(mission.get("chamber_water",0.0)),0.0,1.0),
		"station_open":bool(mission.get("station_open",true)),
		"ocean_open":bool(mission.get("ocean_open",false)),"damage":int(mission.get("damage",0))}

static func ocean_side(room: Dictionary) -> String:
	return Common.rotated_side(str(room.get("ocean_side","west")),int(room.get("rotation",0)))

static func enclosure_walls(room: Dictionary) -> Array[Rect2]:
	var result: Array[Rect2] = []
	var ocean := ocean_side(room)
	var inward := -bay_center(room).normalized()
	var dry_side := Common.rotated_side("east",int(room.get("rotation",0)))
	for side in ["north","east","south","west"]:
		# The ocean wall belongs to the hull, so there is only one launch gate.
		if side == ocean: continue
		var split: bool = side == dry_side
		var vertical: bool = side in ["east","west"]
		var axis := -216.0 if side in ["north","west"] else 192.0
		if split:
			for start in [-216.0,60.0]:
				result.append(Rect2(axis,start,24,156) if vertical else Rect2(start,axis,156,24))
		else:
			result.append(Rect2(axis,-216,24,432) if vertical else Rect2(-216,axis,432,24))
	for i in range(result.size()): result[i].position += bay_center(room)
	# One crew airlock: a shared bay door and a single door into the dry work area.
	var lock := airlock_bounds(room)
	var vertical := absf(inward.x)>0.5
	if vertical:
		for y in [lock.position.y,lock.end.y-24]: result.append(Rect2(lock.position.x,y,114,24))
		var x := lock.end.x-24 if inward.x>0 else lock.position.x
		result.append(Rect2(x,lock.position.y,24,60)); result.append(Rect2(x,60,24,60))
	else:
		for x in [lock.position.x,lock.end.x-24]: result.append(Rect2(x,lock.position.y,24,114))
		var y := lock.end.y-24 if inward.y>0 else lock.position.y
		result.append(Rect2(lock.position.x,y,60,24)); result.append(Rect2(60,y,60,24))
	return result

static func navigation_bounds_for_rotation(room: Dictionary) -> Array[Rect2]:
	var result := enclosure_walls(room)
	var state := visual_state(room)
	if state.sub_present:
		var sub_size := Vector2(256,108) if posmod(int(room.get("rotation",0)),2)==0 else Vector2(108,256)
		result.append(Rect2(bay_center(room)-sub_size*0.5,sub_size))
	var inward := -bay_center(room).normalized()
	var mission: Dictionary = room.get("moonbay_mission",{})
	for distance in [204.0,318.0]:
		var allowed: bool = mission.get("phase","idle") in ["boarding","exit_bay"] if distance==204.0 else bool(state.station_open)
		if allowed: continue
		var center: Vector2 = bay_center(room)+inward*distance
		var size := Vector2(24,CREW_DOOR_WIDTH) if absf(inward.x)>0.5 else Vector2(CREW_DOOR_WIDTH,24)
		result.append(Rect2(center-size*0.5,size))
	# Ocean apertures are never dry crew exits.
	match ocean_side(room):
		"west": result.append(Rect2(-384,-192,28,384))
		"east": result.append(Rect2(356,-192,28,384))
		"south": result.append(Rect2(-192,356,384,28))
		"north": result.append(Rect2(-192,-384,384,28))
	for i in range(result.size()): result[i].position += Vector2.ONE*384.0
	return result

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	draw_base_prefix(canvas,room,rect)
	draw_live_water(canvas,room,rect)
	# Retained internal walls follow water/sub drawing; their live gates follow
	# the walls. Other callers retain the complete immediate drawing path.
	if canvas.has_method("owns_moonbay_tail") and canvas.owns_moonbay_tail():
		Common.finish(canvas)
		return
	draw_static_walls(canvas,room,rect)
	draw_live_gates(canvas,room,rect)
	Common.finish(canvas)

# Contiguous commands before the animated water. External port doors, peripheral
# flood tint and the helmet shelf belong to this prefix and invalidate it.
static func draw_base_prefix(canvas:CanvasItem,room:Dictionary,rect:Rect2)->void:
	var shell := room.duplicate()
	shell["custom_ocean_gate"] = true
	Common.begin(canvas,shell,rect,Color("#263842"),WALL_STYLE,"res://assets/department-floors-v2/robotics-service.png",0.40)
	Common.south_transform(canvas,rect)
	var shelf := locker_point(room)+Vector2(20,-22)
	if locker_bounds(room).has_area():
		canvas.draw_rect(Rect2(shelf+Vector2(-10,0),Vector2(40,4)),Color("#536767"))
		if room.get("shelf_helmet_visible",true):
			Common.sprite(canvas,"res://character/crew-underwater-v1/equipment/east/overlay.png",Rect2(shelf+Vector2(-9,-20),Vector2(18,22)))
	# The sub bay is permanently wet; only the grated crew airlock cycles water.
	var center := bay_center(room)
	Common.floor_tiles(canvas,"res://assets/department-floors-v2/robotics-service.png",Rect2(center-Vector2.ONE*192,Vector2.ONE*384),96.0,Color(0.62,0.68,0.70))
	var lock_floor := airlock_bounds(room)
	canvas.draw_rect(lock_floor,Color("#152129"))
	Common.floor_tiles(canvas,Common.GRATING_ART,lock_floor,96.0,Color("#829394"))
	Common.finish(canvas)

# Threshold grating stays between the original water layers. Each retained child
# establishes its own draw transform; canvas command transforms are not inherited.
static func draw_live_water(canvas:CanvasItem,room:Dictionary,rect:Rect2)->void:
	Common.south_transform(canvas,rect)
	var state:=visual_state(room)
	var center:=bay_center(room)
	var water_clock := float(room.get("moonbay_mission",{}).get("cycle_clock",0.0))
	if preload("res://scripts/title_settings.gd").reduced_motion: water_clock=0.0
	_draw_water(canvas,airlock_water_bounds(room),state.airlock_water,water_clock,state.phase in ["flood","disembark","drain","outbound"])
	_draw_water(canvas,Rect2(center-Vector2.ONE*192,Vector2.ONE*384),1.0,water_clock,false)
	# Flood the shared threshold underneath the retracting leaves. The wall and
	# closed door mask it; opening reveals one continuous wet passage.
	var wet_threshold := wet_door_bounds(room)
	Common.floor_tiles(canvas,Common.GRATING_ART,wet_threshold,96.0,Color("#829394"))
	_draw_water(canvas,wet_threshold,1.0,water_clock,false)
	if state.sub_present:
		# The source nose points west; follow the ocean wall through every rotation.
		var angle := float(int(room.get("rotation",0)))*PI*0.5
		Common.south_transform(canvas,rect,angle)
		Common.sprite(canvas,"res://rooms/large-rooms/art/mini_sub.png",Rect2(center.rotated(-angle)+SUB_BOUNDS.position,SUB_BOUNDS.size),Color("#b0a8a5") if state.damage>0 else Color.WHITE,float(state.chamber_water),angle,SUB_WET_MODULATE)
		Common.south_transform(canvas,rect)
	Common.finish(canvas)

static func draw_static_walls(canvas:CanvasItem,room:Dictionary,rect:Rect2)->void:
	Common.south_transform(canvas,rect)
	var center:Vector2=bay_center(room)
	var lock_floor:Rect2=airlock_bounds(room)
	for wall in enclosure_walls(room): WallMaterial.wall(canvas,wall,wall.size.x>wall.size.y,"engineering")
	for x in [-216.0,192.0]:
		for y in [-216.0,192.0]: _draw_wall_corner(canvas,Rect2(center+Vector2(x,y),Vector2(24,24)),Vector2(1 if x<0 else -1,1 if y<0 else -1))
	for x in [lock_floor.position.x,lock_floor.end.x-24.0]:
		for y in [lock_floor.position.y,lock_floor.end.y-24.0]:
			_draw_wall_corner(canvas,Rect2(x,y,24,24),Vector2(1 if x==lock_floor.position.x else -1,1 if y==lock_floor.position.y else -1))
	for x in [-384.0,356.0]:
		for y in [-393.0 if room.get("raised_walls",true) else -384.0,356.0]:
			_draw_wall_corner(canvas,Rect2(x,y,28,28),Vector2(1 if x<0 else -1,1 if y<0 else -1))
	for window in observation_windows(room): _draw_observation_window(canvas,window)
	Common.finish(canvas)

static func draw_live_gates(canvas:CanvasItem,room:Dictionary,rect:Rect2)->void:
	Common.south_transform(canvas,rect)
	var center:Vector2=bay_center(room)
	var inward := -center.normalized()
	var doors := door_amounts(room)
	_draw_bay_door(canvas,center+inward*204.0,absf(inward.x)>0.5,bay_door_amount(room),CREW_DOOR_WIDTH,28.0)
	_draw_bay_door(canvas,center+inward*318.0,absf(inward.x)>0.5,doors.x,CREW_DOOR_WIDTH,28.0)
	var gate := -inward*370.0
	var vertical := absf(inward.x)>0.5
	var depth := 76.0 if ocean_side(room)=="north" and room.get("raised_walls",true) else 32.0
	var aperture := Vector2(depth,BAY_DOOR_WIDTH) if vertical else Vector2(BAY_DOOR_WIDTH,depth)
	canvas.draw_rect(Rect2(gate-aperture*0.5,aperture),Color("#07161e"))
	_draw_bay_door(canvas,gate,vertical,doors.y,BAY_DOOR_WIDTH,depth)
	var warning := warning_state(room)
	var mounts := beacon_mounts(room)
	_draw_beacon(canvas,mounts.yellow,Color("#d3a438"),warning.yellow,warning.angle)
	_draw_beacon(canvas,mounts.red,Color("#bc4c45"),warning.red,warning.angle)
	Common.finish(canvas)

# Full, stationary water only: reuse CPU geometry, preserving native commands and order.
# The canvas owns at most 16 entries; no textures or scene references are retained.
class WaterCommands extends RefCounted:
	var commands:Array=[]
	var combine:=true
	var topology:Dictionary={}
	func draw_rect(rect:Rect2,color:Color):commands.append(["rect",rect,color])
	func draw_polygon(points:PackedVector2Array,colors:PackedColorArray):commands.append(["polygon",points,colors])
	func draw_polyline(points:PackedVector2Array,color:Color,width:float,aa:bool):
		var geometry:Dictionary=commands.back()[1] if not commands.is_empty() and commands.back()[0]=="strokes" else WaterStrokes.empty(topology,true)
		if combine and aa and WaterStrokes.add(geometry,points,color,width):
			if commands.is_empty() or commands.back()[0]!="strokes":commands.append(["strokes",geometry])
		else:commands.append(["polyline",points,color,width,aa])
static func _draw_water(canvas: CanvasItem, floor: Rect2, level: float, clock: float, pumping: bool) -> void:
	if level<=0.001:return
	if clock!=0.0 or level!=1.0:
		if combine_dynamic_water_strokes:_draw_water_dynamic(canvas,floor,level,clock,pumping)
		else:_draw_water_uncached(canvas,floor,level,clock,pumping)
		return
	var cache:Dictionary=canvas.get_meta("moonbay_water_commands",{})
	var key:Array=[floor,level,clock,pumping]
	if not cache.has(key):
		var capture:=WaterCommands.new()
		capture.combine=combine_cached_water_strokes
		var started:=Time.get_ticks_usec()
		_record_water(capture,floor,level,clock,pumping)
		canvas.set_meta("water_stroke_build_usec",int(canvas.get_meta("water_stroke_build_usec",0))+Time.get_ticks_usec()-started)
		if cache.size()>=16:cache.erase(cache.keys()[0])
		cache[key]=capture.commands;canvas.set_meta("moonbay_water_commands",cache)
	for command in cache[key]:
		match command[0]:
			"strokes":WaterStrokes.draw(canvas,command[1])
			"rect":canvas.draw_rect(command[1],command[2])
			"polygon":canvas.draw_polygon(command[1],command[2])
			"polyline":canvas.draw_polyline(command[1],command[2],command[3],command[4])
# Canvas-owned bounded topology reuses only immutable triangle indices.
# Animated positions/colors are rebuilt, preserving native stroke and blend order.
static func _draw_water_dynamic(canvas:CanvasItem,floor:Rect2,level:float,clock:float,pumping:bool)->void:
	var capture:=WaterCommands.new()
	capture.topology=canvas.get_meta("water_stroke_topology",{})
	canvas.set_meta("water_stroke_topology",capture.topology)
	_record_water(capture,floor,level,clock,pumping)
	for command in capture.commands:
		match command[0]:
			"strokes":WaterStrokes.draw(canvas,command[1])
			"rect":canvas.draw_rect(command[1],command[2])
			"polygon":canvas.draw_polygon(command[1],command[2])
			"polyline":canvas.draw_polyline(command[1],command[2],command[3],command[4])
static func _record_water(canvas, floor: Rect2, level: float, clock: float, pumping: bool) -> void:

	if level<=0.001: return
	var height := floor.size.y*clampf(level,0,1)
	var wet := Rect2(floor.position+Vector2(0,floor.size.y-height),Vector2(floor.size.x,height))
	# Depth colour stays translucent so the real deck/grating remains readable.
	var vertices := PackedVector2Array([wet.position,Vector2(wet.end.x,wet.position.y),wet.end,Vector2(wet.position.x,wet.end.y)])
	canvas.draw_polygon(vertices,PackedColorArray([Color(0.11,0.35,0.42,0.45),Color(0.11,0.35,0.42,0.45),Color(0.06,0.24,0.31,0.34),Color(0.06,0.24,0.31,0.34)]))
	# Soft contact shadows along the walls, without an unfilled floor margin.
	for i in range(4):
		var inset := float(i)*2.0
		var alpha := 0.055*(1.0-float(i)/4.0)
		var stripe_height := maxf(0.0,wet.size.y-inset*2.0)
		if stripe_height<=0: break
		canvas.draw_rect(Rect2(wet.position+Vector2(inset,inset),Vector2(2,stripe_height)),Color(0.02,0.09,0.12,alpha))
		canvas.draw_rect(Rect2(Vector2(wet.end.x-inset-2,wet.position.y+inset),Vector2(2,stripe_height)),Color(0.02,0.09,0.12,alpha))
	# Sparse moving caustic ribbons: short uneven curves rather than a bright grid.
	if wet.size.y>8.0:
		var row:=0
		var y:=wet.position.y+8.0
		while y<wet.end.y-4.0:
			var x:=wet.position.x+6.0
			var column:=0
			while x<wet.end.x-6.0:
				var seed:=float(row*13+column*7)
				var length:=minf(18.0+7.0*sin(seed*1.7),wet.end.x-x-3.0)
				var ribbon:=PackedVector2Array()
				var cos_offset:=cos(seed+clock*0.4)*2.0
				for point_index in range(7):
					var along:=float(point_index)/6.0
					var yy:=y+sin(along*PI+seed+clock*0.65)*3.0+cos_offset
					ribbon.append(Vector2(x+along*length,clampf(yy,wet.position.y+2,wet.end.y-2)))
				canvas.draw_polyline(ribbon,Color(0.55,0.76,0.73,0.07+0.025*sin(seed+clock)),1.1,true)
				x+=36.0+5.0*cos(seed)
				column+=1
			y+=27.0+3.0*sin(float(row)*2.0)
			row+=1
	# Pump turbulence is contained by the actual wetted footprint.
	if pumping and wet.size.y>12.0:
		var drain:=Vector2(wet.get_center().x,wet.end.y-10.0)
		for ring in range(3):
			var radius:=5.0+fposmod(clock*9.0+float(ring)*12.0,36.0)
			var arc:=PackedVector2Array()
			for step in range(25):
				var point:=drain+Vector2.RIGHT.rotated(PI+float(step)*PI/24.0)*Vector2(radius,radius*0.45)
				if wet.has_point(point): arc.append(point)
				elif arc.size()>1: canvas.draw_polyline(arc,Color(0.53,0.74,0.73,0.13),1,true); arc=PackedVector2Array()
			if arc.size()>1: canvas.draw_polyline(arc,Color(0.53,0.74,0.73,0.13),1,true)
	if level<0.999:
		var surface:=PackedVector2Array()
		for i in range(25):
			var xx:=lerpf(wet.position.x,wet.end.x,float(i)/24.0)
			surface.append(Vector2(xx,wet.position.y+sin(float(i)*0.7+clock*1.5)*minf(1.5,height*0.1)))
		canvas.draw_polyline(surface,Color(0.53,0.73,0.73,0.38),1.3,true)

static func _draw_water_uncached(canvas: CanvasItem, floor: Rect2, level: float, clock: float, pumping: bool) -> void:
	if level<=0.001: return
	var height := floor.size.y*clampf(level,0,1)
	var wet := Rect2(floor.position+Vector2(0,floor.size.y-height),Vector2(floor.size.x,height))
	# Depth colour stays translucent so the real deck/grating remains readable.
	var vertices := PackedVector2Array([wet.position,Vector2(wet.end.x,wet.position.y),wet.end,Vector2(wet.position.x,wet.end.y)])
	canvas.draw_polygon(vertices,PackedColorArray([Color(0.11,0.35,0.42,0.45),Color(0.11,0.35,0.42,0.45),Color(0.06,0.24,0.31,0.34),Color(0.06,0.24,0.31,0.34)]))
	# Soft contact shadows along the walls, without an unfilled floor margin.
	for i in range(4):
		var inset := float(i)*2.0
		var alpha := 0.055*(1.0-float(i)/4.0)
		var stripe_height := maxf(0.0,wet.size.y-inset*2.0)
		if stripe_height<=0: break
		canvas.draw_rect(Rect2(wet.position+Vector2(inset,inset),Vector2(2,stripe_height)),Color(0.02,0.09,0.12,alpha))
		canvas.draw_rect(Rect2(Vector2(wet.end.x-inset-2,wet.position.y+inset),Vector2(2,stripe_height)),Color(0.02,0.09,0.12,alpha))
	# Sparse moving caustic ribbons: short uneven curves rather than a bright grid.
	if wet.size.y>8.0:
		var row:=0
		var y:=wet.position.y+8.0
		while y<wet.end.y-4.0:
			var x:=wet.position.x+6.0
			var column:=0
			while x<wet.end.x-6.0:
				var seed:=float(row*13+column*7)
				var length:=minf(18.0+7.0*sin(seed*1.7),wet.end.x-x-3.0)
				var ribbon:=PackedVector2Array()
				var cos_offset:=cos(seed+clock*0.4)*2.0
				for point_index in range(7):
					var along:=float(point_index)/6.0
					var yy:=y+sin(along*PI+seed+clock*0.65)*3.0+cos_offset
					ribbon.append(Vector2(x+along*length,clampf(yy,wet.position.y+2,wet.end.y-2)))
				canvas.draw_polyline(ribbon,Color(0.55,0.76,0.73,0.07+0.025*sin(seed+clock)),1.1,true)
				x+=36.0+5.0*cos(seed)
				column+=1
			y+=27.0+3.0*sin(float(row)*2.0)
			row+=1
	# Pump turbulence is contained by the actual wetted footprint.
	if pumping and wet.size.y>12.0:
		var drain:=Vector2(wet.get_center().x,wet.end.y-10.0)
		for ring in range(3):
			var radius:=5.0+fposmod(clock*9.0+float(ring)*12.0,36.0)
			var arc:=PackedVector2Array()
			for step in range(25):
				var point:=drain+Vector2.RIGHT.rotated(PI+float(step)*PI/24.0)*Vector2(radius,radius*0.45)
				if wet.has_point(point): arc.append(point)
				elif arc.size()>1: canvas.draw_polyline(arc,Color(0.53,0.74,0.73,0.13),1,true); arc=PackedVector2Array()
			if arc.size()>1: canvas.draw_polyline(arc,Color(0.53,0.74,0.73,0.13),1,true)
	if level<0.999:
		var surface:=PackedVector2Array()
		for i in range(25):
			var xx:=lerpf(wet.position.x,wet.end.x,float(i)/24.0)
			surface.append(Vector2(xx,wet.position.y+sin(float(i)*0.7+clock*1.5)*minf(1.5,height*0.1)))
		canvas.draw_polyline(surface,Color(0.53,0.73,0.73,0.38),1.3,true)

static func beacon_mounts(room: Dictionary) -> Dictionary:
	var inward := -bay_center(room).normalized()
	# Center the yellow fitting on the airlock wall and red on the solid ocean
	# jamb, clear of its moving leaves. North's face is taller in raised mode.
	var red := -inward*370.0+inward.orthogonal()*288.0
	if ocean_side(room)=="north" and room.get("raised_walls",true): red.y=-350.0
	return {"yellow":airlock_point(room)+inward.orthogonal()*108.0,"red":red}

static func _draw_wall_corner(canvas: CanvasItem, bounds: Rect2, inward: Vector2) -> void:
	# Miter the actual wall skins together at their existing texel scale.
	var top := bounds.position-Vector2(0,3)
	var origin := top+Vector2(bounds.size.x if inward.x<0 else 0.0,bounds.size.y if inward.y<0 else 0.0)
	canvas.draw_rect(Rect2(top+Vector2(0,4),bounds.size),Color("#22292c"))
	var texture := WallMaterial.texture("engineering")
	var packet=new_surface_packet()
	var inner := origin+bounds.size*inward
	for horizontal in [true,false]:
		var end := origin+(Vector2(bounds.size.x,0) if horizontal else Vector2(0,bounds.size.y))*inward
		var points := PackedVector2Array([origin,end,inner])
		var source: Rect2 = WallMaterial.MATERIALS.engineering["horizontal" if horizontal else "vertical"]
		if horizontal: source.size.x*=bounds.size.x/48.0
		else: source.size.y*=bounds.size.y/48.0
		var uv := PackedVector2Array()
		for point in points: uv.append((source.position+(point-top)/bounds.size*source.size)/Vector2(texture.get_size()))
		if packet!=null:packet.polygon(points,PackedColorArray([Color.WHITE]),uv)
		else:canvas.draw_polygon(points,PackedColorArray([Color.WHITE]),uv,texture)
	if packet!=null:packet.draw(canvas,texture)

static func _draw_bay_door(canvas: CanvasItem, center: Vector2, vertical: bool, amount: float, width: float, depth := 32.0) -> void:
	var half := width*0.5
	var skin = PaintedDoor.for_variant("data_archive")
	for upper in [true,false]:
		var length := half*(1.0-clampf(amount,0,1))
		var at := -half if upper else half-length
		var source := Rect2(213 if upper else 1091,280,865,162)
		if PaintedDoor.catalog.styles[skin.family].has("low_y"): source.position.y=PaintedDoor.catalog.styles[skin.family].low_y
		if length<=0.001: continue
		source.size.x *= length/half
		# Clip rigid leaves translating into wall pockets, retaining their moving tips.
		if upper: source.position.x += 865.0-source.size.x
		var dest := Rect2(center+Vector2(-depth*0.5,at),Vector2(depth,length)) if vertical else Rect2(center+Vector2(at,-depth*0.5),Vector2(length,depth))
		DoorFinish.region(canvas,skin.texture("low"),dest,source,Color.WHITE,vertical)
		_draw_interlock(canvas,center,vertical,amount,half,depth,upper)
	for sign_value in [-1.0,1.0]:
		var at := center+(Vector2(-16,sign_value*half-6) if vertical else Vector2(sign_value*half-6,-16))
		WallMaterial.cap(canvas,Rect2(at,Vector2(32,12) if vertical else Vector2(12,32)),"engineering")

static func _draw_interlock(canvas: CanvasItem, center: Vector2, vertical: bool, amount: float, half: float, depth: float, upper: bool) -> void:
	var tip := (-1.0 if upper else 1.0)*half*clampf(amount,0,1)
	var points := PackedVector2Array()
	var inset := -10.0 if upper else 10.0
	points.append(Vector2(tip+inset,-depth*0.5))
	for band in range(4):
		var tooth := 4.0 if band%2==0 else -4.0
		points.append(Vector2(tip+tooth,-depth*0.5+band*depth*0.25))
		points.append(Vector2(tip+tooth,-depth*0.5+(band+1)*depth*0.25))
	points.append(Vector2(tip+inset,depth*0.5))
	for i in range(points.size()):
		points[i]=center+(Vector2(points[i].y,points[i].x) if vertical else points[i])
	canvas.draw_colored_polygon(points,Color("#607074") if upper else Color("#49585c"))
	points.append(points[0])
	canvas.draw_polyline(points,Color("#18262c"),1.5,true)

static func _draw_beacon(canvas: CanvasItem, point: Vector2, color: Color, active: bool, angle: float) -> void:
	var lens := point-Vector2(0,4)
	var direction := Vector2.RIGHT.rotated(angle if active else 0.0)*Vector2(1,0.65)
	var beam=new_surface_packet() if active else null
	if active:
		_surface_polygon(canvas,beam,PackedVector2Array([lens,lens+Vector2.RIGHT.rotated(angle-0.25)*56,lens+Vector2.RIGHT.rotated(angle+0.25)*56]),Color(color,0.16))
		_surface_polygon(canvas,beam,_beacon_oval(lens,Vector2(25,17)),Color(color,0.06))
	if beam!=null:beam.draw(canvas)
	# Wall backplate, short bracket and cast cylindrical base; fixed as the
	# reflector turns inside the coloured glass, rather than rotating the fitting.
	canvas.draw_rect(Rect2(point-Vector2(11,10),Vector2(22,21)),Color("#1c292e"))
	canvas.draw_rect(Rect2(point-Vector2(9,8),Vector2(18,17)),Color("#556368"))
	var bolts=new_surface_packet()
	for offset in [Vector2(-7,-6),Vector2(7,-6),Vector2(-7,7),Vector2(7,7)]:
		_surface_circle(canvas,bolts,point+offset,1.1,Color("#26343a"))
	if bolts!=null:bolts.draw(canvas)
	canvas.draw_rect(Rect2(point+Vector2(-4,0),Vector2(8,8)),Color("#2e3c41"))
	canvas.draw_colored_polygon(_beacon_oval(point+Vector2(0,5),Vector2(10,4)),Color("#1a272d"))
	canvas.draw_rect(Rect2(point+Vector2(-9,0),Vector2(18,5)),Color("#425257"))
	var glass_packet=new_surface_packet()
	_surface_polygon(canvas,glass_packet,_beacon_oval(point,Vector2(9,4)),Color("#778185"))
	var glass := color*Color(0.52,0.52,0.52,1) if not active else color*Color(0.80,0.80,0.80,1)
	_surface_polygon(canvas,glass_packet,_beacon_oval(lens,Vector2(7,8)),glass)
	var reflector := PackedVector2Array([lens-direction*5,lens+direction.orthogonal()*3,lens+direction*5,lens-direction.orthogonal()*3])
	_surface_polygon(canvas,glass_packet,reflector,Color("#eadba3") if active else Color("#777e75"))
	_surface_circle(canvas,glass_packet,lens,1.5,Color("#39474a"))
	if glass_packet!=null:glass_packet.draw(canvas)
	var rim := _beacon_oval(lens,Vector2(7,8))
	rim.append(rim[0])
	canvas.draw_polyline(rim,Color(color,0.65),1.2,true)
	canvas.draw_line(lens+Vector2(-4,-5),lens+Vector2(-5,0),Color(0.84,0.90,0.86,0.4),1.0,true)
	var tail=new_surface_packet() if active else null
	_surface_polygon(canvas,tail,_beacon_oval(point+Vector2(0,1),Vector2(8,3)),Color(0.16,0.22,0.24,0.72))
	if active: _surface_circle(canvas,tail,lens+direction*4,2,Color("#fff0bd"))
	if tail!=null:tail.draw(canvas)

static func _beacon_oval(center: Vector2, radius: Vector2) -> PackedVector2Array:
	var points := PackedVector2Array()
	for i in range(24): points.append(center+Vector2.RIGHT.rotated(float(i)*TAU/24.0)*radius)
	return points

static func _draw_observation_window(canvas: CanvasItem, bounds: Rect2) -> void:
	# Sealed observation glazing inset into the retained low engineering wall.
	var frame := Rect2(bounds.position-Vector2(0,3),bounds.size)
	canvas.draw_rect(frame.grow(-1),Color("#26353b"))
	canvas.draw_rect(frame.grow(-2),Color("#6b787b"))
	var glass := frame.grow(-5)
	canvas.draw_rect(glass.grow(1),Color("#101e25"))
	var corners:=PackedVector2Array([glass.position,Vector2(glass.end.x,glass.position.y),glass.end,Vector2(glass.position.x,glass.end.y)])
	canvas.draw_polygon(corners,PackedColorArray([Color("#28525b"),Color("#21434e"),Color("#122d38"),Color("#193d47")]))
	var vertical := bounds.size.y>bounds.size.x
	var length := glass.size.y if vertical else glass.size.x
	var center := glass.get_center()
	# Two pressure panes share a slim structural mullion and quiet glass streaks.
	var mullion := Vector2(glass.size.x,3) if vertical else Vector2(3,glass.size.y)
	canvas.draw_rect(Rect2(center-mullion*0.5,mullion),Color("#485e64"))
	for side in [-1.0,1.0]:
		var along: float = side*length*0.28
		var a := Vector2(-3,along-7) if vertical else Vector2(along-7,-3)
		var b := Vector2(3,along+7) if vertical else Vector2(along+7,3)
		canvas.draw_line(center+a,center+b,Color(0.60,0.77,0.78,0.20),1.2,true)
	var bolts=new_surface_packet()
	for x in [frame.position.x+3,frame.end.x-3]:
		for y in [frame.position.y+3,frame.end.y-3]: _surface_circle(canvas,bolts,Vector2(x,y),0.9,Color("#23343a"))
	if bolts!=null:bolts.draw(canvas)
