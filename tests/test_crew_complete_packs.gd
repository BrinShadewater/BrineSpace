extends SceneTree
## Verify the live renderer's selected packs, not only independent catalog loads.
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks+=1
	if not ok: failures+=1;push_error(why)
func _init() -> void: call_deferred("run")
func run() -> void:
	var grid=load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	for actor in ["veld","branforth","marsh"]:
		var player=grid.get(actor+"_player")
		var contract: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://tools/crew-art-source-contracts/"+actor+".json"))
		var supplements: Dictionary={}
		var extra_path: String="res://tools/crew-art-source-contracts/"+actor+"-supplemental.json"
		if FileAccess.file_exists(extra_path):supplements=JSON.parse_string(FileAccess.get_file_as_string(extra_path))
		var bunk_keys := ["bunk-enter-east", "bunk-sleep-east", "bunk-exit-east"]
		var berth_keys: Array = ["berth-lie-east","berth-sleep-east","berth-rise-east"] if actor=="marsh" else []
		var expected_keys: Dictionary={}
		for entry in contract.states:expected_keys[entry.id]=true
		for key in supplements:expected_keys[key]=true
		for key in bunk_keys+berth_keys:expected_keys[key]=true
		check(player.frames.size()==expected_keys.size(),actor+" body coverage")
		check(player.equipment_frames.get("diving-helmet",{}).size()==(0 if actor=="marsh" else contract.equipment.size()+bunk_keys.size()),actor+" gear coverage")
		for key in bunk_keys:
			check(player.frames.has(key), actor+" selected bunk "+key)
			if not player.frames.has(key): continue
			check(player.frames[key].size()==(1 if key=="bunk-sleep-east" else 7),actor+" bunk frame count "+key)
			check(player.timing[key].loop==(key=="bunk-sleep-east"),actor+" bunk loop "+key)
			if actor!="marsh":
				check(player.equipment_frames.get("diving-helmet",{}).get(key,[]).size()==player.frames[key].size(),actor+" bunk gear "+key)
		for key in berth_keys:
			check(player.frames.has(key),actor+" selected legacy berth "+key)
			if player.frames.has(key):
				check(player.frames[key].size()==(1 if key=="berth-sleep-east" else 6),actor+" legacy berth count "+key)
				check(player.timing[key].loop==(key=="berth-sleep-east"),actor+" legacy berth loop "+key)
		for entry in contract.states:
			var key: String=entry.id
			# JSON timing values are floats; Array equality also compares element types.
			var expected_durations: Array=[130.0,170.0,150.0,200.0,150.0,100.0] if actor=="branforth" and key=="walk-west" else entry.timing.durations
			check(player.frames.has(key),actor+" selected "+key)
			if not player.frames.has(key):continue
			check(player.frames[key].size()==entry.frames.size(),actor+" count "+key)
			check(player.timing[key].durations==expected_durations,actor+" durations "+key)
			check(player.timing[key].loop==supplements.get(key,{}).get("loop",entry.timing.loop),actor+" loop "+key)
			var elapsed:=0.0
			for i in range(entry.frames.size()):
				var texture: Texture2D=player.frames[key][i]
				check(texture.get_meta("crew_standing_height")==148.0,actor+" density "+key)
				for meta in ["crew_water_facing","crew_water_kind","crew_water_pose","crew_depth_offset"]:
					var expected: Variant = entry.frames[i].meta[meta]
					if supplements.has(key) and supplements[key].has("metadata"):
						expected=supplements[key].metadata[meta][i]
					# Selected south seating carries Marsh across the furniture front edge.
					# The frozen migration contract predates this reviewed draw-order repair.
					if actor=="marsh" and meta=="crew_depth_offset":
						if key in ["sit-idle-south","read-seated-south"]: expected=40.0
						elif key=="sit-down-south": expected=40.0*i/maxi(1,entry.frames.size()-1)
						elif key=="sit-rise-south": expected=40.0*(entry.frames.size()-1-i)/maxi(1,entry.frames.size()-1)
					check(texture.get_meta(meta)==expected,actor+" metadata "+key+" "+meta)
				check(player.frame_at_elapsed(key,elapsed+float(expected_durations[i])/2000.0)==texture,actor+" playback "+key)
				elapsed+=float(expected_durations[i])/1000.0
		for key in supplements:
			var expected: Dictionary=supplements[key]
			check(player.frames.has(key),actor+" supplemental state "+key)
			if not player.frames.has(key):continue
			check(player.frames[key].size()==expected.sha256.size(),key+" supplemental count")
			check(player.timing[key].durations==expected.durations and player.timing[key].loop==expected.loop,key+" supplemental timing")
			var manifest_path: String=player.REVISION_ROOTS[actor]+expected.manifest
			var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
			var files: Array=[]
			for entry in pack.states:
				if entry.id==key:files=entry.frameFiles
			check(files.size()==expected.sha256.size(),key+" supplemental manifest count")
			var elapsed:=0.0
			for i in range(mini(files.size(),player.frames[key].size())):
				var texture: Texture2D=player.frames[key][i]
				var file: String=manifest_path.get_base_dir().path_join(files[i])
				check(FileAccess.get_sha256(file)==expected.sha256[i],key+" selected pixels")
				check(texture.get_image().get_data()==Image.load_from_file(file).get_data(),key+" rendered source pixels")
				check(texture.get_size()==Vector2(expected.canvas[0],expected.canvas[1]) and texture.get_meta("crew_pivot")==Vector2(expected.pivot[0],expected.pivot[1]),key+" supplemental registration")
				var water_poses:Array=expected.get("metadata",{}).get("crew_water_pose",[])
				check(texture.get_meta("crew_standing_height")==148.0 and texture.get_meta("crew_water_pose")== (water_poses[i] if not water_poses.is_empty() else expected.get("water",false)),key+" supplemental density and medium")
				check(player.frame_at_elapsed(key,elapsed+float(expected.durations[i])/2000.0)==texture,key+" supplemental playback")
				elapsed+=float(expected.durations[i])/1000.0
		for direction in ["east","west","north","south"]:
			player.current_key=""
			player.frame("walk",direction,0.0,Vector2.ZERO)
			var stride: float=player.strides.get("walk-"+direction,player.strides.walk)
			player.frame("walk",direction,1.0,Vector2(stride*0.34,0))
			check(is_equal_approx(player.phase,player.cycle_seconds("walk-"+direction)*0.34),actor+" distance cadence "+direction)
			var snapshot: Dictionary=player.snapshot()
			player.frame("walk",direction,1.0,Vector2(stride*0.34,0))
			check(player.snapshot()==snapshot,actor+" paused cadence "+direction)
		var npc=load("res://scripts/"+actor+"_npc.gd").new()
		npc.active=true
		check(npc.begin_helmet_action(true)==(actor!="marsh"),actor+" equipment semantics")
		if actor!="marsh":check(npc.timer>0,actor+" locker timing")
	grid.free()
	print("CREW COMPLETE PACKS: %d checks, %d failures"%[checks,failures])
	quit(1 if failures else 0)
