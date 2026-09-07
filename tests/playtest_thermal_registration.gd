extends SceneTree
const View = preload("res://rooms/underwater/thermal-control/solar_array_view.gd")
const Geometry = preload("res://tools/modular_room_geometry.gd")
var failures: Array[String] = []
class Sheet extends Node2D:
	var views: Array = []
	func _draw() -> void:
		for q in range(4):
			views[q].render_into(self,Vector2(220+(q%2)*440,220+(q/2)*440),1.0)
func _init() -> void: call_deferred("run")
func check(ok: bool, label: String) -> void:
	if not ok: failures.append(label)
func run() -> void:
	root.size=Vector2i(880,880)
	root.content_scale_size=Vector2i(880,880)
	var sheet := Sheet.new()
	for q in range(4):
		var view=View.new()
		view.embedded=true
		root.add_child(view)
		view.configure_embedded(q,[posmod(2+q,4),posmod(3+q,4)],false,0.0)
		sheet.views.append(view)
		for side in range(4):
			check(Geometry.has_port(view.layout[0],side)==([2,3].has(posmod(side-q,4))),"canonical corner q%d side%d"%[q,side])
		for prop in view.props:
			check(Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),"visual bounds "+str(prop.id))
			for other in view.props:
				if prop.id!=other.id: check(not prop.rect.intersects(other.rect),"overlapping footprint")
			for step in range(90):
				for mark in view.effect_marks(prop,step/30.0):
					for p in mark:
						check(Geometry2D.is_point_in_polygon(p,PackedVector2Array(prop.registration.outline)),"effect outside source host")
		for port in [2,3]:
			for step in range(91):
				check(view.can_stand(Geometry.turn(Vector2(0,-step*2.0),port+q)),"blocked corner aisle")
	for q in range(4): sheet.views[q].configure_embedded(q,[],false,0.0)
	root.add_child(sheet)
	await process_frame
	await RenderingServer.frame_post_draw
	var output := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): output=arg.trim_prefix("--output=")
	if not output.is_empty():
		check(root.get_texture().get_image().save_png(output)==OK,"save native sheet")
	if failures.is_empty(): print("THERMAL REGISTRATION PASS: four corner rotations, visual bounds, footprints, 728 aisle samples and source effects; isolated pilot only")
	else:
		for failure in failures: printerr(failure)
	quit(0 if failures.is_empty() else 1)
