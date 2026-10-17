extends SceneTree
var checks:=0
var failures:=0
func check(ok:bool,label:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init()->void:call_deferred("run")
func run()->void:
	var uid="res://character/krusher-turn-face-polish-v1/test_chairs.gd.uid"
	if not FileAccess.file_exists(uid):
		var f=FileAccess.open(uid,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	var activity=preload("res://scripts/crew_room_activity.gd")
	for actor in ["bill","veld","branforth","marsh"]:
		for source in ["library/sp-crew_lounge-4","library/sp-crew_lounge-4#copy"]:
			var prop={"id":source,"rect":Rect2(-40,-70,75,75)}
			var room={"activity_room":"crew_lounge","bunk_actor":actor,"props":[prop],"blockers":[]}
			check(activity.stations(room).is_empty(),actor+" excludes angled chair and copies")
			prop={"id":"copy-seat","variant_source":source,"behavior_role":"lounge_seat","rect":Rect2(-40,-70,75,75)}
			room.props=[prop]
			check(activity.stations(room).is_empty(),actor+" excludes variant source")
		var sofa={"activity_room":"crew_lounge","bunk_actor":actor,"props":[{"id":"library/sp-crew_lounge-3","rect":Rect2(-77,-70,154,140)}],"blockers":[]}
		check(not activity.stations(sofa).is_empty(),actor+" retains ordinary straight seating")
	var file=FileAccess.open("res://character/krusher-turn-face-polish-v1/chair-validation.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures},"\t"))
	print("KRUSHER_CHAIRS checks=%d failures=%d"%[checks,failures]);quit(1 if failures else 0)
