extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WallMaterial = preload("res://rooms/whole-room/department_wall_material.gd")
const WALL_STYLE := {"material":"tidal_condenser", "art":"res://rooms/large-rooms/art/tidal_wall_bank.png", "axis":230.0, "shade":0.3}
const CENTER_BOUNDS := Rect2(172,172,424,424)
const TURBINE_ART := "res://rooms/large-rooms/art/tidal_turbine.png"
const FILL_SECONDS := 6.0
const DRAIN_SECONDS := 5.0
const FEATURES := [
	{"path":"res://assets/station-props-v2/sp-tidal_condenser-1.png", "rect":Rect2(-197,-305,92,93)},
	{"path":"res://assets/station-props-v2/sp-tidal_condenser-4.png", "rect":Rect2(100,-295,100,67)},
	{"path":"res://assets/station-props-v2/sp-tidal_condenser-2.png", "rect":Rect2(244,0,68,84)},
	{"path":"res://assets/station-props-v2/sp-tidal_condenser-5.png", "rect":Rect2(-37,214,73,98)},
]

static func fixed_bounds() -> Array[Rect2]:
	return Common.fixed_bounds_for_rotation(CENTER_BOUNDS,FEATURES,0)

static func fixed_bounds_for_rotation(rotation: int) -> Array[Rect2]:
	return Common.fixed_bounds_for_rotation(CENTER_BOUNDS,FEATURES,rotation)

static func chamber_state(room: Dictionary) -> Dictionary:
	if not room.has("tidal_chamber"):
		room.tidal_chamber = {"water":0.0,"rotor_angle":0.0,"spinning":false}
	return room.tidal_chamber

static func tick(game, delta: float) -> void:
	if not game.running or game.paused: return
	for room in game.placed_rooms:
		if room.get("id","") != "tidal_power_plant": continue
		var state := chamber_state(room)
		var prior_water := float(state.water)
		var operating: bool = game.hardware.power and game.powered_room_cells.has(room.pos) and not room.get("suspended",false) and game._ocean_face_problem(room).is_empty()
		state.water = clampf(float(state.water)+maxf(0.0,delta)*(1.0/FILL_SECONDS if operating else -1.0/DRAIN_SECONDS),0.0,1.0)
		state.spinning = operating and float(state.water)>=1.0
		if state.spinning:
			var spin_time := maxf(0.0,delta-(1.0-prior_water)*FILL_SECONDS)
			state.rotor_angle = fposmod(float(state.rotor_angle)+spin_time*0.8,TAU)

static func valid_rooms(rooms: Array) -> bool:
	for room in rooms:
		if not room is Dictionary or room.get("id","") != "tidal_power_plant" or not room.has("tidal_chamber"): continue
		var state: Variant = room.tidal_chamber
		if not state is Dictionary: return false
		for key in ["water","rotor_angle"]:
			if not state.get(key) is float and not state.get(key) is int: return false
			if not is_finite(float(state[key])): return false
		if float(state.water)<0 or float(state.water)>1 or float(state.rotor_angle)<0 or float(state.rotor_angle)>=TAU: return false
		if not state.get("spinning") is bool: return false
		if state.spinning and float(state.water)<1.0: return false
	return true

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	Common.begin(canvas,room,rect,Color("#303841"),WALL_STYLE,"res://assets/department-floors-v1/engineering-tread.png",0.36)
	Common.draw_features(canvas,FEATURES,room,rect)
	# Reuse the painted source's large flanged pipe below a flush grate trench.
	Common.south_transform(canvas,rect,float(int(room.get("rotation",0)))*PI*0.5)
	Common.sprite(canvas,TURBINE_ART,Rect2(-1,-1,2,2),Color(1,1,1,0))
	canvas.draw_rect(Rect2(-38,-366,76,172),Color("#142028"))
	canvas.draw_texture_rect_region(Common.art_textures[TURBINE_ART],Rect2(-30,-366,60,174),Rect2(64,244,108,690),Color("#b1b9bc"))
	Common.floor_tiles(canvas,Common.GRATING_ART,Rect2(-38,-366,76,172),96.0,Color("#829394"))
	Common.south_transform(canvas,rect)
	canvas.draw_rect(Rect2(-192,-192,384,384),Color("#16232b"))
	Common.floor_tiles(canvas,Common.GRATING_ART,Rect2(-192,-192,384,384),96.0,Color("#839395"))
	Common.sprite(canvas,TURBINE_ART,Rect2(-190,-190,380,380))
	var state: Dictionary = room.get("tidal_chamber",{"water":0.0,"rotor_angle":0.0,"spinning":false})
	if state.get("spinning",false): _draw_rotor(canvas,float(state.rotor_angle))
	var water := float(state.get("water",0.0))
	if water>0.0:
		canvas.draw_rect(Rect2(-192,192-384*water,384,384*water),Color(0.12,0.34,0.41,0.32))
		if water<1.0: canvas.draw_line(Vector2(-192,192-384*water),Vector2(192,192-384*water),Color("#648a91"),2)
	# A solid pressure enclosure replaces the old yellow outline.
	for y in [-212.0,192.0]: WallMaterial.wall(canvas,Rect2(-212,y,424,20),true,"engineering")
	for x in [-212.0,192.0]: WallMaterial.wall(canvas,Rect2(x,-212,20,424),false,"engineering")
	for x in [-212.0,192.0]:
		for y in [-212.0,192.0]: WallMaterial.cap(canvas,Rect2(x,y,20,20),"engineering")
	Common.finish(canvas)

static func _draw_rotor(canvas: CanvasItem, angle: float) -> void:
	# Only the circular impeller moves; its painted housing and floor stay fixed.
	var texture: Texture2D = Common.art_textures[TURBINE_ART]
	var center := Vector2(-0.3,-6.3)
	canvas.draw_circle(center,115.2,Color("#192a31"))
	var points := PackedVector2Array()
	var uv := PackedVector2Array()
	for i in range(96):
		var unit := Vector2.from_angle(float(i)*TAU/96.0)
		points.append(center+unit.rotated(angle)*115.2)
		uv.append((Vector2(626,606)+unit*380.0)/Vector2(texture.get_size()))
	canvas.draw_polygon(points,PackedColorArray([Color.WHITE]),uv,texture)
