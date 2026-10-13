extends SceneTree
const Life=preload("res://scripts/crew_life.gd")
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok: bool,label: String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func run():
	var Store=preload("res://scripts/room_layout_store.gd")
	Store.loaded=true;Store.data={}
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://sleep-interruption-test.loop";game.meta.save_path="user://sleep-interruption-test.meta"
	root.add_child(game);current_scene=game
	await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	game.bill_npc.active=false;game.veld_npc.active=false;game.branforth_npc.active=false
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear()
	var cell=Vector2i(20,20)
	game.selected_rotation=0;game._place_room("crew_hab",cell,true)
	for actor in ["bill","veld","branforth"]:
		var npc=load("res://scripts/"+actor+"_npc.gd").new()
		npc.rebuild(game);npc.active=true
		var station=npc.RoomActivity.stations(npc.geometry[cell])[0]
		npc.foot=(Vector2(cell)+Vector2.ONE*0.5)*384+station.point
		check(npc.can_stand(npc.foot),actor+" fixture approach clear")
		# The clips the game plays: its loader retimes some catalog clips (Veld's rest family).
		var player=game.grid_view.human_water_player if actor=="bill" else game.grid_view.get(actor+"_player")
		# Each actor times lie-down and get-up from their own art (Veld's rest family is longer).
		npc.stage="life_lie"
		var rest:=float(Life.seconds(npc,"life_lie"))
		check(is_equal_approx(rest,float(Life.seconds(npc,"life_get_up"))),actor+" rest entry and exit share a duration")
		for direction in ["north","east","south","west"]:
			for elapsed in [0.05,0.15,0.25,0.45,0.65,0.79]:
				npc.path.clear();npc.goal="fatigue";npc.goal_cell=cell;npc.direction=direction
				npc.state="idle";npc.stage="life_lie";npc.timer=rest-elapsed
				npc.activity="resting in the berth"
				for need in npc.needs:npc.needs[need]=90.0 if need=="fatigue" else 0.0
				check(is_equal_approx(npc.interrupted_life_rise_seconds(),elapsed),actor+" partial rise duration")
				# One millisecond of actual update should move backward by one millisecond.
				npc.timer+=0.001
				var expected_offset=Life.offset(npc)+Life.head_alignment(npc,player)
				npc.timer-=0.001
				var expected=player.frame_at_elapsed("lie-down-"+direction,elapsed-0.001)
				var serial=int(npc.completed_activity.get("serial",0))
				game.powered_room_cells.erase(cell)
				npc.update(game,0.001)
				check(npc.stage=="life_get_up" and is_equal_approx(npc.timer,elapsed-0.001),actor+" live service interruption reverses partial entry")
				var actual=player.frame_at_elapsed("get-up-"+direction,Life.elapsed(npc))
				check(actual.get_image().get_data()==expected.get_image().get_data(),actor+" no pixel pose jump "+direction)
				check((Life.offset(npc)+Life.head_alignment(npc,player)).distance_to(expected_offset)<0.001,actor+" contact preserved")
				check(int(npc.completed_activity.get("serial",0))==serial,actor+" interrupted activity emits no completion")
				check(npc.valid_snapshot(npc.snapshot()),actor+" partial rise snapshot remains valid")
			var boundary:=0.0
			for duration in player.timing["lie-down-"+direction].durations:
				boundary+=float(duration)/1000.0
				if boundary>=rest-0.001:continue
				npc.stage="life_lie";npc.timer=rest-boundary
				# The pose just entered. Sampling a hair past the boundary keeps this independent of
				# float rounding in the summed frame durations (65+85+100 ms lands one ulp short of 250).
				var a=player.frame_at_elapsed("lie-down-"+direction,boundary+0.00000001)
				var b=player.frame_at_elapsed("get-up-"+direction,rest-npc.interrupted_life_rise_seconds())
				check(a.get_image().get_data()==b.get_image().get_data(),actor+" exact boundary preserves current pose "+direction)
			npc.stage="life_sleep"
			check(is_equal_approx(npc.interrupted_life_rise_seconds(),rest),actor+" full sleep retains full rise")
	print("SLEEP INTERRUPTION: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
