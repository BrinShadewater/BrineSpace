extends SceneTree
const Activity=preload("res://scripts/crew_room_activity.gd")
var failures=0
func check(ok: bool,message: String):
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	for q in range(4):
		var rect=Rect2(-174,-180,87.4,90.25)
		var data={"activity_room":"observation_room","props":[{"id":"library/tileset-mat-116","rect":rect}],"blockers":[rect.grow(10)],"layout":[{"rotation":q}]}
		var station=Activity.stations(data)[0]
		check(station.get("prop","")=="library/tileset-mat-116" and station.facing=="south","Read at visible sofa with its facing")
		check(not rect.grow(10).has_point(station.point),"Standing approach must clear sofa")
		var watched=Activity.stations(data).filter(func(s):return s.get("mode")=="watch")
		check(watched.size()==1 and not rect.grow(10).has_point(watched[0].point),"Watch survives repeated cached sofa lookup")
		check(is_same(watched[0],data.observation_watch_stations[0]),"Repeated watch lookup reuses its computed station")
		check(not is_same(data.observation_watch_stations,data.reachable_service_stations),"Watch and sofa caches stay separate")
		var actor=preload("res://scripts/bill_npc.gd").new()
		actor.goal_cell=Vector2i.ZERO;actor.geometry={Vector2i.ZERO:data};actor.foot=Vector2.ONE*192+station.point
		var offset: Vector2=station.rest_point-station.point
		actor.stage="observation_sit";actor.timer=0.65
		check(actor.observation_visual_offset().is_zero_approx(),"Sit must start at walking foot")
		actor.timer=0.325
		check(actor.observation_visual_offset().is_equal_approx(offset*0.5),"Sit must interpolate into cushion")
		actor.stage="observation_read"
		check(actor.observation_visual_offset().is_equal_approx(offset),"Reading must remain on cushion")
		actor.stage="observation_rise";actor.timer=0
		check(actor.observation_visual_offset().is_zero_approx(),"Rise must return to walking foot")
	var legacy=Activity.stations({"activity_room":"observation_room","props":[],"layout":[{"rotation":0}]})
	var blocked={"activity_room":"observation_room","props":[],"layout":[{"rotation":3}],"blockers":[Rect2(-16,-96,32,32)]}
	var shifted=Activity.stations(blocked).filter(func(s):return s.get("mode")=="watch")
	check(shifted.size()==1 and not blocked.blockers[0].has_point(shifted[0].point),"Watch relocates when furnishing covers old anchor")
	check(legacy[0].point==Vector2(0,112) and not legacy[0].has("rest_point"),"Legacy fixture remains compatible")
	print("OBSERVATION SOFA: four room rotations and sit/read/rise registration; %d failures"%failures)
	quit(0 if failures==0 else 1)
