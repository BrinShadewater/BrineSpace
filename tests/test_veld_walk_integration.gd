extends SceneTree
const PACK := "res://character/crew-runtime-matte-v1/veld/manifest.json"
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(why)
func _init() -> void: call_deferred("run")
func run() -> void:
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_replacement_crew_animations()
	var p = grid.veld_player
	var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(PACK))
	for entry in pack.states:
		var key: String = entry.id
		check(p.frames[key].size() == entry.frameFiles.size(), key + " count")
		var elapsed := 0.0
		for i in range(entry.frameFiles.size()):
			var source := Image.load_from_file(PACK.get_base_dir().path_join(entry.frameFiles[i]))
			var tex: Texture2D = p.frame_at_elapsed(key, elapsed + float(entry.frameDurationsMs[i])/2000.0)
			check(tex.get_image().get_data() == source.get_data(), key + " exact accepted pixels")
			check(tex.get_meta("crew_pivot") == Vector2(92,172) and tex.get_meta("crew_standing_height") == 148.0, key + " registration")
			elapsed += float(entry.frameDurationsMs[i])/1000.0
		# Older helmet rows must remain readable at every phase after the bare override.
		var gear: Array = p.equipment_frames["diving-helmet"][key]
		elapsed = 0.0
		for i in range(gear.size()):
			var duration: float = p.equipment_timing["diving-helmet"][key].durations[i]/1000.0
			check(p.frame_at_elapsed(key, elapsed + duration*0.5, "diving-helmet") == gear[i], key + " original helmet timing")
			elapsed += duration
	for gear in ["", "diving-helmet"]:
		for direction in ["south", "east", "north", "west"]:
			p.current_key = ""
			p.frame("walk", direction, 0.0, Vector2.ZERO, gear)
			var strides: Dictionary = p.strides if gear.is_empty() else p.equipment_strides[gear]
			var stride: float = strides.get("walk-"+direction,strides.get("walk",0.12))
			var tex = p.frame("walk", direction, 0.75, Vector2(stride*0.5,0), gear)
			check(is_equal_approx(p.phase,p.cycle_seconds("walk-"+direction,gear)*0.5), "distance phase " + direction + gear)
			var saved: Dictionary = p.snapshot()
			check(p.frame("walk",direction,0.75,Vector2(stride*0.5,0),gear)==tex and p.snapshot()==saved,"pause retains phase")
			p.frame("walk", direction, 0.8, Vector2(8,8), gear)
			check(p.phase==0.0,"teleport resets gait")
			p.restore_snapshot(saved)
			check(p.snapshot()==saved,"playback snapshot round trip")
			p.frame("idle",direction,1.0,Vector2(stride*0.5,0),gear)
			check(p.phase==0.0,"walk to idle resets")
	p.current_key = ""
	p.frame("walk","east",0.0,Vector2.ZERO)
	p.frame("walk","east",0.75,Vector2(0.08984375,0))
	# Cycle length and stride come from the art, so compare the fraction itself.
	var fraction: float = p.phase/p.cycle_seconds("walk-east","")
	p.frame("walk","north",0.75,Vector2(0.08984375,0))
	check(fraction>0.0 and fraction<1.0 and is_equal_approx(p.phase/p.cycle_seconds("walk-north",""),fraction),"direction change preserves gait fraction")
	grid.free()
	print("VELD WALK INTEGRATION: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
