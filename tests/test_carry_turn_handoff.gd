extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
func registered_pixels(texture: Texture2D) -> PackedByteArray:
	var canvas=Image.create(640,640,false,Image.FORMAT_RGBA8)
	var image=texture.get_image()
	canvas.blend_rect(image,Rect2i(Vector2i.ZERO,image.get_size()),Vector2i(Vector2(320,320)-texture.get_meta("crew_pivot")))
	return canvas.get_data()
func _init():call_deferred("run")
func run():
	var failures=0
	var cases=0
	for actor in ["bill","veld","branforth","marsh"]:
		var base: String=Player.REVISION_ROOTS[actor]
		var catalog=JSON.parse_string(FileAccess.get_file_as_string(base+"catalog.json"))
		var source=Player.new()
		for path in catalog.body:source.load_manifest(base+str(path),true)
		for path in catalog.equipment:source.load_equipment_manifest("diving-helmet",base+str(path))
		if actor!="marsh" and not source.equipment_frames.has("diving-helmet"):
			failures+=1;push_error("Expected crew helmet coverage missing: "+actor)
		for state in ["carry","swim","swim-carry"]:
			for equipment in (["","diving-helmet"] if source.equipment_frames.has("diving-helmet") else [""]):
				var pairs=[["east","west"],["west","east"]]
				if actor=="marsh":pairs.append_array([["north","south"],["south","north"],["east","north"],["north","east"],["west","north"],["north","west"],["east","south"],["south","east"],["west","south"],["south","west"]])
				for directions in pairs:
					var clip=state+"-turn-"+directions[0]+"-"+directions[1]
					if not source.frames.has(clip):
						failures+=1;push_error("Expected turn coverage missing: "+actor+clip)
						continue
					cases+=1
					var player=Player.new()
					player.frames=source.frames;player.timing=source.timing;player.strides=source.strides;player.equipment_frames=source.equipment_frames
					player.frame(state,directions[0],0.0,Vector2.ZERO,equipment,true)
					player.frame(state,directions[0],0.2,Vector2(0.05,0),equipment,true)
					player.frame(state,directions[1],0.3,Vector2(0.06,0),equipment,true)
					var end: float=0.3+player.cycle_seconds(clip)
					var last=player.frame(state,directions[1],end-0.001,Vector2(0.10,0),equipment,true)
					var saved=bytes_to_var(var_to_bytes(player.snapshot()))
					player=Player.new()
					player.frames=source.frames;player.timing=source.timing;player.strides=source.strides;player.equipment_frames=source.equipment_frames
					player.restore_snapshot(saved)
					var paused=player.frame(state,directions[1],end-0.001,Vector2(0.10,0),equipment,true)
					if paused!=last:failures+=1;push_error("Restored paused turn changed pose: "+actor+clip)
					var first=player.frame(state,directions[1],end+0.001,Vector2(0.11,0),equipment,true)
					var rows: Dictionary=source.frames if equipment.is_empty() else source.equipment_frames[equipment]
					var expected=rows[state+"-"+directions[1]][0]
					if registered_pixels(last)!=registered_pixels(expected) or first!=expected:
						failures+=1;push_error("Turn endpoint mismatch "+state+" "+actor+str(directions)+equipment+" phase="+str(player.phase))
					player.frame(state,directions[1],end+0.101,Vector2(0.13,0),equipment,true)
					var destination=state+"-"+directions[1]
					var expected_phase=0.02/float(player.strides.get(destination,player.strides.get(state,0.12)))*player.cycle_seconds(destination) if player.strides.has(state) or player.strides.has(destination) else 0.1
					if not is_equal_approx(player.phase,expected_phase):failures+=1;push_error("Turn resumed with stale clock: "+actor+clip+" phase="+str(player.phase)+" expected="+str(expected_phase))
	print("CREW TURN HANDOFF: ",cases," actor/body/equipment cases, failures=",failures)
	if not FileAccess.file_exists("res://tests/test_carry_turn_handoff.gd.uid"):
		var f=FileAccess.open("res://tests/test_carry_turn_handoff.gd.uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	quit(0 if failures==0 else 1)
