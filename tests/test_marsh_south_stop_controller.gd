extends SceneTree
const Stop=preload("res://character/marsh-south-stop-v1/stop_controller.gd")
class Probe extends Stop:
	var arrivals:=0
	var fallbacks:=0
	var floor_clear:=true
	var peer_clear:=true
	func can_stand(_p: Vector2) -> bool:return floor_clear
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return true
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return peer_clear
	func finish_south_stop_arrival() -> void:arrivals+=1;state="idle";timer=6
	func _step_base_arrive() -> void:fallbacks+=1;super._step_base_arrive()
class PausedMain:
	var paused:=true
	var running:=true
	func get_visual_time_seconds() -> float:return 0
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func actor_at_phase(player,slot: int):
	var actor=Probe.new();actor.active=true;actor.battery=100;actor.state="walk";actor.direction="south";actor.goal="curiosity"
	actor.foot=Vector2(100,200);actor.path=PackedVector2Array([Vector2(100,212)]);actor.bind_south_stop_player(player)
	actor.south_stop_time=1 # Actual playback advances distance only at a later time.
	player.current_key="walk-south";player.current_equipment="";player.phase=slot*.15+.04-12/(.128*384)*.9
	# Wrap the outgoing phase as real repeated gait playback does.
	player.phase=fposmod(player.phase,.9);player.last_position=actor.south_stop_position_cells();player.last_time=0;player.started=0
	player.motion={"state":"walk","direction":"south","clip":"","started":0.0}
	return actor
func run():
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations();var player=grid.marsh_player
	check(player.frames.has("walk-stop-phase4-south"),"normal catalog admits the authored South stop bank")
	player.load_manifest("res://character/marsh-south-walk-material-v1/candidate-02/manifest.json",true)
	player.load_manifest("res://character/marsh-south-idle-material-v1/candidate-01/manifest.json",true)
	player.load_manifest("res://character/marsh-south-stop-v1/candidate-07/phase-4/manifest.json",true)
	for manifest in ["res://character/marsh-south-stop-v1/candidate-06/phase-0/manifest.json","res://character/marsh-south-stop-v1/candidate-06/phase-1/manifest.json","res://character/marsh-south-stop-v1/candidate-06/phase-2/manifest.json","res://character/marsh-south-stop-v1/candidate-01/phase-3/manifest.json","res://character/marsh-south-stop-v1/candidate-01/phase-5/manifest.json"]:player.load_manifest(manifest,true)
	for slot in range(6):
		var actor=actor_at_phase(player,slot);actor.move(12/46.0)
		check(actor.foot==Vector2(100,212) and actor.path.is_empty(),"actual navigation reaches terminal foot for phase%d"%slot)
		check(actor.south_stop_active() and actor.south_stop_phase==slot,"actual loaded outgoing phase selects its authored stop")
		check(actor.fallbacks==0,"available branch defers base arrival")
	for phase in range(6):
		for dt in [.01,.02,.08,.1,.4,.7]:
			var actor=actor_at_phase(player,phase);actor.move(12/46.0)
			check(actor.south_stop_active() and actor.arrivals==0,"arrival callback waits behind finite artwork")
			check(player.frame_at_elapsed(actor.animation_state()+"-south",actor.action_elapsed()).get_image().get_data()==player.frames["walk-south"][phase].get_image().get_data(),"exact outgoing gait begins stop")
			var main=PausedMain.new();actor.update(main,.2);check(actor.south_stop_clock==0,"pause freezes actual controller")
			actor.move(0);check(actor.south_stop_clock==0,"zero delta freezes actual controller")
			while actor.south_stop_active():actor.advance_south_stop(dt)
			check(actor.arrivals==1 and actor.foot==Vector2(100,212),"finite stop completes callback once without root translation")
			var elapsed: float=actor.south_stop_idle_elapsed
			actor.prepare_stop_pose(player,5,actor.south_stop_position_cells())
			check(player.current_key=="idle-south" and is_equal_approx(player.phase,elapsed),"completion owns idle clock seed including large-delta residue")
			check(player.frame("idle","south",5,actor.south_stop_position_cells())==player.frames["idle-south"][0],"idle0 is exact first completion pose")
			check(player.frame("idle","south",5+.651-elapsed,actor.south_stop_position_cells())==player.frames["idle-south"][1],"idle650ms hold is measured from completion")
			actor.advance_south_stop(1);check(actor.arrivals==1,"completed stop cannot repeat old callback")
	var changes=[{"dead":true},{"helmet_equipped":true},{"direction":"east"},{"stage":"kneel"},{"movement_medium":"swim"},{"flood_speed":.7},{"injury_pending":true},{"battery":35.0},{"returning_to_pod":true},{"recharge_docked":true},{"running_motion":true},{"goal":"fire-retreat"},{"foot":Vector2(100,213)},{"floor_clear":false},{"peer_clear":false}]
	for phase in range(6):
		for change in changes:
			var actor=actor_at_phase(player,phase);actor.move(12/46.0)
			for field in change:actor.set(field,change[field])
			check(not actor.south_stop_active() and actor.arrivals==0,"priority/context invalidation releases without old callback: "+str(change))
		var actor=actor_at_phase(player,phase);actor.move(12/46.0);actor.goal=""
		actor.choose_goal(null)
		check(actor.south_stop_active() and actor.south_stop_cancelled and actor.south_stop_goal.is_empty(),"released work identity clears before stationary settle")
		actor.advance_south_stop(.4)
		check(actor.arrivals==0 and actor.timer==0,"cancelled work never receives arrival callback")
	# A delayed first draw must select the pending South-start distance seed.
	# Base navigation uses relative Vector2 tolerance at large station coordinates.
	var near_actor=actor_at_phase(player,5)
	near_actor.foot=Vector2(8176,7770.761640625)
	var requested=Vector2(8176,7771.71741981982)
	near_actor.path=PackedVector2Array([requested]);player.last_position=near_actor.south_stop_position_cells()
	near_actor.move(.02)
	var anchor: Vector2=near_actor.foot
	check(anchor!=requested and anchor.is_equal_approx(requested) and near_actor.path.is_empty(),"real base navigation may finish slightly short at large coordinates")
	check(near_actor.south_stop_active() and near_actor.south_stop_foot==anchor,"stop anchors actual base arrival without snapping requested endpoint")
	near_actor.advance_south_stop(.4)
	check(near_actor.foot==anchor and near_actor.arrivals==1,"approximate base endpoint remains stationary through settlement")
	var actor=actor_at_phase(player,0);actor.south_pending=true
	actor.south_target=actor.path[0];actor.south_goal=actor.goal
	actor.south_gait_origin=Vector2(100,212)-Vector2(0,(.64-.68+.9)/.9*.128*384)
	actor.south_origin=actor.south_gait_origin-Vector2(0,actor.SOUTH_ADVANCE)
	actor.move(12/46.0)
	check(actor.south_stop_active() and actor.south_stop_phase==4 and not actor.south_pending,"unrendered South start seeds actual phase4 on arrival")
	var saved=player.frames["walk-stop-phase2-south"];player.frames.erase("walk-stop-phase2-south")
	actor=actor_at_phase(player,2);actor.move(12/46.0)
	check(not actor.south_stop_active() and actor.fallbacks==1,"missing staged bank delegates actual base arrival")
	player.frames["walk-stop-phase2-south"]=saved
	actor=actor_at_phase(player,3);actor.move(12/46.0);actor.south_stop_phase=9
	check(not actor.south_stop_active() and actor.south_stop_phase==-1 and actor.arrivals==0,"invalid stored branch clears without callback")
	grid.free();print("MARSH SOUTH STOP CONTROLLER: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
