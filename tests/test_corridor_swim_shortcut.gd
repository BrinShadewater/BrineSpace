extends SceneTree
## A cold swim search spent 508 of 830 ms sampling corridor floor (Sept 26 spike probe):
## each corridor link tested a 9x5 grid of lines, 16 outline points per sample. When the
## padded swept body lies inside a rectangle that sits inside the floor outline, every
## sample passes, so the link is clear without sampling. This must never change an answer.
const Corridor = preload("res://rooms/underwater/corridor_geometry.gd")
const Geometry = preload("res://tools/modular_room_geometry.gd")
var failures := 0

func _init(): call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)

func run() -> void:
	# 1. Every inner rectangle lies strictly inside its outline (dense sampling, edges included).
	for shape in [[false,false],[true,false],[false,true]]:
		var outline := Corridor.floor_for(shape[0], shape[1])
		for rect in Corridor.inner_for(shape[0], shape[1]):
			var outside := 0
			for i in range(81):
				for j in range(81):
					var point: Vector2 = rect.position + rect.size * Vector2(i/80.0, j/80.0)
					if not Geometry2D.is_point_in_polygon(point, outline): outside += 1
			check(outside == 0, "Inner rect %s of shape %s lies inside the floor outline" % [rect, shape])
	# 2. The shortcut answers exactly like full sampling for every rotation and many swept boxes.
	var rng := RandomNumberGenerator.new()
	rng.seed = 26
	var agreed := 0
	var shortcuts := 0
	for id in ["corridor","corner","tee_corridor"]:
		for rotation in range(4):
			var room := {"id": id, "rotation": rotation}
			for trial in range(400):
				var center := Vector2(rng.randf_range(-200,200), rng.randf_range(-200,200))
				var box := Rect2(center, Vector2(rng.randf_range(4,60), rng.randf_range(4,90)))
				var fast := Corridor.encloses_foot_area(room, box, 10.0)
				if not fast: continue
				shortcuts += 1
				# Full sampling over the box: any point inside must be standable floor.
				var every := true
				for i in range(9):
					for j in range(9):
						if not Corridor.contains_foot(room, box.position + box.size*Vector2(i/8.0, j/8.0), 10.0): every = false
				check(every, "Shortcut only accepts boxes whose every foot sample is floor (%s r%d %s)" % [id, rotation, box])
				if every: agreed += 1
	check(shortcuts > 200, "Shortcut applies to ordinary corridor interiors (%d)" % shortcuts)
	print("CORRIDOR SWIM SHORTCUT shortcuts=", shortcuts, " agreed=", agreed, " failures=", failures)
	quit(0 if failures == 0 else 1)
