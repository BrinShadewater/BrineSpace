extends "res://tests/test_veld_seated_north_continue.gd"
const PROBE_OUT="res://output/veld-seat-approach-probe-v1/"
func _init():
	var path="res://tests/test_veld_seat_approach_probe.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(PROBE_OUT)
	var game=await fresh();var actor=game.veld_npc
	game.selected_rotation=0;game._place_room("crew_lounge",CELL,true);game.powered_room_cells[CELL]=true
	var records=[];var center:Vector2=(Vector2(CELL)+Vector2.ONE*.5)*384
	for rotation in 4:
		game.occupied[CELL].rotation=rotation;await actor.rebuild(game)
		var data:Dictionary=actor.geometry[CELL];var stations:Array=actor.RoomActivity.stations(data);var candidates=[]
		for station in stations:
			var rest:Vector2=station.get("rest_point",station.point)
			for y in [rest.y+20,rest.y+24,rest.y+28,rest.y+32,rest.y+36]:
				var point:Vector2=Vector2(rest.x,y)
				var near:int=actor.nearest_in_room(center+point,CELL,false)
				var near_point:Vector2=actor.graph.get_point_position(near) if near>=0 else Vector2.INF
				candidates.append({"point":point,"rest":rest,"canStand":actor.can_stand(center+point),"approachBlocked":actor.RoomActivity._approach_blocked(data,point),"nearestNode":near_point-center,"nodeJoins":near>=0 and actor.segment_clear(near_point,center+point)})
		var nodes=[]
		for node in actor.room_nodes.get(CELL,[]):
			var point:Vector2=actor.graph.get_point_position(node)-center
			if point.y>=144:nodes.append(point)
		records.append({"rotation":rotation,"stations":stations,"frontCandidates":candidates,"southNodes":nodes,"props":data.props,"blockers":data.blockers})
	var file=FileAccess.open(PROBE_OUT+"approaches.json",FileAccess.WRITE);file.store_string(JSON.stringify(records,"\t"));file.close()
	check(records.size()==4,"Four actual default lounge quarters inspected")
	check(root.get_texture().get_image().save_png(PROBE_OUT+"final.png")==OK,"Fresh probe capture")
	print("VELD SEAT APPROACH PROBE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
