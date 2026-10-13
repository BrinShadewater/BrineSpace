extends SceneTree
var checks := 0
var failures := 0
func _init() -> void: call_deferred("run")
func check(value: bool, message: String) -> void:
	checks += 1
	if not value:
		failures += 1
		push_error(message)
func run() -> void:
	var activity = load("res://scripts/crew_room_activity.gd")
	var methods: Array = activity.get_script_method_list().map(func(method): return method.name)
	if not methods.has("at_stations"):
		print("ACTIVITY STATION REUSE FAIL: scoped resolver missing")
		quit(1)
		return
	for room in ["galley", "observation_room", "crew_hab", "life_support"]:
		var station := {"point":Vector2.ZERO,"room":room,"tag":"first"}
		var other := {"point":Vector2.ZERO,"room":room,"tag":"second"}
		var canonical: Array = [station, other]
		var sorted: Array = canonical.duplicate()
		sorted.reverse()
		var limit := 5.0 if room in ["galley", "observation_room"] else 36.0
		for distance in [0.0, limit-0.01, limit, limit+0.01]:
			var found: Dictionary = activity.at_stations(canonical,Vector2(distance,0))
			check(found == (station if distance <= limit else {}), "Retain first canonical contact and inclusive threshold")
		check(sorted[0] == other and canonical[0] == station, "Sort reversal must not reorder contact resolution")
	var desk := {"id":"library/tileset-srb2-35","rect":Rect2(-150,20,101.2,100.1)}
	var data := {"activity_room":"life_support","props":[desk]}
	var old: Array = activity.stations(data)
	for move in [Vector2.ZERO, Vector2(20,-30)]:
		desk.rect.position += move
		var fresh: Array = activity.stations(data)
		for x in range(-160,161,20):
			for y in range(-160,161,20):
				var point := Vector2(x,y)
				check(activity.at_stations(fresh,point) == activity.at(data,point), "Scoped resolver equals fresh geometry lookup")
		check(activity.at_stations(fresh,fresh[0].point) == fresh[0], "Moved furniture has fresh contact")
	check(old[0].point != activity.stations(data)[0].point, "Previous decision does not retain moved contact")
	print("ACTIVITY STATION REUSE: %d checks, %d failures" % [checks,failures])
	quit(0 if failures == 0 else 1)
