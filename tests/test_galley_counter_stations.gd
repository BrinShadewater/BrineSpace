extends SceneTree
const Activity=preload("res://scripts/crew_room_activity.gd")
var failures=0
func check(ok: bool, message: String):
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	for q in range(4):
		for moved in [false,true]:
			var rect=Rect2(-174,66,70.5,64.5)
			if moved:rect.position+=Vector2(100,-64)
			var prop={"id":"copy/counter" if moved else "library/tileset-mms-58","copy_source":"library/tileset-mms-58","rect":rect}
			var data={"activity_room":"galley","props":[prop],"layout":[{"rotation":q}],"blockers":[rect.grow(10)]}
			var stations=Activity.stations(data)
			check(stations.size()==1,"Counter must offer one adjacent meal location")
			for station in stations:
				check(station.get("prop","")==prop.id,"Meal must identify its actual counter")
				check(not rect.grow(10).has_point(station.point),"Meal location must clear counter collision")
				check(station.point.distance_to(Vector2(rect.get_center().x,rect.end.y+12))<24,"Meal must follow moved counter, not room rotation")
				check(station.facing=="north","Fixed-facing bought counter must retain service facing")
	# A counter against the south edge can be approached from its accessible rear.
	var edge=Rect2(-100,100,70,60)
	var rear=Activity.stations({"activity_room":"galley","props":[{"id":"library/tileset-mms-60","rect":edge}],"blockers":[edge.grow(10)]})
	check(rear.size()==1 and rear[0].facing=="south","South-edge counter needs an adjacent rear approach")
	var legacy=Activity.stations({"activity_room":"galley","props":[],"blockers":[],"layout":[{"rotation":0}]})
	check(legacy.size()==2 and legacy[0].point==Vector2(64,144),"Legacy fixture approaches must remain compatible")
	print("GALLEY COUNTER STATIONS: rotation, movement, copy, collision, rear access and legacy; %d failures"%failures)
	quit(0 if failures==0 else 1)
