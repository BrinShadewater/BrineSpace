extends SceneTree
const Assist=preload("res://scripts/companion_repair.gd")
const Hull=preload("res://scripts/hull_repair.gd")
const Companion=preload("res://scripts/companion_npc.gd")
class Worker extends RefCounted:
	var active=true
	var dead=false
	var goal="hull-repair"
	var state="weld"
	var expedition={}
	var locker_request={}
	var activity=""
	var timer=0.0
	var foot=Vector2(200,200)
	var goal_cell=Vector2i.ZERO
	var path=PackedVector2Array()
	var direction="north"
	var movement_medium="dry"
	var helmet_equipped=false
	func helmet_action_active():return false
	func can_stand(_point):return true
class JoshFixture extends "res://scripts/companion_npc.gd":
	func _init():super("josh")
	func topology(_main) -> String:return signature
	func can_stand(_point: Vector2) -> bool:return true
class Game extends RefCounted:
	const Architects=preload("res://scripts/architects.gd")
	var running=true
	var paused=false
	var hardware={"doors":false,"power":true,"pumps":false}
	var resources={"metal":20,"oxygen":20}
	var occupied={}
	var placed_rooms=[]
	var companion_actors={}
	var bill_npc=Worker.new()
	var veld_npc=Worker.new()
	var branforth_npc=Worker.new()
	var marsh_npc=Worker.new()
	var architect_run={}
	var logs=[]
	func _log(message,_important):logs.append(message)
	func _refresh_all():pass
var failures=0
func _init():call_deferred("run")
func check(ok,message):
	if not ok:failures+=1;push_error(message)
func run():
	var game=Game.new()
	var room={"pos":Vector2i.ZERO,"hull_crack":0.5,"water_level":0.0}
	game.occupied[Vector2i.ZERO]=room;game.placed_rooms=[room]
	check(Hull.request(game,Vector2i.ZERO),"Paid hull repair queues")
	check(game.resources.metal==17,"Normal three-metal cost retained")
	room.leak_repair.worker="bill";room.leak_repair.point=game.bill_npc.foot
	var josh=JoshFixture.new();josh.active=true;josh.foot=Vector2(260,200);josh.interest_cell=Vector2i.ZERO;josh.interest_point=game.bill_npc.foot;josh.direction="west"
	game.companion_actors.josh=josh
	check(not Assist.target(game,josh).is_empty(),"Finds an active crew repair")
	josh.start_behavior("torch")
	check(Assist.multiplier(game,Vector2i.ZERO)==1.0,"Deploy phase grants no work")
	josh.behavior_elapsed=1.0
	check(Assist.multiplier(game,Vector2i.ZERO)==1.25,"Lit torch contributes 25 percent")
	Hull.advance(game,game.bill_npc,1.0)
	check(is_equal_approx(room.leak_repair.progress,1.25),"Actual hull job consumes helper contribution")
	var saved=josh.personality_snapshot()
	check(Companion.valid_personality(saved,"josh"),"Mid-torch save accepted")
	check(not Companion.valid_personality(saved,"river"),"Other identities reject torch state")
	var restored=Companion.new("josh");restored.restore_personality(saved)
	check(restored.behavior=="torch" and restored.behavior_elapsed==1.0,"Torch phase restores")
	game.paused=true
	var before=room.leak_repair.progress;Hull.advance(game,game.bill_npc,1.0)
	check(room.leak_repair.progress==before and Assist.multiplier(game,Vector2i.ZERO)==1.0,"Pause freezes work")
	game.paused=false;game.hardware.doors=true
	check(Assist.multiplier(game,Vector2i.ZERO)==1.0,"Locked access disables helper")
	game.hardware.doors=false;room.water_level=0.5
	check(Assist.target(game,josh).is_empty(),"No dry blowtorch assistance in flooding")
	room.water_level=0.0;josh.foot=Vector2(350,200)
	check(Assist.multiplier(game,Vector2i.ZERO)==1.0,"Cannot repair from out of reach")
	josh.foot=Vector2(260,200);josh.behavior_elapsed=5.8
	check(Assist.multiplier(game,Vector2i.ZERO)==1.0,"Stow phase grants no work")
	josh.behavior_elapsed=1.0;game.bill_npc.dead=true
	check(Assist.target(game,josh).is_empty(),"No assistance without a living worker")
	game.bill_npc.dead=false
	for d in ["south","west","north","east"]:
		for phase in ["torch-enter","torch","torch-exit"]:
			check(josh.poses.frame_at_elapsed(phase+"-"+d,.2)!=null,"Torch texture "+phase+d)
	var pending=saved.duplicate(true);pending.action="";pending.elapsed=0.0;pending.duration=0.0;pending.pending="torch"
	check(Companion.valid_personality(pending,"josh"),"Travel to repair saves")
	Hull.advance(game,game.bill_npc,20.0)
	check(room.hull_crack==0.0 and not room.has("leak_repair"),"Assisted repair finishes normally")
	check(Assist.multiplier(game,Vector2i.ZERO)==1.0,"Completed job gives no further contribution")
	josh.update(game,0.01)
	check(josh.behavior=="torch" and josh.behavior_elapsed>=5.52,"Completed job immediately enters unlit stow")
	josh.update(game,0.6)
	check(josh.behavior.is_empty(),"Stow returns to ordinary companion idle")
	check(game.resources.metal==17,"Assistance does not charge or refund materials")
	print("COMPANION REPAIR ","PASS" if failures==0 else "FAIL"," failures=",failures)
	quit(failures)
