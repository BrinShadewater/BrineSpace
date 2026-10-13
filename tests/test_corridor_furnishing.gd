extends SceneTree
const G=preload("res://tools/modular_room_geometry.gd")
const C=preload("res://rooms/underwater/corridor_geometry.gd")
func _init():call_deferred("run")
func run():
	var grid=preload("res://scripts/grid_canvas.gd").new()
	var doors=preload("res://rooms/doors/department_door.gd")
	var checked:=0
	for id in ["corridor","corner","tee_corridor"]:
		for other in ["reactor","crew_hab","brine_core","airlock"]:
			assert(doors.pair_variant({"id":id},{"id":other})=="hallway")
			assert(doors.pair_variant({"id":other},{"id":id})=="hallway")
		for q in range(4):
			var room:Dictionary={"id":id,"rotation":q,"pos":Vector2i.ZERO}
			var data:Dictionary=grid.bill_room_geometry(room,[0,1,2,3])
			assert(data.props.size()>=2,"Corridor navigation sees the effective furniture")
			data.open=[0,1,2,3];data.blockers=[]
			var npc=preload("res://scripts/bill_npc.gd").new()
			for prop in data.props:
				for rect in G.prop_collision_rects(prop):
					data.blockers.append(rect.grow(10))
			npc.geometry={Vector2i.ZERO:data}
			for rect in data.blockers:
				assert(not npc.can_stand(Vector2(192,192)+rect.get_center()),"Furniture prevents standing inside it")
			var exits=preload("res://rooms/underwater/corridor_dressing.gd").corridor_exit_directions(C.hull_for(id=="corner",id=="tee_corridor"),C.rotation(room))
			var start:Vector2i=Vector2i(exits[0]*176)
			var seen:Dictionary={start:true}
			var queue:Array[Vector2i]=[start]
			var index:=0
			while index<queue.size():
				var at:Vector2i=queue[index];index+=1
				for offset in [Vector2i(16,0),Vector2i(-16,0),Vector2i(0,16),Vector2i(0,-16)]:
					var next:Vector2i=at+offset
					if seen.has(next) or absi(next.x)>176 or absi(next.y)>176:continue
					if npc.segment_clear(Vector2(at)+Vector2(192,192),Vector2(next)+Vector2(192,192)):
						seen[next]=true;queue.append(next)
			for exit in exits:
				if not seen.has(Vector2i(exit*176)):
					push_error("Blocked corridor route: %s q%d"%[id,q]);grid.free();quit(1);return
			checked+=1
	grid.free()
	print("CORRIDOR FURNISHING PASS: ",checked," rotations; all ports reachable around real prop blockers; hallway door precedence")
	quit()
