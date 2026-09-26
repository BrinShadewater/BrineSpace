extends SceneTree
const Activity=preload("res://scripts/crew_room_activity.gd")
func _init():call_deferred("run")
func run():
	var failures=0
	for q in range(4):
		var rect=Rect2(-174,-180,93.1,85.5)
		var data={"activity_room":"cold_store","props":[{"id":"library/tileset-as-244","rect":rect}],"blockers":[rect.grow(10)],"layout":[{"rotation":q}]}
		var stations=Activity.stations(data)
		if stations.size()!=1 or stations[0].get("prop","")!="library/tileset-as-244" or stations[0].facing!="north" or stations[0].point.distance_to(Vector2(-127.45,-78.5))>32:
			failures+=1;push_error("Cold Store inspection detached from freezer q"+str(q))
	# A blocked freezer must not be represented by an unrelated clear-floor target.
	var blocked={"activity_room":"cold_store","props":[{"id":"library/tileset-as-244","rect":Rect2(-174,-180,93.1,85.5)}],"blockers":[Rect2(-190,-190,150,200)],"layout":[{"rotation":0}]}
	if not Activity.stations(blocked).is_empty():failures+=1;push_error("Blocked freezer became a distant inspection point")
	print("COLD STORE STATIONS: four rotations and blocked-front rejection; %d failures"%failures)
	quit(0 if failures==0 else 1)
