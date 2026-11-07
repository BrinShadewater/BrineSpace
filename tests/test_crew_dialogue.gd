extends SceneTree
const Dialogue=preload("res://scripts/crew_dialogue.gd")
func _init() -> void:
	var ids: Array=["bill","veld","branforth"]
	for room_id in Dialogue.ROOM_LINES:
		var unique: Array=[]
		for id in ids:
			var line: String=Dialogue.room_comment(id,room_id)
			assert(not line.is_empty() and line.length()<230)
			assert(not unique.has(line)); unique.append(line)
	for id in ids:
		assert("checking gauges" in Dialogue.greeting(id,"checking gauges"))
		assert(Dialogue.room_comment(id,"unlisted_room").is_empty(),"Unwritten rooms fall back to their definition")
		var line: String=Dialogue.resource_report(id,"oxygen",7,2.5)
		assert("Oxygen" in line and "7 in reserve" in line and "2.5 used per cycle" in line)
		assert(not Dialogue.resource_report(id,"",0,0).is_empty())
	print("CREW DIALOGUE PASS: 15 distinct room opinions, live activity, resource figures and fallback")
	quit()
