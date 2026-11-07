extends SceneTree
const View=preload("res://rooms/underwater/batch-two/holographic_core_view.gd")
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
	var source: Image=view.life_texture.get_image()
	var missing_lens_pixels:=0
	var lens_pixels:=0
	var lens_quads: Array=view.projector_status_lens_quads()
	if "--negative-missing-status-lenses" in OS.get_cmdline_user_args(): lens_quads=[]
	for region in [Rect2i(170,155,25,18),Rect2i(420,155,26,18),Rect2i(174,351,22,25),Rect2i(418,351,22,26)]:
		for y in range(region.position.y,region.end.y):
			for x in range(region.position.x,region.end.x):
				var color:=source.get_pixel(x,y)
				# Frozen-source bright cyan lens cores, not a general recolour rule.
				if color.g<=85.0/255 or color.b<=85.0/255 or color.g<=color.r*1.35: continue
				lens_pixels+=1
				var covered:=false
				for quad in lens_quads:
					if Geometry2D.is_point_in_polygon(Vector2(x+0.5,y+0.5),PackedVector2Array(quad)): covered=true
				if not covered: missing_lens_pixels+=1
	check(lens_pixels>0 and missing_lens_pixels==0,"Status-lens mask covers all frozen-source bright cores: missing %d of %d"%[missing_lens_pixels,lens_pixels])
	var samples:=0
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		check(view.layout[0].kind==2,"Holo four-port layout")
		for prop in view.props:
			if prop.id=="holo_calibrator":
				for point in [Vector2(280,790),Vector2(332,795)]:
					check(not Geometry2D.is_point_in_polygon(point,PackedVector2Array(prop.registration.outline)),"Calibrator source floor above beam excluded")
				for point in [Vector2(282,802),Vector2(310,802)]:
					check(Geometry2D.is_point_in_polygon(point,PackedVector2Array(prop.registration.outline)),"Calibrator beam and optical plate retained")
			if prop.id=="holo_projector":
				for quad in view.projector_status_lens_quads():
					for point in quad: check(Geometry2D.is_point_in_polygon(point,PackedVector2Array(prop.registration.outline)),"Status-lens mask stays on projector")
				for quad in view.projector_lens_quads():
					check(not Geometry2D.is_point_in_polygon(Vector2(308,252),PackedVector2Array(quad)),"Ring cover preserves lens centre")
					for point in quad: check(Geometry2D.is_point_in_polygon(point,PackedVector2Array(prop.registration.outline)),"Ring cover stays on projector")
			check(Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),"Holo complete silhouette fits: "+str(prop.id))
			# Host art must not collide; a parked dressing cart's bounding box may
			# graze a host without any art collision, so compare hosts only.
			for other in view.props:
				if other.id!=prop.id and not prop.registration.get("dressing",false) and not other.registration.get("dressing",false):
					check(not view.prop_visual_bounds(prop).intersects(view.prop_visual_bounds(other)),"Holo hosts overlap")
			for t in range(180):
				for mark in view.effect_marks(prop,t/30.0):
					for point in mark:
						check(view.effect_region(prop).has_point(point),"Holo effect envelope: "+str(prop.id))
						check(Geometry2D.is_point_in_polygon(point,PackedVector2Array(prop.registration.outline)),"Holo effect on host")
						samples+=1
	view.free()
	if not failed: print("HOLO REGISTRATION PASS: four rotations, full bounds/non-overlap, ",samples," effect samples; native and perimeter traversal checks separate")
	quit(1 if failed else 0)
