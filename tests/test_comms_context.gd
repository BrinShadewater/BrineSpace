extends SceneTree
class FakeGame extends RefCounted:
	var paused:=false
	func _set_paused(value: bool, _write_log:=false) -> void: paused=value
	var resources={"oxygen":100,"power":100,"food":100,"water":100}
	func _project_cycle_delta() -> Dictionary: return {"oxygen":-1,"power":-1,"food":-1,"water":0}
	var powered_room_cells={Vector2i(2,2):true}
	var bill_npc={"completed_activity":{},"active":true,"dead":false,"activity":"idle","goal_cell":Vector2i(2,2)}
	var veld_npc={"completed_activity":{},"active":false,"dead":false,"activity":"idle","goal_cell":Vector2i(2,2)}
	var branforth_npc={"completed_activity":{},"active":false,"dead":false,"activity":"idle","goal_cell":Vector2i(2,2)}
	var marsh_npc={"completed_activity":{},"active":false,"dead":false,"activity":"idle","goal_cell":Vector2i(2,2)}
func _init() -> void: call_deferred("run")
func run() -> void:
	var panel=preload("res://scripts/crew_comms.gd").new(); root.add_child(panel); panel.set_process(false)
	var game:=FakeGame.new(); panel.game=game
	panel.observe_game(); assert(panel.pending.size()==1 and panel.pending[0].speaker=="brine")
	panel.show_next(); var count: int=panel.history.size()
	panel.replay_history(1); assert(panel.history.size()==count,"Replay does not duplicate history")
	panel.observe_game(); assert(panel.pending.is_empty(),"Opening deduplicated")
	game.resources.oxygen=1; panel.observe_game(); assert(panel.pending.is_empty(),"Cooldown blocks ambient flood")
	panel.event_clock=46; panel.observe_game(); assert(panel.pending.size()==1)
	panel.event_clock=92; panel.observe_game(); assert(panel.pending.size()==1,"Same shortage deduplicated")
	game.resources.oxygen=100; game.veld_npc.active=true; panel.observe_game()
	assert(panel.pending.back().speaker=="veld","Recovered crew speak")
	panel.event_clock=140; game.bill_npc.activity="checking manifold gauges"; panel.observe_game()
	game.bill_npc.activity="looking around"; panel.observe_game()
	assert(panel.pending.back().speaker=="veld","An interrupted action must not claim completion")
	game.bill_npc.completed_activity={"serial":1,"activity":"checking manifold gauges","cell":Vector2i(2,2)}; panel.observe_game()
	assert(panel.pending.back().speaker=="bill","Completed room activity speaks")
	panel.game=null; panel.dismiss(); panel.transmit("brine","Slow words, with pauses."); panel.show_next()
	panel.text_speed=1; panel._process(0.3); var slow: int=panel.body.visible_characters
	panel.present_current(); panel.text_speed=2.25; panel._process(0.3)
	assert(panel.body.visible_characters>slow,"Speed setting affects reveal")
	print("COMMS CONTEXT PASS: greeting, shortage deduplication, cooldown, recovery, completed activity, history and speed")
	quit()
