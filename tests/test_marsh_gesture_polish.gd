extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
var checks:=0
var failures:=0
func _init():call_deferred("run")
func run():
	var p=Player.new();var path="res://character/marsh-v2/catalog.json"
	for rel in JSON.parse_string(FileAccess.get_file_as_string(path)).body:p.load_manifest(path.get_base_dir().path_join(str(rel)),true)
	for direction in ["east","west","north","south"]:
		for slot in [0,1,6,7]:
			checks+=1
			if p.frames["crew-chat-"+direction][slot].get_image().get_data()!=p.frames["idle-"+direction][0].get_image().get_data():failures+=1;push_error("Current conversation idle mismatch "+direction+str(slot))
		for pair in [["injury-ground",0,"idle",0],["injury-ground",5,"injury-rise",0],["injury-rise",5,"idle",0]]:
			checks+=1
			if p.frames[str(pair[0])+"-"+direction][pair[1]].get_image().get_data()!=p.frames[str(pair[2])+"-"+direction][pair[3]].get_image().get_data():failures+=1;push_error("Current injury boundary mismatch "+direction+str(pair))
	print("MARSH GESTURE JOINS: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
