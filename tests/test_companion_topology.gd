extends SceneTree
class Game extends RefCounted:
	var running:=true
	var paused:=false
	var occupied:Dictionary={}
	var placed_rooms:Array=[]
	func get_room_doors(_room):return ["north","east","south","west"]
class Motion extends RefCounted:
	func advance(_actor,_state,_direction,_delta):pass
	func restore(_data):pass
class Actor extends "res://scripts/companion_npc.gd":
	var topology_calls:=0
	var rebuild_calls:=0
	func topology(main)->String:
		topology_calls+=1
		return super.topology(main)
	func rebuild(main,_allow_defer:=true)->void:
		rebuild_calls+=1
		signature=topology(main)
	func can_stand(_point:Vector2)->bool:return true
	func _make_way(_main,_delta:float)->bool:return false
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _initialize():call_deferred("run")
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var game:=Game.new();var room:Dictionary={"id":"solar_array","pos":Vector2i.ZERO,"rotation":0,"water_level":0.0}
	game.occupied[Vector2i.ZERO]=room;game.placed_rooms=[room]
	for identity in ["margot","river"]:
		var actor:=Actor.new();actor.identity=identity;actor.active=true;actor.foot=Vector2(192,192)
		actor.locomotion=Motion.new();actor.behavior="nap";actor.behavior_duration=100
		actor.signature=actor.topology(game);actor.topology_calls=0
		actor.update(game,1.0/60.0)
		check(actor.topology_calls==1,"One complete topology read per normal update: "+identity)
		check(actor.rebuild_calls==0 and actor.behavior_elapsed>0,"Unchanged navigation and behavior advance: "+identity)
		room.doors_locked=true;actor.topology_calls=0;actor.update(game,1.0/60.0)
		check(actor.rebuild_calls==1 and actor.topology_calls==2,"Lock change validates and records rebuilt signature: "+identity)
		check(actor.locked_room_cells.has(Vector2i.ZERO),"Locked-cell snapshot refreshed: "+identity)
		room.doors_locked=false;actor.topology_calls=0;actor._advance_companion(game,1.0/60.0)
		check(actor.rebuild_calls==2 and actor.topology_calls==2,"Direct helper call keeps live validation: "+identity)
		check(actor.locked_room_cells.is_empty(),"Direct helper refreshes unlocked cells: "+identity)
		room.fire=1.0;actor.topology_calls=0
		var before_fire:float=actor.behavior_elapsed
		actor.update(game,1.0/60.0)
		check(actor.topology_calls==1 and actor.goal=="fire-retreat","Fire retreat returns after validated topology: "+identity)
		check(actor.behavior_elapsed==0 and actor.behavior.is_empty() and before_fire>0,"Fire retreat keeps behavior interruption: "+identity)
		room.fire=0.0
		actor.topology_calls=0;actor.update(game,0.0)
		check(actor.topology_calls==0,"Zero delta does no topology work: "+identity)
		actor.active=false;actor.update(game,1.0/60.0)
		check(actor.topology_calls==0,"Inactive companion stays untouched: "+identity)
		actor.active=true;game.paused=true;actor.update(game,1.0/60.0)
		check(actor.topology_calls==0,"Paused game stays untouched: "+identity)
		game.paused=false;game.running=false;actor.update(game,1.0/60.0)
		check(actor.topology_calls==0,"Stopped game stays untouched: "+identity)
		game.running=true
	var josh:=Actor.new();josh.identity="josh";josh.active=true;josh.foot=Vector2(192,192);josh.locomotion=Motion.new()
	room.water_level=1.0;josh.update(game,1.0/60.0)
	check(josh.topology_calls==0 and josh.water.mode=="offline","Water powerdown exits before navigation")
	print("COMPANION_TOPOLOGY ",checks," checks; failures=",failures)
	quit(1 if failures else 0)
