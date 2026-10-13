extends SceneTree
const PACKS := {
	"bill":"res://character/crew-runtime-matte-v1/bill/manifest.json",
	"veld":"res://character/crew-runtime-matte-v1/veld/manifest.json",
	"branforth":"res://character/crew-runtime-matte-v1/branforth/manifest.json"}
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(why)
func _init() -> void: call_deferred("run")
func run() -> void:
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_major_bill_animations()
	grid._load_replacement_crew_animations()
	for actor in PACKS:
		var p = grid.human_water_player if actor == "bill" else grid.get(actor+"_player")
		var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(PACKS[actor]))
		for s in pack.states:
			var key: String = s.id
			check(p.frames[key].size() == s.frameCount, actor+key+" count")
			var elapsed := 0.0
			for i in range(s.frameCount):
				var texture = p.frame_at_elapsed(key,elapsed+float(s.frameDurationsMs[i])/2000.0)
				var expected = Image.load_from_file(str(PACKS[actor]).get_base_dir().path_join(s.frameFiles[i]))
				check(texture.get_image().get_data()==expected.get_data(),actor+key+" loaded pixels")
				check(texture.get_meta("crew_pivot")==Vector2(92,172),actor+key+" pivot")
				check(texture is CanvasTexture and texture.texture_filter==CanvasItem.TEXTURE_FILTER_LINEAR,actor+key+" approved linear sampling")
				elapsed += float(s.frameDurationsMs[i])/1000.0
			if key.begins_with("walk-"):
				var cycles: int = s.gaitCycles
				check(is_equal_approx(p.strides[key],cycles*69.0/384.0),actor+key+" full clip travel")
				var expected_cycle: float = ({"walk-east":1.625,"walk-west":1.680}[key]) if actor == "branforth" and key in ["walk-east", "walk-west"] else cycles*1.5
				if actor == "bill": expected_cycle = {"walk-south":2.458,"walk-east":2.0,"walk-north":1.5,"walk-west":2.0}[key]
				check(is_equal_approx(elapsed,expected_cycle),actor+key+" cycle timing")
				p.current_key=""
				p.frame("walk",key.trim_prefix("walk-"),0,Vector2.ZERO)
				p.frame("walk",key.trim_prefix("walk-"),0.75,Vector2(69.0/768.0,0))
				check(is_equal_approx(p.phase,expected_cycle/(2.0*cycles)),actor+key+" half physical stride")
				var snapshot: Dictionary=p.snapshot()
				p.frame("walk",key.trim_prefix("walk-"),0.75,Vector2(69.0/768.0,0))
				check(p.snapshot()==snapshot,actor+key+" pause stable")
			var gear: Array=p.equipment_frames["diving-helmet"][key]
			check(not gear.is_empty(),actor+key+" helmet preserved")
			if actor == "bill":
				var helmet_pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-shared-helmet-runtime-v2/manifest.json"))
				for helmet_state in helmet_pack.states:
					if helmet_state.id != key: continue
					check(gear.size()==helmet_state.frameCount,actor+key+" shared helmet count")
					for sample in [0, int(gear.size()/2.0), gear.size()-1]:
						var expected_helmet:=Image.load_from_file("res://character/bill-shared-helmet-runtime-v2/"+helmet_state.frameFiles[sample])
						check(gear[sample].get_image().get_data()==expected_helmet.get_data(),actor+key+" shared helmet pixels")
			if actor == "veld":
				var veld_pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/veld-shared-helmet-v1/manifest.json"))
				for veld_state in veld_pack.states:
					if veld_state.id != key: continue
					check(gear.size()==veld_state.frameCount,actor+key+" shared helmet count")
					for sample in [0, int(gear.size()/2.0), gear.size()-1]:
						var expected_veld:=Image.load_from_file("res://character/veld-shared-helmet-v1/"+veld_state.frameFiles[sample])
						check(gear[sample].get_image().get_data()==expected_veld.get_data(),actor+key+" shared helmet pixels")
			if actor == "branforth":
				var helmet_pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-shared-helmet-runtime-v1/manifest.json"))
				for helmet_state in helmet_pack.states:
					if helmet_state.id != key: continue
					check(gear.size()==helmet_state.frameCount,actor+key+" shared helmet count")
					for sample in [0, int(gear.size()/2.0), gear.size()-1]:
						var expected_helmet:=Image.load_from_file("res://character/james-shared-helmet-runtime-v1/"+helmet_state.frameFiles[sample])
						check(gear[sample].get_image().get_data()==expected_helmet.get_data(),actor+key+" shared helmet pixels")
			var gear_time:=0.0
			for i in range(gear.size()):
				var duration: float=p.equipment_timing["diving-helmet"][key].durations[i]/1000.0
				check(p.frame_at_elapsed(key,gear_time+duration*0.5,"diving-helmet")==gear[i],actor+key+" independent helmet timing")
				gear_time+=duration
	grid.free()
	print("CREW WALK V2: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
