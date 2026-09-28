extends RefCounted
## Studio-only previews of special animations and hazards (owner, Sept 28): airlock
## cycles, drone launch/return, the survey probe launch, fire and flooding. The state
## lives here and is handed to the room view each frame, the way grid_canvas does for
## the live game, so nothing reaches layouts, saves or the station.
const Airlock = preload("res://scripts/airlock_cycle.gd")
const DRONE_BAYS := {"mining_drone_bay":"mining","construction_drone_bay":"construction","salvage_drone_bay":"salvage"}
# Only machinery heat ignites a room, and those rooms also throw sparks (room_fire.gd).
const FIRE_ROOMS: Dictionary = preload("res://scripts/room_fire.gd").MACHINERY
const DOCK_SECONDS := 1.2 # drone_dock.pose() spans launching/docking over 1.2 s
const PROBE_SECONDS := 32.0 # survey_probe.pose(): launch, trip, scan and dock
const FLOOD_SECONDS := 6.0
const FLOOD_LEVEL := 0.85
const FIRE_SECONDS := 3.0

class StubGrid extends RefCounted:
	const DOOR_OPEN_FRAMES := 10
	var door_wet_history: Dictionary = {}
	func _door_frame_for_pair(_game, _a: Vector2i, _b: Vector2i) -> int: return 0

## The few game members the fire and flood drawings read. A Studio room stands alone,
## so it has no neighbours and every door reads as shut and dry.
class StubGame extends RefCounted:
	var time := 0.0
	var hardware: Dictionary = {"power": true}
	var occupied: Dictionary = {}
	var paused := false
	var grid_view := StubGrid.new()
	func get_visual_time_seconds() -> float: return time

var room_id := ""
var clock := 0.0
var airlock: Dictionary = {}
var drone: Dictionary = {}
var drone_return_phase := ""
var probe_clock := -1.0
var fire := 0.0
var flood := 0.0
var stub := StubGame.new()

func actions() -> Array:
	var list: Array = []
	if room_id == "airlock": list += [["Cycle out", "cycle_out"], ["Cycle in", "cycle_in"]]
	if DRONE_BAYS.has(room_id):
		list += [["Launch drone", "launch"], ["Return drone", "return"]]
		if room_id != "construction_drone_bay": list.append(["Return with cargo", "return_cargo"])
	if room_id == "survey_probe_bay": list.append(["Launch probe", "probe"])
	if FIRE_ROOMS.has(room_id): list.append(["Fire", "fire"])
	list += [["Flood", "flood"], ["Clear", "clear"]]
	return list

func start(action: String) -> void:
	match action:
		"cycle_out": airlock = Airlock.begin("sealing_inner")
		"cycle_in": airlock = Airlock.begin("sealing_outer")
		"launch": drone = {"phase": "launching", "elapsed": 0.0, "job": "preview", "battery": 100.0, "cargo": {}}
		"return", "return_cargo":
			drone = {"phase": "docking", "elapsed": 0.0, "job": "preview", "battery": 100.0, "cargo": {"metal": 2} if action == "return_cargo" else {}}
		"probe": probe_clock = 0.0
		"fire": fire = 0.3
		"flood": flood = maxf(flood, 0.01)
		"clear": clear()

func clear() -> void:
	airlock = {}
	drone = {}
	probe_clock = -1.0
	fire = 0.0
	flood = 0.0

func active() -> bool:
	return not airlock.is_empty() or not drone.is_empty() or probe_clock >= 0.0 or fire > 0.0 or flood > 0.0

func advance(delta: float) -> void:
	clock += delta
	stub.time = clock
	if not airlock.is_empty(): airlock = _step_airlock(airlock, delta)
	if not drone.is_empty():
		drone.elapsed = float(drone.elapsed) + delta
		if float(drone.elapsed) >= DOCK_SECONDS:
			# Launched drones stay out until Return; returned drones settle in the dock.
			drone = {} if drone.phase == "docking" else {"phase": "outbound", "elapsed": 0.0, "job": "preview", "battery": 100.0, "cargo": {}}
	if probe_clock >= 0.0:
		probe_clock += delta
		if probe_clock >= PROBE_SECONDS: probe_clock = -1.0
	if fire > 0.0: fire = minf(0.9, fire + delta * 0.6 / FIRE_SECONDS)
	if flood > 0.0: flood = minf(FLOOD_LEVEL, flood + delta * FLOOD_LEVEL / FLOOD_SECONDS)

# airlock_cycle.advance() needs a running game with a serviced airlock; the Studio steps
# the same phase table directly, holding at the open outer hatch or the dry chamber.
func _step_airlock(state: Dictionary, delta: float) -> Dictionary:
	var s := state.duplicate()
	var remaining := maxf(0.0, delta)
	if float(s.get("warning_delay", 0)) > 0:
		var warning_step := minf(remaining, float(s.warning_delay))
		s.warning_delay -= warning_step
		remaining -= warning_step
	while Airlock.DURATIONS.has(s.phase) and remaining > 0:
		var step := minf(remaining, float(Airlock.DURATIONS[s.phase]) - float(s.elapsed))
		s.elapsed += step
		remaining -= step
		if s.elapsed >= float(Airlock.DURATIONS[s.phase]): s = {"phase": Airlock.NEXT[s.phase], "elapsed": 0.0}
	return {} if s.phase == "dry" else s

func hazard_room() -> Dictionary:
	return {"id": room_id, "pos": Vector2i.ZERO, "fire": fire, "fire_heat": 0.0, "suspended": false,
		"water_level": flood, "hull_crack": 0.6 if flood > 0.0 else 0.0}

## Hand the preview state to the room view before it renders.
func apply(view) -> void:
	if view == null: return
	if "cycle_pose" in view:
		var room := {"airlock_cycle": airlock} if not airlock.is_empty() else {}
		view.cycle_pose = Airlock.pose(room)
		view.caution_active = not airlock.is_empty() and Airlock.warning_active(room)
	if "drone_visual" in view and DRONE_BAYS.has(room_id):
		var visual := drone.duplicate()
		if not visual.is_empty(): visual["clock"] = clock
		view.drone_visual = visual
		if "drone_deployed" in view: view.drone_deployed = str(visual.get("phase", "docked")) not in ["docked", "launching", "docking"]
		if "hatch_open" in view:
			view.hatch_open = clampf(float(visual.get("elapsed", 0)) / 0.35, 0, 1) if visual.get("phase", "") == "launching" else (1.0 - clampf((float(visual.get("elapsed", 0)) - 0.85) / 0.35, 0, 1) if visual.get("phase", "") == "docking" else 0.0)
	if "survey_clock" in view and room_id == "survey_probe_bay":
		view.survey_clock = maxf(0.0, probe_clock)
		view.survey_status = "blue" if probe_clock >= 0.0 else "yellow"
	if "flood_water" in view:
		view.flood_water = flood
		view.flood_clock = clock

## Fire, sparks and the flood front, drawn by the live game's own functions around a room
## at cell (0,0). The Studio canvas centres the room on origin().
func draw_hazards(canvas: CanvasItem, origin: Vector2, factor: float) -> void:
	if fire <= 0.0 and flood <= 0.0: return
	canvas.draw_set_transform(origin - Vector2.ONE * 192.0 * factor, 0, Vector2.ONE * factor)
	var rooms := [hazard_room()]
	if flood > 0.0: preload("res://scripts/room_flooding.gd").draw(canvas, stub, rooms, 384.0)
	if fire > 0.0: preload("res://scripts/room_fire.gd").draw(canvas, stub, rooms, 384.0)
	canvas.draw_set_transform(origin, 0, Vector2.ONE * factor)
