extends SceneTree
const View=preload("res://rooms/underwater/batch-two/biodome_view.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	var view:=View.new()
	view.embedded=true
	root.add_child(view)
	var failures: Array[String]=[]
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		for prop in view.props:
			if prop.id!="biodome_tree": continue
			var outline:=PackedVector2Array(prop.registration.outline)
			# Source-coordinate samples selected from the integer-zoom donor crop.
			for point in [Vector2(334,197),Vector2(339,199),Vector2(341,201)]:
				if Geometry2D.is_point_in_polygon(point,outline): failures.append("Source floor retained at "+str(point))
			for point in [Vector2(328,193),Vector2(336,206),Vector2(346,196),Vector2(452,350)]:
				if not Geometry2D.is_point_in_polygon(point,outline): failures.append("Leaf or planter rim lost at "+str(point))
			for sample in [[Vector2(323,227),false],[Vector2(324,230),false],[Vector2(334,230),false],[Vector2(335,234),false],[Vector2(330,228),true],[Vector2(339,234),true],[Vector2(330,256),true]]:
				var included:=false
				for polygon in view.render_polygons(prop): included=included or Geometry2D.is_point_in_polygon(sample[0],polygon)
				if included!=sample[1]: failures.append("Enclosed gap / retained leaf or branch: "+str(sample[0]))
	view.free()
	if not failures.is_empty():
		for failure in failures: push_error(failure)
		quit(1)
	else:
		print("BIODOME CANOPY PASS: seven excluded floor and seven retained leaf/rim/branch samples across four rotations; not exhaustive silhouette acceptance")
		quit()
