extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")

static func fixed_bounds() -> Array[Rect2]:
	return [Rect2(151, 267, 466, 234)]

static func visual_state(room: Dictionary) -> Dictionary:
	var mission: Dictionary = room.get("moonbay_mission",{})
	var phase: String = str(mission.get("phase","idle"))
	return {"phase":phase,"sub_present":phase not in ["launch","outbound","work","return"],
		"chamber_water":clampf(float(mission.get("chamber_water",0.0)),0.0,1.0),
		"station_open":bool(mission.get("station_open",true)),
		"ocean_open":bool(mission.get("ocean_open",false)),
		"damage":int(mission.get("damage",0))}

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var cyan := Color("#46d3e6")
	var state := visual_state(room)
	Common.begin(canvas, room, rect, Color("#263842"), cyan)
	# Floor rail points west to the sealed launch chamber; the hangar stays dry.
	for y in [-89, 89]:
		canvas.draw_rect(Rect2(-360, y - 7, 720, 14), Color("#597683"))
		for x in range(-340, 341, 68): canvas.draw_rect(Rect2(x - 4, y - 12, 8, 24), Color("#a2b7b9"))
	Common.panel(canvas, Rect2(-233, -117, 466, 234), Color("#1b303b"), Color("#537887"))
	if state.sub_present:
		# Broad pressure hull, observation glass and twin compact thrusters.
		canvas.draw_colored_polygon(PackedVector2Array([Vector2(-210,0),Vector2(-130,-73),Vector2(137,-73),Vector2(215,-35),Vector2(225,0),Vector2(215,35),Vector2(137,73),Vector2(-130,73)]), Color("#8d999f") if state.damage>0 else Color("#b4c5c6"))
		canvas.draw_colored_polygon(PackedVector2Array([Vector2(-173,0),Vector2(-114,-54),Vector2(120,-54),Vector2(180,-22),Vector2(185,0),Vector2(180,22),Vector2(120,54),Vector2(-114,54)]), Color("#4e707d"))
		canvas.draw_rect(Rect2(-80, -48, 105, 96), Color("#123a4e"))
		canvas.draw_rect(Rect2(-68, -37, 81, 74), Color("#2d7384"))
		for y in [-48, 48]:
			canvas.draw_rect(Rect2(130, y - 16, 94, 32), Color("#899ca2"))
			canvas.draw_circle(Vector2(218, y), 16, Color("#223c49"))
	else:
		for x in [-178,-70,70,178]: canvas.draw_rect(Rect2(x-12,-86,24,172),Color("#547481"))
		for x in [-142,142]: canvas.draw_circle(Vector2(x,0),23,Color("#0c2533"))
	if state.chamber_water>0.0:
		var water_height: float = 214.0*state.chamber_water
		canvas.draw_rect(Rect2(-226,108-water_height,452,water_height),Color(0.09,0.54,0.72,0.48))
		canvas.draw_line(Vector2(-226,108-water_height),Vector2(226,108-water_height),Color("#72daf0"),4)
	# Independent interlocks make the dry station entrance and ocean gate readable.
	canvas.draw_rect(Rect2(238,-77,20,154),Color("#132a32") if state.station_open else Color("#c09258"))
	canvas.draw_rect(Rect2(-258,-77,20,154),Color("#1c809b") if state.ocean_open else Color("#c09258"))
	for x in [-247,247]: canvas.draw_circle(Vector2(x,96),7,Color("#52d8df") if (x>0 and state.station_open) or (x<0 and state.ocean_open) else Color("#d7a25c"))
	canvas.draw_line(Vector2(-203, 0), Vector2(-340, 0), cyan.darkened(0.4), 6)
	for x in [-280, -150, 150, 280]: canvas.draw_circle(Vector2(x, 172), 9, cyan.darkened(0.3))
	Common.finish(canvas)
