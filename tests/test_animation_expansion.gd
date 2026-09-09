extends SceneTree
const Companion=preload("res://scripts/companion_npc.gd")
const Player=preload("res://scripts/crew_sprite_player.gd")
const DIRS=["south","west","north","east"]
class Fixture extends "res://scripts/companion_npc.gd":
	func _init(id="margot"):super(id)
	func topology(_main)->String:return signature
	func can_stand(_point:Vector2)->bool:return true
class Game extends RefCounted:
	var occupied={}
	var running=true
	var paused=false
	func play_station_sound(_key,_point):pass
var failures=0
func _init():call_deferred("run")
func check(ok,message):
	if not ok:failures+=1;push_error(message)
func run():
	var game=Game.new()
	for id in ["margot","river","josh"]:
		var actor=Fixture.new(id);actor.active=true
		for d in DIRS:
			for action in actor.ACTIONS[id]:
				check(actor.poses.frames.has(action+"-"+d) or (action=="pet" and d!="south"),id+" directional coverage "+action+d)
			for action in (["sit","groom","nap","stretch","yawn"] if id=="margot" else ["boot"] if id=="river" else ["powerdown"]):
				actor.direction=d;actor.start_behavior(action);actor.update(game,.35)
				check(actor.direction==d,"Retains authored facing "+id+action+d)
				var state=actor.personality_snapshot();check(Companion.valid_personality(state,id),"Valid new action checkpoint")
				var pixels=actor.texture(0).get_image().get_data()
				game.paused=true;actor.update(game,1);check(actor.personality_snapshot()==state,"Paused action is unchanged")
				game.paused=false;actor.restore_personality(state);check(actor.texture(10).get_image().get_data()==pixels,"Restored action frame unchanged")
				if action=="nap":
					actor.pet();check(actor.wake_direction==d,"Wake retains nap facing")
					check(actor.texture(0).get_image().get_data()==actor.poses.frame_at_elapsed("nap-exit-"+d,0).get_image().get_data(),"Pet wakes through correct directional exit")
				actor.update(game,30);check(actor.behavior.is_empty(),"Action completes "+action)
		if id=="margot":continue
		actor.behavior="";actor.direction="south";actor.state="walk"
		actor.locomotion.advance(actor,"idle","south",.1)
		check(actor.locomotion.key=="move-start-south","Movement enters acceleration clip")
		var slow=actor.locomotion.speed_factor(actor)
		actor.locomotion.advance(actor,"walk","south",.2)
		check(actor.locomotion.speed_factor(actor)>slow,"Acceleration advances with simulation time")
		var motion=actor.personality_snapshot();actor.locomotion.key="";actor.restore_personality(motion)
		check(actor.locomotion.snapshot()==motion.locomotion,"Movement checkpoint restores")
		game.paused=true;actor.update(game,2);check(actor.locomotion.snapshot()==motion.locomotion,"Pause preserves movement phase");game.paused=false
		for d in DIRS:
			for to in DIRS:
				if d==to:continue
				actor.direction=to;actor.locomotion.advance(actor,"walk",d,.1)
				check(actor.locomotion.key=="turn-"+d+"-"+to,"Authored turn selected "+d+to)
		actor.state="idle";actor.locomotion.advance(actor,"walk",actor.direction,.1)
		check(actor.locomotion.key.begins_with("move-stop-"),"Braking plays at arrival")
	var marsh=Player.new();marsh.load_manifest("res://character/animation-expansion-v5/marsh/manifest.json")
	for d in DIRS:
		for pair in [["sit-idle","weld"],["sleep","death-ground"],["carry","walk"],["swim","tread"]]:
			check(marsh.frames[pair[0]+"-"+d][0].get_image().get_data()!=marsh.frames[pair[1]+"-"+d][0].get_image().get_data(),"Distinct Marsh activity "+pair[0]+d)
	print("ANIMATION EXPANSION ","PASS" if failures==0 else "FAIL"," failures=",failures)
	quit(failures)
