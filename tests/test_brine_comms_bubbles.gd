extends SceneTree

func _init() -> void:
	call_deferred("run")

func run() -> void:
	var effect = load("res://scripts/brine_comms_bubbles.gd").new()
	root.add_child(effect)
	assert(not effect.glass_at(Vector2(.5,.4)), "Face must occlude bubbles")
	assert(not effect.glass_at(Vector2(.5,.9)), "Suit must occlude bubbles")
	assert(effect.glass_at(Vector2(.10,.4)), "Side glass admits bubbles")
	assert(not effect.glass_at(Vector2(.26,.45)), "Swept-back hair occludes bubbles")
	assert(not effect.cropped_glass_at(Vector2(.26,.40)), "Portrait framing preserves hair occlusion")
	assert(effect.cropped_glass_at(Vector2(.05,.10)), "Upper glass remains visible in closer framing")
	effect.advance(2.5)
	assert(is_equal_approx(effect.elapsed,2.5))
	print("BRINE BUBBLES PASS: glass bounds, foreground occlusion and animation clock")
	quit()
