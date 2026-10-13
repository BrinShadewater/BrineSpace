extends SceneTree
const Common=preload("res://rooms/large-rooms/common.gd")
var failures:=0
func check(ok: bool,message: String):
	if not ok:failures+=1;push_error(message)
func area(points: PackedVector2Array) -> float:
	var value:=0.0
	for i in range(points.size()):value+=points[i].cross(points[(i+1)%points.size()])
	return absf(value)*.5
func _initialize():
	for size in [Vector2(408,408),Vector2(328,156),Vector2(60,174)]:
		var points:=PackedVector2Array([-size*.5,Vector2(size.x,-size.y)*.5,size*.5,Vector2(-size.x,size.y)*.5])
		for q in range(4):
			var angle:=float(q)*PI*.5
			var bottom: float=-INF
			for point in points:bottom=maxf(bottom,point.rotated(angle).y)
			for water in [.25,.65,1.0]:
				var line: float=bottom-float(water)*76.0
				var dry:=Common.water_clip(points,line,angle,false)
				var wet:=Common.water_clip(points,line,angle,true)
				check(is_equal_approx(area(dry)+area(wet),size.x*size.y),"Clipped art has no gap or duplicate area")
				for point in dry:check(point.rotated(angle).y<=line+.001,"Exposed source stays above the horizontal waterline")
				for point in wet:check(point.rotated(angle).y>=line-.001,"Submerged source stays below the horizontal waterline")
	print("LARGE WATERLINE GEOMETRY: %d failures"%failures)
	quit(failures)
