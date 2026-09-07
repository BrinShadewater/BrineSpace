extends "res://scripts/bill_npc.gd"
## Engineering interests use the shared collision-aware crew controller.

func _init() -> void:
	decision_rng = RandomNumberGenerator.new()
	decision_rng.randomize()
	spawn_offset = Vector2(-48, 32)
	needs = {"hunger": 20.0, "fatigue": 35.0, "curiosity": 25.0, "maintenance": 80.0}
	service_preferences["maintenance"] = ["maintenance_bay", "reactor", "battery_array", "ore_refinery", "life_support"]

func choose_goal(main) -> void:
	super.choose_goal(main)
	if goal == "maintenance": activity = "looking for equipment to service"

func arrive() -> void:
	super.arrive()
	if goal == "maintenance":
		activity = "servicing equipment"
	elif goal == "curiosity":
		activity = "checking diagnostic readings"
		state = "interact"
		direction = "east"
		timer = 1.02
