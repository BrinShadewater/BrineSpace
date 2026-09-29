extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WallMaterial = preload("res://rooms/whole-room/department_wall_material.gd")
const DoorFinish = preload("res://rooms/doors/door_finish.gd")
const PaintedDoor = preload("res://rooms/doors/painted_door.gd")
const WALL_STYLE := {"material":"data_archive", "art":"res://rooms/large-rooms/art/launch_wall_bank.png", "axis":0.0, "shade":0.35}
const BAY_DOOR_WIDTH := 192.0
const SUB_BOUNDS := Rect2(-210,-80,420,160)
const FEATURES := [
	{"path":"res://assets/station-props-v2/sp-construction_drone_bay-4.png", "rect":Rect2(-58,-300,116,87)},
	{"path":"res://assets/station-props-v2/sp-airlock-5.png", "rect":Rect2(-57,220,113,87)},
	{"path":"res://assets/station-props-v2/sp-construction_drone_bay-2.png", "rect":Rect2(80,205,109,107)},
]

static func fixed_bounds() -> Array[Rect2]:
	var result: Array[Rect2] = [Rect2(151, 267, 466, 234)]
	result.append_array(Common.feature_bounds(FEATURES))
	return result

static func visual_state(room: Dictionary) -> Dictionary:
	var mission: Dictionary = room.get("moonbay_mission",{})
	var phase: String = str(mission.get("phase","idle"))
	return {"phase":phase,"sub_present":phase not in ["launch","outbound","work","return"],
		"chamber_water":clampf(float(mission.get("chamber_water",0.0)),0.0,1.0),
		"station_open":bool(mission.get("station_open",true)),
		"ocean_open":bool(mission.get("ocean_open",false)),
		"damage":int(mission.get("damage",0))}

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var cyan := Color("#78afb9")
	var state := visual_state(room)
	Common.begin(canvas, room, rect, Color("#263842"), cyan, WALL_STYLE)
	Common.draw_features(canvas, FEATURES)
	# Floor rail points west to the sealed launch chamber; the hangar stays dry.
	for y in [-89, 89]:
		canvas.draw_rect(Rect2(-360, y - 7, 720, 14), Color("#597683"))
		for x in range(-340, 341, 68): canvas.draw_rect(Rect2(x - 4, y - 12, 8, 24), Color("#a2b7b9"))
	Common.panel(canvas, Rect2(-233, -117, 466, 234), Color("#1b303b"), Color("#537887"))
	if state.sub_present:
		Common.sprite(canvas, "res://rooms/large-rooms/art/mini_sub.png", SUB_BOUNDS, Color("#b0a8a5") if state.damage>0 else Color.WHITE)
	else:
		for x in [-178,-70,70,178]: canvas.draw_rect(Rect2(x-12,-86,24,172),Color("#547481"))
		for x in [-142,142]: canvas.draw_circle(Vector2(x,0),23,Color("#0c2533"))
	if state.chamber_water>0.0:
		var water_height: float = 214.0*state.chamber_water
		canvas.draw_rect(Rect2(-226,108-water_height,452,water_height),Color(0.16,0.42,0.50,0.42))
		canvas.draw_line(Vector2(-226,108-water_height),Vector2(226,108-water_height),Color("#89bac2"),4)
	# A full pressure enclosure keeps the dry hangar distinct from the floodable launch path.
	_draw_bay_enclosure(canvas, state)
	for x in [-247,247]: canvas.draw_circle(Vector2(x,96),7,Color("#83b9bc") if (x>0 and state.station_open) or (x<0 and state.ocean_open) else Color("#b49a72"))
	canvas.draw_line(Vector2(-203, 0), Vector2(-340, 0), cyan.darkened(0.4), 6)
	for x in [-280, -150, 150, 280]: canvas.draw_circle(Vector2(x, 172), 9, cyan.darkened(0.3))
	Common.finish(canvas)

static func _draw_bay_enclosure(canvas: CanvasItem, state: Dictionary) -> void:
	var top := Rect2(-258,-138,516,24)
	var bottom := Rect2(-258,114,516,24)
	WallMaterial.wall(canvas, top, true, "engineering")
	WallMaterial.wall(canvas, bottom, true, "engineering")
	for x in [-258.0,234.0]:
		for y in [-138.0,96.0]:
			WallMaterial.wall(canvas, Rect2(x,y,24,42), false, "engineering")
	for side in [-1,1]:
		var x: float = -258.0 if side < 0 else 234.0
		var open: bool = bool(state.ocean_open) if side < 0 else bool(state.station_open)
		_draw_bay_door(canvas, x, open)

static func _draw_bay_door(canvas: CanvasItem, x: float, open: bool) -> void:
	var half := BAY_DOOR_WIDTH * 0.5
	canvas.draw_rect(Rect2(x - 4,-half - 4,32,BAY_DOOR_WIDTH + 8),Color("#0b1820"))
	canvas.draw_rect(Rect2(x + 1,-half,22,BAY_DOOR_WIDTH),Color("#344b55"))
	for y in [-half - 10,half - 4]:
		canvas.draw_rect(Rect2(x - 5,y,34,14),Color("#8a989a"))
		canvas.draw_rect(Rect2(x - 2,y + 3,28,5),Color("#b0b9af"))
	for upper in [true,false]:
		var length := 16.0 if open else half
		var y := -half if upper else half - length
		var skin = PaintedDoor.for_variant("data_archive")
		var source := Rect2(213 if upper else 1091,280,865,162)
		if PaintedDoor.catalog.styles[skin.family].has("low_y"):
			source.position.y = PaintedDoor.catalog.styles[skin.family].low_y
		if open:
			source.size.x *= length / half
			if not upper: source.position.x += 865.0 - source.size.x
		DoorFinish.region(canvas,skin.texture("low"),Rect2(x,y,24,length),source,Color.WHITE,true)
		if not open:
			canvas.draw_rect(Rect2(x + 10,y + 8,4,length - 16),Color("#49677a"))
			for rib in range(24,roundi(length),30):
				canvas.draw_rect(Rect2(x + 2,y + float(rib),20,3),Color("#8c9b9d"))
	if not open:
		canvas.draw_rect(Rect2(x - 3,-3,30,6),Color("#b4aaa0"))
