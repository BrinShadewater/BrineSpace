extends SceneTree

const Grid = preload("res://scripts/grid_canvas.gd")
var failures := 0

func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	var grid = Grid.new()
	grid._load_major_bill_animations()
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/major-bill-v2/final/manifest.json"))
	var sprite_frames: SpriteFrames = load("res://character/major-bill-v2/final/major-bill.tres")
	check(sprite_frames != null, "SpriteFrames imports")
	for state in ["idle", "walk", "run"]:
		for direction in ["north", "east", "south", "west"]:
			check(grid.human_animations[state].has(direction), "Missing " + state + "/" + direction)
	for entry: Dictionary in manifest.states:
		var key := str(entry.id)
		var split := key.find("-")
		var frames: Array = grid.human_animations[key.substr(0, split)][key.substr(split + 1)]
		check(frames.size() == int(entry.frameCount), key + " count")
		var elapsed := 0.0
		for i in range(frames.size()):
			check(frames[i].get_size() == Vector2(92, 92), key + " canvas")
			check(frames[i].get_meta("major_bill_v2", false), key + " renderer geometry tag")
			var milliseconds := float(entry.frameDurationsMs[i])
			check(grid._human_frame_index(key, (elapsed + milliseconds * 0.5) / 1000.0) == i, key + " duration selection")
			if sprite_frames != null:
				check(is_equal_approx(sprite_frames.get_frame_duration(key, i) / sprite_frames.get_animation_speed(key), milliseconds / 1000.0), key + " native timing")
			elapsed += milliseconds
		check(grid._human_frame_index(key, elapsed / 1000.0 + 0.001) == (0 if entry.loop else 5), key + " loop/clamp")
		if sprite_frames != null:
			check(sprite_frames.get_animation_loop(key) == bool(entry.loop), key + " native loop")
	for pair in [["idle",0,"kneel",0],["kneel",5,"repair",0],["repair",5,"stand",0],["stand",5,"idle",0]]:
		var first: Texture2D = grid.human_animations[pair[0]]["east"][pair[1]]
		var last: Texture2D = grid.human_animations[pair[2]]["east"][pair[3]]
		check(first.get_image().get_data() == last.get_image().get_data(), "Repair transition endpoint continuity")
	grid._advance_human_animation("walk-south",10.0,Vector2.ZERO)
	var fast: float = grid._advance_human_animation("walk-south",10.1,Vector2(0,0.03))
	grid._advance_human_animation("walk-south",0.0,Vector2.ZERO)
	var slow: float = grid._advance_human_animation("walk-south",0.8,Vector2(0,0.03))
	check(is_equal_approx(fast,slow), "Equal travel distance gives equal gait phase regardless of speed")
	check(is_equal_approx(grid._advance_human_animation("walk-south",1.2,Vector2(0,0.03)),slow), "Stationary walking cannot moonwalk")
	check(is_equal_approx(grid._advance_human_animation("walk-south",1.2,Vector2(0,0.04)),slow), "Paused clock cannot advance gait")
	check(grid._advance_human_animation("walk-south",2.0,Vector2(0,2.0))==0.0, "Teleport resets instead of racing through frames")
	check(grid._advance_human_animation("run-south",2.1,Vector2(0,2.01))==0.0, "State change resets distance clock")
	grid.free()
	print("MAJOR BILL: 17 animations / 102 frames; coverage, timing, transitions, native SpriteFrames: %d failures" % failures)
	quit(1 if failures else 0)
