extends SceneTree
## --layouts=res://... --defaults=res://... --rooms=crew_hab,maintenance_bay,bio_lab --out=res://output/...
## Reads layouts only; never opens player saves or writes Studio preferences.
const Store = preload("res://scripts/room_layout_store.gd")
const Actor = preload("res://scripts/room_scale_preview.gd")
const Baker = preload("res://tools/bake_current_architecture_cards.gd")
const Activity = preload("res://scripts/crew_room_activity.gd")
var failures: Array[String] = []
var visual_overlaps: Array[String] = []

func _init() -> void: call_deferred("run")

func check(ok: bool, message: String) -> void:
	if not ok:
		failures.append(message)
		push_error(message)

func door_route(actor, at: Vector2) -> PackedVector2Array:
	if not actor.can_stand(at): return PackedVector2Array()
	var start: int = actor.graph.get_closest_point(actor.foot)
	if start < 0 or not actor.segment_clear(actor.foot, actor.graph.get_point_position(start)):
		return PackedVector2Array()
	for target in actor.graph.get_point_ids():
		var point: Vector2 = actor.graph.get_point_position(target)
		if point.distance_to(at) > 24.0 or not actor.segment_clear(point, at): continue
		var route: PackedVector2Array = actor.graph.get_point_path(start,target)
		if not route.is_empty():
			route.insert(0,actor.foot)
			route.append(at)
			return route
	return PackedVector2Array()

func run() -> void:
	if DisplayServer.get_name() == "headless":
		print("Native rendering required")
		quit(2)
		return
	var layout_file := ""
	var strict_visual_overlap := false
	var out := "res://output/room-composition-review"
	var selected := PackedStringArray(["crew_hab", "maintenance_bay", "bio_lab"])
	for arg in OS.get_cmdline_user_args():
		if arg == "--strict-visual-overlap": strict_visual_overlap = true
		if arg.begins_with("--layouts="): layout_file = arg.trim_prefix("--layouts=")
		if arg.begins_with("--defaults="): Store.defaults_path = arg.trim_prefix("--defaults=")
		if arg.begins_with("--out="): out = arg.trim_prefix("--out=").trim_suffix("/")
		if arg.begins_with("--rooms="): selected = arg.trim_prefix("--rooms=").split(",")
	Store.loaded = true
	Store.data = {}
	if not layout_file.is_empty():
		var parsed = JSON.parse_string(FileAccess.get_file_as_string(layout_file))
		if not parsed is Dictionary or parsed.get("version") != 1 or not parsed.get("layouts") is Dictionary:
			push_error("Invalid layout input")
			quit(1)
			return
		Store.data = parsed.layouts
	Store.prime()
	root.size = Vector2i(512, 512)
	root.content_scale_size = root.size
	root.transparent_bg = true
	DirAccess.make_dir_recursive_absolute(out)
	var catalog: Array = JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json"))
	var report: Array = []
	var samples := 0
	for id in selected:
		var matches := catalog.filter(func(entry): return entry.room == id)
		if matches.is_empty():
			check(false, "Unknown room: " + id)
			continue
		var room = load(matches[0].view).new()
		if "room_id" in room: room.room_id = id
		room.embedded = true
		room.hide()
		root.add_child(room)
		var preview = Baker.Preview.new()
		preview.compact = true
		preview.id = id
		preview.room = room
		preview.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		preview.scale_actor = Actor.new()
		preview.scale_actor.load_art()
		preview.scale_actor.mode = 1
		preview.scale_actor.foot = Vector2(0,64)
		root.add_child(preview)
		for q in range(4):
			preview.q = q
			preview.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var label := "%s q%d" % [id,q]
			var actor = preview.scale_actor
			var props: Array = []
			var ports: Array = []
			var door_routes: Array = []
			check(actor.visible, label + ": no space for crew")
			for prop in room.props:
				var bounds: Rect2 = room.prop_visual_bounds(prop)
				# The Airlock's code-owned exterior hatch straddles its hull threshold.
				var envelope := Rect2(-200,-200,400,400) if id=="airlock" and prop.id=="outer_hatch" else Rect2(-192,-250,384,442)
				check(envelope.encloses(bounds), label + ": art outside room: " + str(prop.id))
				for other in props:
					if bounds.intersects(other.bounds):
						var overlap: String = label + ": visual overlap: " + str(prop.id) + " / " + str(other.id)
						visual_overlaps.append(overlap)
						if strict_visual_overlap: check(false, overlap)
				props.append({"id":str(prop.id), "bounds":bounds})
			for side in range(4):
				if not room.Geometry.has_port(room.layout[0],side): continue
				ports.append(side)
				var at: Vector2 = [Vector2(0,-168),Vector2(168,0),Vector2(0,168),Vector2(-168,0)][side]
				var route := door_route(actor,at)
				var blocking_props: Array = []
				for prop in room.props:
					for rect in actor.Geometry.prop_collision_rects(prop):
						if rect.grow(10.0).has_point(at):
							blocking_props.append({"id":str(prop.id),"collision_rect":rect,"crew_clearance":10.0})
				door_routes.append({"side":side,"direct_from_center":actor.segment_clear(Vector2.ZERO,at),"route":route,"endpoint_clear":actor.can_stand(at),"blocking_props":blocking_props})
				check(not route.is_empty(), label + ": unreachable door approach in preview graph " + str(side))
			if id == "crew_hab":
				var stations := Activity.stations({"activity_room":id,"props":room.props})
				check(stations.any(func(station): return station.get("mode", "")=="sleep" and station.has("rest_point")), label + ": no functional sleeping berth")
				for station in stations:
					check(actor.can_stand(station.point), label + ": blocked berth approach")
					var start: int = actor.graph.get_closest_point(Vector2.ZERO)
					var target: int = actor.graph.get_closest_point(station.point)
					check(start >= 0 and target >= 0 and not actor.graph.get_point_path(start,target).is_empty(), label + ": unreachable berth")
			var image := root.get_texture().get_image()
			check(image.save_png(out + "/%s-q%d.png" % [id,q]) == OK, label + ": capture failed")
			actor.mode = 2
			var distance := 0.0
			for step in range(160):
				var before: Vector2 = actor.foot
				actor.advance(0.1)
				check(actor.segment_clear(before,actor.foot), label + ": walking through equipment")
				distance += before.distance_to(actor.foot)
				samples += 1
			check(distance > 40.0, label + ": crew did not traverse room")
			actor.mode = 1
			actor.moving = false
			actor.foot = Vector2(0,64)
			report.append({"room":id,"quarter":q,"ports":ports,"door_routes":door_routes,"props":props,"walking_distance":distance})
		preview.queue_free()
		room.queue_free()
		await process_frame
	var file := FileAccess.open(out + "/review.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"views":report,"walking_samples":samples,"visual_overlaps":visual_overlaps,"strict_visual_overlap":strict_visual_overlap,"failures":failures},"\t"))
	file.close()
	print("ROOM COMPOSITION: %d views, %d walking samples, %d failures" % [report.size(),samples,failures.size()])
	quit(0 if failures.is_empty() else 1)
