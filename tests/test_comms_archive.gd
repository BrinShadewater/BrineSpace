extends SceneTree
const Comms=preload("res://scripts/crew_comms.gd")
class CrewState extends RefCounted:
	var active:=false
	var dead:=false
	var completed_activity:Dictionary={}
class SavedStation extends Node:
	var bill_npc=CrewState.new()
	var veld_npc=CrewState.new()
	var branforth_npc=CrewState.new()
	var marsh_npc=CrewState.new()
	var resources={"oxygen":12,"power":6,"food":12,"water":6}
	func _project_cycle_delta() -> Dictionary:return {}
func _init() -> void: call_deferred("run")
func run() -> void:
	DirAccess.make_dir_recursive_absolute("res://output/comms-archive")
	var path: String="res://output/comms-archive/test-%d.json"%OS.get_process_id()
	var first=Comms.new(); first.archive_path=path; root.add_child(first); first.set_process(false)
	first.transmit("brine","A message worth keeping."); first.show_next()
	first.transmit("bill","The gauge is steady."); first.show_next()
	assert(FileAccess.file_exists(path))
	var restored=Comms.new(); restored.archive_path=path; root.add_child(restored); restored.set_process(false)
	assert(restored.history.size()==2 and restored.history[0].speaker=="brine")
	restored.replay_history(1); assert(restored.current.text=="A message worth keeping.")
	assert(restored.history.size()==2)
	for i in range(35): restored.transmit("brine","Record %d"%i); restored.show_next()
	assert(restored.history.size()==30)
	var file:=FileAccess.open(path,FileAccess.WRITE); file.store_string("damaged archive"); file.close()
	var broken=Comms.new(); broken.archive_path=path; root.add_child(broken); broken.set_process(false)
	broken.transmit("bill","Keep the original."); broken.show_next()
	assert(FileAccess.get_file_as_string(path)=="damaged archive","Malformed history preserved")
	# Save/Continue keeps what was already said: a restored comms never repeats a keyed line,
	# and drops the same line if it was queued while the checkpoint loaded.
	var said=Comms.new(); said.archive_path=path+".said"; root.add_child(said); said.set_process(false)
	assert(said.transmit("bill","Still breathing.","awake/bill"))
	said.show_next()
	var state: Dictionary=said.snapshot()
	var resumed=Comms.new(); resumed.archive_path=path+".resumed"; root.add_child(resumed); resumed.set_process(false)
	assert(resumed.transmit("bill","Still breathing.","awake/bill"),"Fresh comms queue a wake line before the restore lands")
	resumed.restore_state(state)
	assert(resumed.pending.is_empty(),"Restored state drops a wake line queued during the load")
	assert(not resumed.transmit("bill","Still breathing.","awake/bill"),"Restored comms do not repeat a keyed line")
	assert(resumed.transmit("bill","A new observation.","finding/1"),"Unsaid lines still transmit")
	var wake_failures:=check_opening_restore()
	print("COMMS ARCHIVE: opening restore failures=",wake_failures)
	print("COMMS ARCHIVE PASS: disk reload, replay, atomic replacement, bounded history, malformed preservation, said lines survive Continue")
	quit(1 if wake_failures else 0)

func check_opening_restore() -> int:
	var failures:=0
	for starter in Comms.Architects.IDS:
		var station=SavedStation.new();root.add_child(station)
		Comms.Architects.actor_for(station,starter).active=true
		var comms=Comms.new();comms.game=station
		# The initial crew line uses opening/crew, not awake/<architect>.
		comms.restore_state({"seen":["opening","opening/crew","opening/objective"],"greeting_sent":true})
		comms.observe_game()
		if not comms.pending.is_empty():
			failures+=1;push_error("Continue repeats the starting architect's wake line: "+starter)
		comms.pending.clear();comms.event_clock=60.0
		var newcomer:String="veld" if starter!="veld" else "bill"
		Comms.Architects.actor_for(station,newcomer).active=true
		comms.observe_game()
		if comms.pending.size()!=1 or comms.pending[0].get("key","")!="awake/"+newcomer:
			failures+=1;push_error("A newly thawed architect must still announce waking: "+newcomer)
		comms.free();station.free()
	return failures
