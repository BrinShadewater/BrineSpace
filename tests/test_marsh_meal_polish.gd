extends SceneTree
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	var player=preload("res://scripts/crew_sprite_player.gd").new()
	var path:="res://character/marsh-v2/catalog.json"
	for rel in JSON.parse_string(FileAccess.get_file_as_string(path)).body:player.load_manifest(path.get_base_dir().path_join(str(rel)),true)
	var actor=preload("res://scripts/marsh_npc.gd").new();actor.active=true
	for direction in ["east","south","west","north"]:
		actor.direction=direction
		for kind in ["eat","drink"]:
			var key:String=kind+"-"+direction
			var idle:PackedByteArray=player.frames["idle-"+direction][0].get_image().get_data()
			check(player.frames[key][0].get_image().get_data()==idle,"meal entry matches current idle "+key)
			check(player.frames[key][-1].get_image().get_data()==idle,"meal exit matches current idle "+key)
			actor.stage="life_"+kind
			var duration:float=actor.Life.seconds(actor,actor.stage)
			for sample in range(0,int(duration*120)):
				actor.timer=duration-float(sample)/120
				var data:Dictionary=actor.meal_animation()
				check(data.pose==kind and data.elapsed>=0,"deterministic service presentation")
				var saved:Dictionary=actor.snapshot();var restored=preload("res://scripts/marsh_npc.gd").new()
				restored.stage=actor.stage;restored.timer=float(saved.timer);restored.direction=direction
				check(restored.meal_animation()==data,"saved timer resumes exact meal pose")
			actor.timer=.001
			var final:Dictionary=actor.meal_animation()
			check(player.frame_at_elapsed(key,final.elapsed).get_image().get_data()==idle,"service finishes empty handed "+key)
	actor.movement_medium="water"
	check(actor.meal_animation().is_empty(),"no eating underwater")
	print("MARSH MEALS: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
