extends SceneTree
const Floor=preload("res://rooms/whole-room/modular_floor.gd")
class FinishHost extends RefCounted:
	var comparing:=false
	var draft: Dictionary={"prop/example":[10,20]}
	var defaults: Dictionary={}
	var history: Array=[]
	var future: Array=[]
	var dirty:=false
	func refresh() -> void: pass
func _init() -> void:
	assert(Floor.hall_module(Vector2(-60,-12),"corridor")==Floor.hall_module(Vector2(-60,12),"corridor"),"Symmetric lanes meet flipped neighboring sockets")
	assert(Floor.hall_module(Vector2(-60,-36),"corridor").tile==Vector2(6,0))
	assert(Floor.hall_module(Vector2(36,60),"corner").tile==Vector2(5,1))
	assert(Floor.hall_module(Vector2(-60,-12),"corridor").turn==1)
	assert(Floor.hall_module(Vector2(-12,60),"corner").turn==0)
	assert(Floor.hall_module(Vector2(12,-12),"corner").tile==Vector2(0,0))
	assert(Floor.hall_module(Vector2(-12,-12),"tee_corridor").tile==Vector2(0,0))
	var patterns: Array=[]
	for shape in ["corridor","corner","tee_corridor"]:
		for v in range(3):
			var fingerprint=hash(Floor.meshes({},true,0,1.0,"",shape,v)[0].mesh.surface_get_arrays(0)[Mesh.ARRAY_TEX_UV])
			assert(not fingerprint in patterns,"Nine floor layouts have unique UV arrangements")
			patterns.append(fingerprint)
	var dressing=preload("res://rooms/underwater/corridor_dressing.gd")
	var geometry=preload("res://rooms/underwater/corridor_geometry.gd")
	assert(dressing.side_return_top(geometry.junction_hull,0,6)==64)
	assert(dressing.side_return_top(geometry.junction_hull,0,10)==64)
	var uid="res://tests/test_hallway_floor_tiles.gd.uid"
	if not FileAccess.file_exists(uid):
		var f=FileAccess.open(uid,FileAccess.WRITE)
		f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	for shape in ["corridor","corner","tee_corridor"]:
		for q in range(4):
			var batches=Floor.meshes({},true,q,1.0,"",shape)
			assert(batches.size()==1 and batches[0].texture==Floor.texture(Floor.HALL_TILES))
			var a=batches[0].mesh.surface_get_arrays(0)
			var vertices=a[Mesh.ARRAY_VERTEX]
			var indices=a[Mesh.ARRAY_INDEX]
			var area:=0.0
			for i in range(0,indices.size(),3):
				var x: Vector3=vertices[indices[i]]
				var y: Vector3=vertices[indices[i+1]]
				var z: Vector3=vertices[indices[i+2]]
				area+=(y-x).cross(z-x).length()*.5
			var p=Floor.footprint(true,q,shape)
			var expected:=0.0
			for i in range(p.size()):expected+=p[i].cross(p[(i+1)%p.size()])*.5
			assert(absf(area-absf(expected))<.1,"Tiles cover the complete clipped footprint")
			for uv in a[Mesh.ARRAY_TEX_UV]:assert(uv.x>=0 and uv.y>=0 and uv.x<=1 and uv.y<=1)
	var original=Floor.meshes({"floor/finish":Floor.DECK},true)
	assert(original[0].texture==Floor.texture(Floor.DECK),"Explicit saved finish preserved")
	var first=Floor.meshes({},true)[0].mesh.surface_get_arrays(0)[Mesh.ARRAY_TEX_UV]
	var edited=Floor.meshes({"tile/3/3":[0,0]},true)[0].mesh.surface_get_arrays(0)[Mesh.ARRAY_TEX_UV]
	assert(first!=edited,"Tile editing selects an atlas tile")
	var host=FinishHost.new()
	var selector=preload("res://scripts/floor_finish_tools.gd").new()
	selector.setup(host)
	var choice=selector.paths.find(Floor.HALL_TILES)
	assert(choice>0,"Current finish selector includes the new atlas")
	selector.apply_finish(choice)
	assert(host.draft["floor/finish"]==Floor.HALL_TILES and host.draft.has("prop/example"))
	assert(host.dirty and host.history.size()==1 and not host.history[0].has("floor/finish"))
	selector.free()
	print("HALLWAY FLOOR PASS: 12 complete clipped footprints, bounded atlas UVs, saved finish, tile editing and current finish selector")
	quit()
