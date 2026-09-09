extends SceneTree
const Geometry=preload("res://rooms/underwater/corridor_geometry.gd")
func _init() -> void:
	var samples:=0
	for id in ["corridor","corner","tee_corridor"]:
		for q in range(4):
			var room: Dictionary={"id":id,"rotation":q}
			var hull:=PackedVector2Array()
			for point in Geometry.hull_for(id=="corner",id=="tee_corridor"): hull.append(Geometry.G.turn(point,Geometry.rotation(room)))
			var edges:=Geometry.foundation_edges(room)
			assert(not edges.is_empty())
			for edge in edges:
				var midpoint:=Vector2(edge.get_center().x,edge.position.y)
				assert(Geometry2D.is_point_in_polygon(midpoint+Vector2(0,-0.1),hull),"Support sits under hull")
				assert(not Geometry2D.is_point_in_polygon(midpoint+Vector2(0,0.1),hull),"Support follows exposed south edge")
				samples+=1
			for edge in Geometry.foundation_edges(room,true): assert(edge.position.y<191.9,"Connected southern mouth has no duplicate base")
	var horizontal:=Geometry.foundation_edges({"id":"corridor","rotation":1})
	assert(is_equal_approx(horizontal[0].position.y,64.0),"Horizontal corridor base follows hull, not cell bottom")
	print("CORRIDOR FOUNDATION PASS: ",samples," hull faces across straight, bend and tee rotations")
	quit()
