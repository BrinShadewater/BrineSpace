extends SceneTree
const View=preload("res://rooms/underwater/batch-two/med_office_view.gd")
var failed:=false
func _init() -> void: call_deferred("run")
func check(ok: bool,message: String) -> void:
	if not ok:
		failed=true
		push_error(message)
func run() -> void:
	var view:=View.new()
	view.embedded=true
	root.add_child(view)
	var samples:=0
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		check(view.layout[0].kind==1,"Medical Office NS layout")
		for prop in view.props:
			check(Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),"Complete medical assembly fits")
			for other in view.props:
				if other.id!=prop.id: check(not view.prop_visual_bounds(prop).intersects(view.prop_visual_bounds(other)),"Medical assemblies overlap")
			for piece in prop.registration.get("pieces",[prop.registration.outline]):
				for point in piece: check(Rect2(-180,-180,360,360).has_point(view.life_point(prop,point)),"Rendered piece stays within hull")
			for step in range(180):
				var marks: Array=view.effect_marks(prop,step/30.0)
				check(not marks.is_empty() if view.is_animated_prop(prop) else marks.is_empty(),"Per-host activity expectation")
				for mark in marks:
					for point in mark:
						check(view.effect_region(prop).has_point(point),"Medical effect on display surface")
						var on_piece:=false
						for piece in prop.registration.get("pieces",[prop.registration.outline]): on_piece=on_piece or Geometry2D.is_point_in_polygon(point,PackedVector2Array(piece))
						check(on_piece,"Medical effect on rendered piece, not gap")
						samples+=1
	view.free()
	if not failed: print("MED OFFICE REGISTRATION PASS: four rotations, full bounds/pieces, static furnishings and ",samples," display-effect samples")
	quit(1 if failed else 0)
