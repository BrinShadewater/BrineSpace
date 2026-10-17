extends SceneTree
var failures:=0
var checks:=0
func check(ok: bool,why: String):
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init():call_deferred("run")
func run():
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	if failures:quit(2);return
	var player=preload("res://scripts/crew_sprite_player.gd").new()
	player.load_manifest("res://character/james-lying-family-v1/bare-manifest.json")
	check(player.load_equipment_manifest("diving-helmet","res://character/james-lying-family-v1/helmet-manifest.json"),"Paired helmet contract")
	var eq: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-lying-family-v1/helmet-manifest.json"))
	var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-lying-family-v1/bare-manifest.json"))
	for state in manifest.states:
		var key: String=state.id
		check(player.frames[key].size()==6,"Six authored slots "+key)
		var elapsed: float=0.0
		for slot in range(6):
			var tex: Texture2D=player.frames[key][slot]
			var disk:=Image.load_from_file("res://character/james-lying-family-v1/"+state.frameFiles[slot])
			check(tex.get_image().get_data()==disk.get_data(),"Exact authored pixels "+key+str(slot))
			check(tex.get_meta("crew_pivot")==Vector2(128,224),"Pivot "+key)
			check(tex.get_meta("crew_standing_height")==148.0,"Scale metadata "+key)
			check(tex.get_meta("crew_depth_offset")==state.depthOffsets[slot],"Furniture depth "+key)
			check(player.frame_at_elapsed(key,elapsed+float(state.frameDurationsMs[slot])/2000.0)==tex,"Simulation clock slot "+key+str(slot))
			if key.begins_with("sleep-"):check(tex.get_meta("crew_rest_head_offset")==Vector2(state.restHeadOffset[0],state.restHeadOffset[1]),"Pillow metadata "+key)

			var es: Dictionary=eq.states.filter(func(v):return v.id==key)[0]
			var et: Texture2D=player.equipment_frames["diving-helmet"][key][slot]
			var ei:=Image.load_from_file("res://character/james-lying-family-v1/"+es.frameFiles[slot])
			check(et.get_image().get_data()==ei.get_data(),"Exact helmet pixels "+key)
			check(et.get_meta("crew_pivot")==tex.get_meta("crew_pivot"),"Paired pivot "+key)
			check(et.get_meta("crew_standing_height")==tex.get_meta("crew_standing_height"),"Paired anatomy "+key)
			check(et.get_meta("crew_depth_offset")==tex.get_meta("crew_depth_offset"),"Paired furniture depth "+key)
			check(player.frame_at_elapsed(key,elapsed+float(state.frameDurationsMs[slot])/2000.0,"diving-helmet")==et,"Helmet clock "+key)
			if key.begins_with("sleep-"):check(et.get_meta("crew_rest_head_offset")==tex.get_meta("crew_rest_head_offset"),"Paired pillow anchor "+key)
			elapsed+=float(state.frameDurationsMs[slot])/1000.0
		check(absf(player.cycle_seconds(key)-elapsed)<0.001,"Cycle duration "+key)
	print("JAMES PAIRED LYING: ",checks," native loader/clock checks; ",failures," failures; staged only, no room contact claim")
	quit(1 if failures else 0)
