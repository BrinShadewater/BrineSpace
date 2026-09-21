extends SceneTree
## What the Layout Studio does not check, checked. Free placement is the Studio's default
## and issues() returns nothing in that mode, so a prop can be saved standing in a
## doorway, on top of another prop, or off the hull, and nothing says so until crew stop
## being able to walk somewhere. Five doorways were blocked this way before anyone noticed.
##
##   godot --headless --path . -s res://tools/lint_room_layouts.gd
##   godot --headless --path . -s res://tools/lint_room_layouts.gd -- --rooms=research_lab,med_bay
##   godot --headless --path . -s res://tools/lint_room_layouts.gd -- --out=res://output/layout-lint.json
##
## Exits 1 if anything is reported. Reads the owner's layout store; never writes it.
const Geometry = preload("res://tools/modular_room_geometry.gd")
const DOOR_REACH := 176.0   # where bill_npc.gd puts a door's navigation node
const PAD := 10.0           # the padding bill_npc.gd grows every blocker by
const OVERLAP_FLOOR := 400.0 # smaller than this is props touching, which the owner does on purpose
const HULL_SLACK := 8.0     # a prop may sit flush to the wall without being "past" it

var game
var findings: Array = []

func _init() -> void: call_deferred("run")

func note(room: String, q: int, kind: String, detail: String) -> void:
	findings.append({"room": room, "rotation": q, "kind": kind, "detail": detail})
	print("LINT %-22s q%d  %-14s %s" % [room, q, kind, detail])

func run() -> void:
	var only: Array = []
	var out_path := "res://output/layout-lint.json"
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--rooms="): only = Array(argument.trim_prefix("--rooms=").split(","))
		if argument.begins_with("--out="): out_path = argument.trim_prefix("--out=")
	preload("res://scripts/title_settings.gd").save_path = "user://layout_lint_%d.cfg" % OS.get_process_id()
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://layout_lint_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://layout_lint_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game.set_process(false)
	game.tick_timer.stop()
	var checked := 0
	for room_id in game.RoomDatabaseScript.all_rooms():
		if not only.is_empty() and room_id not in only: continue
		for q in range(4):
			var room: Dictionary = game.RoomDatabaseScript.get_room(room_id).duplicate(true)
			if room.has("fixed_rotation") and q != int(room.fixed_rotation): continue
			room.pos = Vector2i(20, 20)
			room.rotation = q
			var view = game.grid_view._bill_room_view(room)
			if view == null or not view.has_method("configure_embedded"): continue
			view.configure_embedded(q, [0, 1, 2, 3], true, 1.0, [])
			if view.layout.is_empty(): continue
			checked += 1
			# Collision rectangles exactly as the navigation graph builds them.
			var solids: Array = []
			for prop in view.props:
				# A wall bank is mounted ON the wall and reaches past the interior by
				# design, and props legitimately stand in front of one, so it is a
				# backdrop for these two checks rather than a thing on the floor.
				var backdrop: bool = str(prop.id).begins_with("full_wall_") \
					or prop.get("wall_mount", false) \
					or prop.get("registration", {}).get("wall_mount", false)
				for rect in Geometry.prop_collision_rects(prop):
					solids.append({"id": str(prop.id), "rect": rect, "backdrop": backdrop})
			for side in range(4):
				if not Geometry.has_port(view.layout[0], side): continue
				var node := Vector2(Geometry.DIRS[side]) * DOOR_REACH
				for solid in solids:
					if not (solid.rect as Rect2).grow(PAD).has_point(node): continue
					note(room_id, q, "blocked-door",
						"%s stands on the door %d node %s (its floor is %s)" % [solid.id, side, node, solid.rect])
			for i in range(solids.size()):
				for j in range(i + 1, solids.size()):
					if solids[i].id == solids[j].id: continue
					if solids[i].backdrop or solids[j].backdrop: continue
					var overlap: Rect2 = (solids[i].rect as Rect2).intersection(solids[j].rect)
					# The owner's props touch on purpose - 63% sit within 8 units. Only a
					# real shared footprint is worth a word.
					if overlap.get_area() < OVERLAP_FLOOR: continue
					note(room_id, q, "overlap",
						"%s and %s share %d square units of floor" % [solids[i].id, solids[j].id, int(overlap.get_area())])
			for solid in solids:
				if solid.backdrop: continue
				var rect: Rect2 = solid.rect
				var out := maxf(maxf(-182.0 - rect.position.x, -186.0 - rect.position.y),
					maxf(rect.end.x - 182.0, rect.end.y - 178.0))
				if out <= HULL_SLACK: continue
				note(room_id, q, "off-hull", "%s stands %d units past the hull at %s" % [solid.id, int(out), rect])
	var by_kind := {}
	for finding in findings: by_kind[finding.kind] = int(by_kind.get(finding.kind, 0)) + 1
	var file := FileAccess.open(out_path, FileAccess.WRITE)
	if file != null:
		file.store_string(JSON.stringify({"checked_room_rotations": checked, "counts": by_kind, "findings": findings}, "\t"))
		file.close()
	print("LAYOUT LINT: %d room/rotations checked, %d findings %s" % [checked, findings.size(), JSON.stringify(by_kind)])
	quit(1 if not findings.is_empty() else 0)
