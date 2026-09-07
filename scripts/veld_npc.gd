extends "res://scripts/bill_npc.gd"
## Same safe station navigation as Bill, with independent science interests.

func _init() -> void:
	decision_rng = RandomNumberGenerator.new()
	decision_rng.randomize()
	spawn_offset = Vector2(48, 32)
	needs = {"hunger": 12.0, "fatigue": 28.0, "curiosity": 45.0, "maintenance": 72.0}
	service_preferences["maintenance"] = ["research_lab", "bio_lab", "xeno_lab", "anomaly_lab", "data_archive", "mycelium_nursery", "hydroponics_bay"]

func choose_goal(main) -> void:
	super.choose_goal(main)
	if goal == "maintenance": activity = "looking for samples to examine"
	elif activity == "stretching his legs": activity = "stretching her legs"

func arrive() -> void:
	super.arrive()
	if goal == "maintenance":
		activity = "examining a sample"
	elif goal == "curiosity":
		activity = "taking scanner readings"
		state = "interact"
		direction = "east"
		timer = 1.02
