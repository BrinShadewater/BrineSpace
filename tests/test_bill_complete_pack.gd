extends SceneTree
## Verify the selected consumer, not just manifests sitting on disk.
var failures := 0
var count := 0
func check(ok: bool, message: String) -> void:
	count += 1
	if not ok:
		failures += 1
		push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_major_bill_animations()
	var player = grid.human_water_player
	var contract: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://tools/bill-art-source-contract.json"))
	# 175 contract states plus the three bunk states (enter, sleep, exit) added Sept 21.
	check(player.frames.size()==178,"All 178 body states selected")
	check(player.equipment_frames["diving-helmet"].size()==171,"All 171 equipped states selected")
	for entry in contract.states:
		var key: String=entry.id
		check(player.frames.has(key),key+" selected")
		if not player.frames.has(key):continue
		check(player.timing[key].durations==entry.timing.durations,key+" original durations")
		check(player.timing[key].loop==entry.timing.loop,key+" original loop behavior")
		var elapsed := 0.0
		for i in range(entry.frames.size()):
			var old: Dictionary=entry.frames[i]
			var frame: Texture2D=player.frames[key][i]
			check(frame.get_size()==Vector2(old.size[0],old.size[1])*2,key+" source density")
			check(frame.get_meta("crew_pivot")==Vector2(old.meta.crew_pivot[0],old.meta.crew_pivot[1])*2,key+" registered pivot")
			check(frame.get_meta("crew_standing_height")==148.0,key+" render calibration")
			for meta in ["crew_water_facing","crew_water_kind","crew_water_pose","crew_depth_offset"]:
				check(frame.get_meta(meta)==old.meta[meta],key+" preserved "+meta)
			var sample: float=elapsed+float(entry.timing.durations[i])/2000.0
			check(player.frame_at_elapsed(key,sample)==frame,key+" phase selection")
			if key in contract.equipmentStates:
				var gear: Texture2D=player.frame_at_elapsed(key,sample,"diving-helmet")
				check(gear!=null and gear.get_size()==frame.get_size(),key+" gear phase/canvas")
				check(gear.get_meta("crew_pivot")==frame.get_meta("crew_pivot"),key+" gear anchor")
			elapsed+=float(entry.timing.durations[i])/1000.0
	for facing in ["east","west","north","south"]:
		var key: String="walk-"+facing
		var stride: float=92.0*65.28/148.0/384.0 if facing in ["east","west"] else 0.12
		player.current_key=""
		player.frame("walk",facing,0.0,Vector2.ZERO)
		player.frame("walk",facing,1.0,Vector2(stride*0.34,0))
		var expected: float=player.cycle_seconds(key)*0.34
		check(is_equal_approx(player.phase,expected),key+" calibrated distance phase")
		grid.human_animation_key=""
		grid._advance_human_animation(key,0.0,Vector2.ZERO)
		check(is_equal_approx(grid._advance_human_animation(key,1.0,Vector2(stride*0.34,0)),expected),key+" legacy renderer calibrated phase")
		check(is_equal_approx(grid._advance_human_animation(key,1.0,Vector2(stride*0.34,0)),expected),key+" paused gait remains fixed")
	var npc=load("res://scripts/bill_npc.gd").new()
	npc.active=true
	check(npc.begin_helmet_action(true),"New locker manifest starts equip action")
	check(npc.timer>0,"Locker duration retained")
	grid.free()
	print("BILL COMPLETE PACK: %d checks, %d failures"%[count,failures])
	quit(1 if failures else 0)
