extends SceneTree
const Art = preload("res://rooms/underwater/corridor_surfaces.gd")
const Geometry = preload("res://rooms/underwater/corridor_geometry.gd")
func _init() -> void:
	var samples := 0
	for corner in [false,true]:
		var parts:=Art.detail_parts(corner)
		if "--negative-bound-control" in OS.get_cmdline_user_args():
			parts.append({"rect":Rect2(170,100,10,10)})
		for part in parts:
			var r: Rect2 = part.rect
			# Sample interior corners: polygon edges are valid construction bounds.
			var inset := r.grow(-0.01)
			for p in [inset.position,Vector2(inset.end.x,inset.position.y),inset.end,Vector2(inset.position.x,inset.end.y)]:
				if not Geometry2D.is_point_in_polygon(p,Geometry.hull_for(corner)) or absf(p.x)>=160 or absf(p.y)>=160:
					push_error("Routing detail outside hull or inside doorway approach: corner=%s rect=%s point=%s"%[corner,r,p])
					quit(1)
					return
				samples+=1
	print("CORRIDOR DETAIL PASS: %d fitting corners inside hull and clear of socket approaches"%samples)
	quit()
