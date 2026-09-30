extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WallMaterial = preload("res://rooms/whole-room/department_wall_material.gd")
const DoorFinish = preload("res://rooms/doors/door_finish.gd")
const PaintedDoor = preload("res://rooms/doors/painted_door.gd")
const WALL_STYLE := {"material":"data_archive", "art":"res://rooms/large-rooms/art/launch_wall_bank.png", "axis":0.0, "shade":0.35}
const BAY_DOOR_WIDTH := 192.0
const SUB_BOUNDS := Rect2(-78,-164,156,328)
const CENTER_BOUNDS := Rect2(168,168,432,432)
const AIRLOCK_BOUNDS := Rect2(-120,-306,240,114)
const LOCKER_RECT := Rect2(274,-112,76,88)
const FEATURES := [
	{"path":"res://assets/station-props-v2/sp-airlock-5.png", "rect":Rect2(-57,228,113,79), "fixed_position":true},
	{"path":"res://assets/station-props-v2/sp-construction_drone_bay-2.png", "rect":Rect2(274,24,76,88), "fixed_position":true},
	{"path":"res://assets/station-props-v2/sp-airlock-4.png", "rect":LOCKER_RECT, "fixed_position":true},
]

static func features_for_rotation(rotation: int) -> Array:
	var result: Array = FEATURES.duplicate(true)
	if posmod(rotation,4) == 2:
		result[1].rect.position.x = -result[1].rect.end.x
		result[2].rect = Rect2(274,-190,76,66)
	elif posmod(rotation,4) == 3:
		result[0].rect = Rect2(-312,-45,90,90)
	return result

static func locker_point(room: Dictionary) -> Vector2:
	var locker: Rect2 = features_for_rotation(int(room.get("rotation",0)))[2].rect
	return Vector2(locker.position.x-26,locker.end.y-12)

static func fixed_bounds() -> Array[Rect2]:
	return fixed_bounds_for_rotation(0)

static func fixed_bounds_for_rotation(rotation: int) -> Array[Rect2]:
	var result := Common.fixed_bounds_for_rotation(CENTER_BOUNDS,features_for_rotation(rotation),rotation)
	result.append(Rect2(AIRLOCK_BOUNDS.position+Vector2.ONE*384.0,AIRLOCK_BOUNDS.size))
	return result

static func visual_state(room: Dictionary) -> Dictionary:
	var mission: Dictionary = room.get("moonbay_mission",{})
	var phase: String = str(mission.get("phase","idle"))
	return {"phase":phase,"sub_present":phase not in ["launch","outbound","work","return"],
		"chamber_water":clampf(float(mission.get("chamber_water",0.0)),0.0,1.0),
		"station_open":bool(mission.get("station_open",true)),
		"ocean_open":bool(mission.get("ocean_open",false)),"damage":int(mission.get("damage",0))}

static func ocean_side(room: Dictionary) -> String:
	return Common.rotated_side(str(room.get("ocean_side","west")),int(room.get("rotation",0)))

static func enclosure_walls(room: Dictionary) -> Array[Rect2]:
	var result: Array[Rect2] = []
	var ocean := ocean_side(room)
	for side in ["north","east","south","west"]:
		var split: bool = side == "north" or side == ocean
		var vertical: bool = side in ["east","west"]
		var axis := -216.0 if side in ["north","west"] else 192.0
		if split:
			for start in [-216.0,96.0]:
				result.append(Rect2(axis,start,24,120) if vertical else Rect2(start,axis,120,24))
		else:
			result.append(Rect2(axis,-216,24,432) if vertical else Rect2(-216,axis,432,24))
	# Rear crew airlock shares the chamber's north pressure door.
	if ocean != "north": result.append(Rect2(-120,-306,240,22))
	else:
		result.append(Rect2(-120,-306,24,22)); result.append(Rect2(96,-306,24,22))
	result.append(Rect2(-120,-306,24,114))
	result.append(Rect2(96,-306,24,14)); result.append(Rect2(96,-220,24,28))
	return result

static func navigation_bounds_for_rotation(room: Dictionary) -> Array[Rect2]:
	var result := enclosure_walls(room)
	var state := visual_state(room)
	if state.sub_present: result.append(Rect2(-54,-128,108,256))
	if not state.station_open:
		result.append(Rect2(-96,-216,192,24))
		result.append(Rect2(96,-292,24,72))
	# Ocean apertures are never dry crew exits.
	match ocean_side(room):
		"west": result.append(Rect2(-216,-96,24,192))
		"east": result.append(Rect2(192,-96,24,192))
		"south": result.append(Rect2(-96,192,192,24))
		"north": result.append(Rect2(-96,-306,192,22))
	for i in range(result.size()): result[i].position += Vector2.ONE*384.0
	var features := Common.fixed_bounds_for_rotation(CENTER_BOUNDS,features_for_rotation(int(room.get("rotation",0))),int(room.get("rotation",0)))
	for i in range(1,features.size()): result.append(features[i])
	return result

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var state := visual_state(room)
	Common.begin(canvas,room,rect,Color("#263842"),WALL_STYLE,"res://assets/department-floors-v2/robotics-service.png",0.40)
	Common.draw_features(canvas,features_for_rotation(int(room.get("rotation",0))),room,rect)
	Common.south_transform(canvas,rect)
	var shelf := locker_point(room)+Vector2(20,-22)
	canvas.draw_rect(Rect2(shelf+Vector2(-10,0),Vector2(40,4)),Color("#536767"))
	if room.get("shelf_helmet_visible",true):
		Common.sprite(canvas,"res://character/crew-underwater-v1/equipment/east/overlay.png",Rect2(shelf+Vector2(-9,-20),Vector2(18,22)))
	# Both chambers have real material floors; the rear airlock remains dry.
	Common.floor_tiles(canvas,"res://assets/department-floors-v2/robotics-service.png",Rect2(-192,-192,384,384),96.0,Color(0.62,0.68,0.70))
	canvas.draw_rect(Rect2(-96,-284,192,80),Color("#152129"))
	Common.floor_tiles(canvas,Common.GRATING_ART,Rect2(-96,-284,192,80),96.0,Color("#829394"))
	if state.sub_present:
		# The source nose points west; -90 degrees puts it south in every room rotation.
		Common.south_transform(canvas,rect,-PI*0.5)
		Common.sprite(canvas,"res://rooms/large-rooms/art/mini_sub.png",Rect2(-164,-78,328,156),Color("#b0a8a5") if state.damage>0 else Color.WHITE)
		Common.south_transform(canvas,rect)
	if state.chamber_water>0.0:
		var height: float = 384.0*state.chamber_water
		canvas.draw_rect(Rect2(-192,192-height,384,height),Color(0.16,0.42,0.50,0.40))
	for wall in enclosure_walls(room): WallMaterial.wall(canvas,wall,wall.size.x>wall.size.y,"engineering")
	for x in [-216.0,192.0]:
		for y in [-216.0,192.0]: WallMaterial.cap(canvas,Rect2(x,y,24,24),"engineering")
	# Rear bay gate + dry-side airlock door, with no center bar across either opening.
	_draw_bay_door(canvas,Vector2(0,-204),false,bool(state.station_open),BAY_DOOR_WIDTH)
	Common._draw_station_port(canvas,Vector2(108,-256),"east",Color("#263842"),false,"robotics",1.0 if state.station_open else 0.0)
	match ocean_side(room):
		"west": _draw_bay_door(canvas,Vector2(-204,0),true,state.ocean_open,BAY_DOOR_WIDTH)
		"east": _draw_bay_door(canvas,Vector2(204,0),true,state.ocean_open,BAY_DOOR_WIDTH)
		"south": _draw_bay_door(canvas,Vector2(0,204),false,state.ocean_open,BAY_DOOR_WIDTH)
		"north": _draw_bay_door(canvas,Vector2(0,-295),false,state.ocean_open,BAY_DOOR_WIDTH)
	Common.finish(canvas)

static func _draw_bay_door(canvas: CanvasItem, center: Vector2, vertical: bool, open: bool, width: float) -> void:
	var half := width*0.5
	var skin = PaintedDoor.for_variant("data_archive")
	for upper in [true,false]:
		var length := 12.0 if open else half
		var at := -half if upper else half-length
		var source := Rect2(213 if upper else 1091,280,865,162)
		if PaintedDoor.catalog.styles[skin.family].has("low_y"): source.position.y=PaintedDoor.catalog.styles[skin.family].low_y
		if open:
			source.size.x *= length/half
			if not upper: source.position.x += 865.0-source.size.x
		var dest := Rect2(center+Vector2(-16,at),Vector2(32,length)) if vertical else Rect2(center+Vector2(at,-16),Vector2(length,32))
		DoorFinish.region(canvas,skin.texture("low"),dest,source,Color.WHITE,vertical)
	for sign_value in [-1.0,1.0]:
		var at := center+(Vector2(-16,sign_value*half-6) if vertical else Vector2(sign_value*half-6,-16))
		WallMaterial.cap(canvas,Rect2(at,Vector2(32,12) if vertical else Vector2(12,32)),"engineering")
	for x in [-120.0,96.0]: WallMaterial.cap(canvas,Rect2(x,-306,24,24),"engineering")
