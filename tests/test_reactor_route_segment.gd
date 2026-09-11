extends SceneTree
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://reactor_segment_%d.meta"%OS.get_process_id()
	game.run_save_path="user://reactor_segment_%d.loop"%OS.get_process_id()
	game.Preferences.initialized=true
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	game.occupied.clear()
	game.placed_rooms.clear()
	for offset in [Vector2i.ZERO,Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
		var cell: Vector2i=Vector2i(20,20)+offset
		game._place_room("reactor" if offset==Vector2i.ZERO else "battery_array",cell,true)
		game.occupied[cell].rotation=1
	var npc=game.bill_npc
	npc.rebuild(game)
	var start:=Vector2(7872,7488)
	var stopped:=Vector2(7862.20654296875,7634.875)
	var target:=Vector2(7856,7728)
	var blockers:=[]
	for cell in npc.geometry:
		var bounds:=Rect2(Vector2(cell)*384,Vector2.ONE*384)
		for rect in npc.geometry[cell].blockers:
			var world: Rect2=Rect2(rect.position+bounds.get_center(),rect.size).intersection(bounds)
			if world.has_area() and npc.segment_hits_rect(stopped,target,world): blockers.append({"cell":str(cell),"rect":str(world)})
	print("REACTOR SEGMENT: ",JSON.stringify({"whole_clear":npc.segment_clear(start,target),"remainder_clear":npc.segment_clear(stopped,target),"start_standable":npc.can_stand(stopped),"blockers":blockers}))
	npc.foot=start
	var failures:=0
	# This fixture reproduced one grazing path from the pre-declutter reactor
	# layout. The Sept 9 declutter removed the grazed prop, so with no blocker
	# near the segment the tangent assertion no longer tests anything; the
	# general near-tangent rule stays covered by test_npc_segment_clearance.gd.
	if blockers.is_empty():
		print("REACTOR SEGMENT: tangent case not applicable to the current layout (no blocker near the segment)")
	elif npc.segment_clear(start,target):
		push_error("Near-tangent planning route must be rejected")
		failures+=1
	var start_id: int=npc.nearest_in_room(start,npc.cell_at(start))
	var target_id: int=npc.nearest_in_room(target,npc.cell_at(target))
	npc.path=npc.smooth_route(npc.graph.get_point_path(start_id,target_id))
	for i in range(100):
		if npc.path.is_empty(): break
		npc.move(0.1)
	print("REACTOR SEGMENT MOVEMENT: ",npc.foot," ",npc.activity," arrived=",npc.foot.is_equal_approx(target))
	if not npc.foot.is_equal_approx(target):
		push_error("Production route must reach the original target")
		failures+=1
	quit(1 if failures else 0)
