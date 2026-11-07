extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
var checks:=0
var failures:=0
func same(a:Texture2D,b:Texture2D,label:String):
	checks+=1
	if a.get_image().get_data()!=b.get_image().get_data():failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	var activity=preload("res://scripts/crew_room_activity.gd")
	for source in ["library/sp-crew_lounge-4","library/sp-crew_lounge-4#copy"]:
		var corner:Dictionary={"id":source,"rect":Rect2(-40,-70,75,75)}
		var room:Dictionary={"activity_room":"crew_lounge","bunk_actor":"marsh","props":[corner],"blockers":[]}
		checks+=1
		if not activity.stations(room).is_empty():failures+=1;push_error("Marsh must skip corner armchair and copies")
		for actor_id in ["bill","veld","branforth"]:
			room.bunk_actor=actor_id
			checks+=1
			if not activity.stations(room).is_empty():failures+=1;push_error("Crew must skip angled corner armchair and copies")
	var sofa:Dictionary={"activity_room":"crew_lounge","bunk_actor":"marsh","props":[{"id":"library/sp-crew_lounge-3","rect":Rect2(-77,-70,154,140)}],"blockers":[]}
	checks+=1
	if activity.stations(sofa).is_empty():failures+=1;push_error("Marsh retains straight lounge bench")
	var p=Player.new();var path="res://character/marsh-v2/catalog.json"
	for rel in JSON.parse_string(FileAccess.get_file_as_string(path)).body:p.load_manifest(path.get_base_dir().path_join(str(rel)),true)
	for direction in ["east","west","north","south"]:
		var idle:Texture2D=p.frames["idle-"+direction][0]
		for join in [["sit-down",0],["sit-rise",-1],["lie-down",0],["get-up",-1]]:same(p.frames[str(join[0])+"-"+direction][join[1]],idle,"current standing rest join "+direction+str(join))
		same(p.frames["sit-down-"+direction][-1],p.frames["sit-idle-"+direction][0],"seated landing")
		same(p.frames["sit-rise-"+direction][0],p.frames["sit-idle-"+direction][0],"seated rise entry")
		same(p.frames["lie-down-"+direction][-1],p.frames["sleep-"+direction][0],"sleep landing")
		same(p.frames["get-up-"+direction][0],p.frames["sleep-"+direction][0],"sleep rise entry")
		for i in range(4):
			same(p.frames["sit-down-"+direction][i],p.frames["sit-rise-"+direction][3-i],"reversible seated pose "+direction)
			same(p.frames["lie-down-"+direction][i],p.frames["get-up-"+direction][3-i],"reversible generic rest pose "+direction)
	print("MARSH REST JOINS: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
