extends SceneTree
const View=preload("res://rooms/underwater/batch-two/bio_lab_view.gd")
var failures: Array[String]=[]
func _init() -> void: call_deferred("run")
func check(value: bool,message: String) -> void:
	if not value: failures.append(message)
func run() -> void:
	var view:=View.new()
	view.embedded=true
	root.add_child(view)
	var effect_samples:=0
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		check(view.layout[0].kind==0,"Bio tee kind")
		check(view.props.size()==4,"Four complete Bio assemblies")
		for prop in view.props:
			check(Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),"Full bounds: "+str(prop.id))
			for other in view.props:
				if other.id!=prop.id: check(not view.prop_visual_bounds(prop).intersects(view.prop_visual_bounds(other)),"Overlapping hosts")
			for region in view.display_regions(prop):
				for point in [region.position,region.end,Vector2(region.position.x,region.end.y),Vector2(region.end.x,region.position.y)]:
					check(Geometry2D.is_point_in_polygon(point,PackedVector2Array(prop.registration.outline)),"Display in source outline")
			for sample in range(180):
				for mark in view.effect_marks(prop,sample/30.0):
					for point in mark:
						var in_surface:=false
						for surface in view.effect_surfaces(prop): in_surface=in_surface or surface.has_point(point)
						check(in_surface,"Effect on a real surface, not the gap between vessels")
						check(view.effect_region(prop).has_point(point),"Operating effect within working surface: "+str(prop.id))
						check(Geometry2D.is_point_in_polygon(point,PackedVector2Array(prop.registration.outline)),"Operating effect inside source host")
						effect_samples+=1
	view.free()
	if not failures.is_empty():
		for failure in failures.slice(0,20): push_error(failure)
		quit(1)
		return
	print("BIO REGISTRATION PASS: four rotations, full host bounds/non-overlap, display apertures, ",effect_samples," effect points; station/economy acceptance separate")
	quit()
