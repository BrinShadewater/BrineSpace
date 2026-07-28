extends RefCounted
class_name OrbitManager

const POIS := [
	{
		"name": "Asteroid Field",
		"timer": 6,
		"work_required": 3,
		"work_type": "mining",
		"reward": {"metal": 8},
		"expire_effect": {"metal": 2},
		"complete_message": "Mining drones finish an asteroid sweep.",
		"expire_message": "Mining drones skim the edge of an asteroid field."
	},
	{
		"name": "Derelict Freighter",
		"timer": 6,
		"work_required": 3,
		"work_type": "salvage",
		"reward": {"metal": 4, "data": 5},
		"expire_effect": {"metal": 1, "data": 2},
		"complete_message": "Salvage drones strip the freighter before orbital drift.",
		"expire_message": "Salvage telemetry pings from a dead freighter."
	},
	{
		"name": "Mineral Cloud",
		"timer": 7,
		"work_required": 4,
		"work_type": "mining",
		"reward": {"rare_minerals": 3},
		"expire_effect": {"rare_minerals": 1},
		"complete_message": "Mining drones bottle dense mineral vapor.",
		"expire_message": "Rare minerals condense along the station wake."
	},
	{
		"name": "Frozen Escape Pod",
		"timer": 8,
		"work_required": 3,
		"work_type": "life_support",
		"reward": {},
		"expire_effect": {},
		"complete_message": "The escape pod docks cleanly under life-support protocol.",
		"expire_message": "A frozen escape pod drifts beyond docking range."
	},
	{
		"name": "Alien Wreckage",
		"timer": 8,
		"work_required": 5,
		"work_type": "salvage",
		"reward": {"data": 8, "rare_minerals": 2},
		"expire_effect": {"data": 2},
		"expire_corruption": 1,
		"complete_corruption": 1,
		"complete_message": "Salvage drones recover alien data from the wreckage.",
		"expire_message": "Alien wreckage answers with impossible signal geometry."
	},
	{
		"name": "Solar Flare",
		"timer": 4,
		"work_required": 0,
		"work_type": "environment",
		"reward": {},
		"expire_effect": {"power": 6},
		"expire_damage": 2,
		"expire_message": "A solar flare floods the station skin with unstable Power."
	}
]

var current_poi := {}
var timer := 0
var rng := RandomNumberGenerator.new()

func _init() -> void:
	rng.randomize()
	_roll_poi()

func advance(cycle: int, capacities := {}) -> Dictionary:
	var work_type := str(current_poi.get("work_type", "environment"))
	var work_required := int(current_poi.get("work_required", 0))
	if work_required > 0:
		current_poi["progress"] = int(current_poi.get("progress", 0)) + int(capacities.get(work_type, 0))
		if int(current_poi["progress"]) >= work_required:
			var completed_event := current_poi.duplicate(true)
			completed_event["triggered"] = true
			completed_event["completed"] = true
			completed_event["cycle"] = cycle
			completed_event["effect"] = completed_event.get("reward", {})
			completed_event["message"] = completed_event.get("complete_message", "%s completed." % completed_event["name"])
			if completed_event.has("complete_corruption"):
				completed_event["corruption"] = completed_event["complete_corruption"]
			_roll_poi()
			completed_event["next_poi"] = current_poi
			completed_event["next_timer"] = timer
			return completed_event
	timer -= 1
	if timer > 0:
		return {"triggered": false, "poi": current_poi, "timer": timer}
	var event := current_poi.duplicate(true)
	event["triggered"] = true
	event["completed"] = false
	event["cycle"] = cycle
	event["effect"] = event.get("expire_effect", {})
	event["message"] = event.get("expire_message", "An orbital event passes over BRINE.")
	if event.has("expire_damage"):
		event["damage"] = event["expire_damage"]
	if event.has("expire_corruption"):
		event["corruption"] = event["expire_corruption"]
	_roll_poi()
	event["next_poi"] = current_poi
	event["next_timer"] = timer
	return event

func get_panel_text() -> String:
	if current_poi.is_empty():
		return "Orbit: scanning..."
	var work_required := int(current_poi.get("work_required", 0))
	var progress := int(current_poi.get("progress", 0))
	var work_text := "Passive event" if work_required <= 0 else "Progress: %d/%d %s" % [progress, work_required, current_poi.get("work_type", "work")]
	return "POI: %s\nETA: %d cycle%s\n%s" % [current_poi["name"], timer, "" if timer == 1 else "s", work_text]

func get_current_poi_name() -> String:
	return str(current_poi.get("name", "Scanning"))

func get_current_poi_progress() -> float:
	var work_required := int(current_poi.get("work_required", 0))
	if work_required <= 0:
		return 1.0
	return clamp(float(current_poi.get("progress", 0)) / float(work_required), 0.0, 1.0)

func _roll_poi() -> void:
	current_poi = POIS[rng.randi_range(0, POIS.size() - 1)].duplicate(true)
	current_poi["progress"] = 0
	timer = int(current_poi["timer"])
