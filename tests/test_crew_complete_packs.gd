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
		check(player.frames.size()==contract.states.size()+supplements.size(),actor+" body coverage")
		check(player.equipment_frames.get("diving-helmet",{}).size()==(0 if actor=="marsh" else contract.equipment.size()),actor+" gear coverage")
		for entry in contract.states:
			var key: String=entry.id
			# JSON timing values are floats; Array equality also compares element types.
			var expected_durations: Array=[130.0,170.0,150.0,200.0,150.0,100.0] if actor=="branforth" and key=="walk-west" else entry.timing.durations
			check(player.frames.has(key),actor+" selected "+key)
			if not player.frames.has(key):continue
			check(player.frames[key].size()==entry.frames.size(),actor+" count "+key)
			check(player.timing[key].durations==expected_durations,actor+" durations "+key)
			check(player.timing[key].loop==entry.timing.loop,actor+" loop "+key)
			var elapsed:=0.0
			for i in range(entry.frames.size()):
				var texture: Texture2D=player.frames[key][i]
				check(texture.get_meta("crew_standing_height")==148.0,actor+" density "+key)
				for meta in ["crew_water_facing","crew_water_kind","crew_water_pose","crew_depth_offset"]:
					check(texture.get_meta(meta)==entry.frames[i].meta[meta],actor+" metadata "+key+" "+meta)
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
				check(texture.get_meta("crew_standing_height")==148.0 and not texture.get_meta("crew_water_pose"),key+" supplemental dry density")
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
