extends SceneTree
const Scene = preload("res://rooms/whole-room/nursery_south_facing.tscn")
const LifeView = preload("res://rooms/whole-room/life_support_view.gd")
const HydroView = preload("res://rooms/whole-room/hydroponics_view.gd")
var hydro := false
const ReactorView = preload("res://rooms/whole-room/reactor_view.gd")
var reactor := false
var failures := 0
var view
var OUT := "res://output/whole-room-pilot-01/south-facing"
var life := false
func _init() -> void:
	life = "--life" in OS.get_cmdline_user_args()
	hydro = "--hydro" in OS.get_cmdline_user_args()
	reactor = "--reactor" in OS.get_cmdline_user_args()
	if hydro or reactor: life = true
	if life: OUT = "res://output/whole-room-pilot-01/life-depth"
	if hydro: OUT = "res://output/whole-room-pilot-01/hydro-depth"
	if reactor: OUT = "res://output/whole-room-pilot-01/reactor-depth"
	call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures+=1
		push_error(message)
func snap(name: String) -> PackedByteArray:
	view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	img.save_png(OUT.path_join(name+".png"))
	return img.get_data()
func actor_region() -> PackedByteArray:
	var p: Vector2 = view.view_origin+view.actor*view.view_scale
	return root.get_texture().get_image().get_region(Rect2i(p-Vector2(45,80),Vector2(90,100))).get_data()
func actor_changes(name: String) -> int:
	view.show_actor = false
	await snap(name+"-background")
	var before := actor_region()
	view.show_actor = true
	await snap(name)
	var after := actor_region()
	var count := 0
	for i in range(before.size()):
		if before[i]!=after[i]: count+=1
	return count
func run() -> void:
	root.size = Vector2i(1600,900)
	root.content_scale_size = Vector2i(1600,900)
	view = HydroView.new() if hydro else (LifeView.new() if life else Scene.instantiate())
	if reactor:
		view.free()
		view = ReactorView.new()
	root.add_child(view)
	await process_frame
	view.set_process(false)
	# Automated motion/state owns this fixture; desktop keystrokes must not
	# toggle its pause/rotation while screenshots are being captured.
	view.set_process_unhandled_key_input(false)
	var out := OUT
	DirAccess.make_dir_recursive_absolute(out)
	for q in range(4):
		view.quarter = q
		view.rebuild()
		view.operating = true
		view.paused = false
		view.show_actor = true
		for prop in view.props:
			var src: Rect2 = prop.registration.rect if life else prop.registration.footprint
			var size: Vector2 = src.size if life else src.size*view.PIXEL_SCALE
			check(prop.rect.size.is_equal_approx(size),"Fixed-facing footprint size")
			var original_center: Vector2 = src.get_center() if life else view.pixel_to_world(src.get_center())
			var expected: Vector2 = view.Geometry.turn(original_center,q)
			check(prop.rect.get_center().distance_to(expected+prop.get("layout_adjustment",Vector2.ZERO))<0.001,"Rotated position plus wall-clearance adjustment")
			check(Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),"Full visible assembly inside walls q%d %s"%[q,prop.id])
			check(Rect2(-184,-184,368,368).encloses(prop.rect),"Prop footprint inside shell q%d %s"%[q,prop.id])
			var anchor: Vector2 = view.life_point(prop,prop.registration.pivot) if life else view.pixel_to_world(Vector2(src.get_center().x,prop.registration.sort_pixel))+prop.art_offset
			check(absf(anchor.y-prop.rect.end.y)<0.001,"Art and collision ground contact")
			var r: Rect2 = prop.rect
			var visible: Array[int] = []
			for front in [false,true]:
				view.actor = Vector2(r.get_center().x,r.end.y+9 if front else r.position.y-9)
				check(view.can_stand(view.actor),"Depth pose reachable")
				visible.append(await actor_changes("q%d-%s-%s"%[q,prop.id,"front" if front else "behind"]))
			check(visible[1]>0 and visible[0]<visible[1],"Depth q%d %s"%[q,prop.id])
			var side := r.end.x+10
			if not view.can_stand(Vector2(side,r.position.y-10)) or not view.can_stand(Vector2(side,r.end.y+10)): side = r.position.x-10
			var route := [Vector2(r.get_center().x,r.position.y-10),Vector2(side,r.position.y-10),Vector2(side,r.end.y+10),Vector2(r.get_center().x,r.end.y+10)]
			view.actor = route[0]
			for waypoint in route.slice(1):
				for unused in range(300):
					if view.actor.distance_to(waypoint)<1.3: break
					view.advance(1.0/60.0,waypoint-view.actor)
				check(view.actor.distance_to(waypoint)<1.3 and view.can_stand(view.actor),"Route q%d %s"%[q,prop.id])
		for side in range(4):
			var point: Vector2 = Vector2(view.Geometry.DIRS[side])*190
			check(view.can_stand(point)==(life or side!=q),"Rotated doorway q%d side%d"%[q,side])
		if reactor:
			# Existing main-game perimeter anchors are at 0.30 cell, joined diagonally.
			for side in range(4):
				var a: Vector2 = Vector2(view.Geometry.DIRS[side])*384.0*0.30
				var b: Vector2 = Vector2(view.Geometry.DIRS[(side+1)%4])*384.0*0.30
				for step in range(101):
					check(view.can_stand(a.lerp(b,step/100.0)),"Reactor perimeter segment q%d side%d sample%d"%[q,side,step])
		view.actor = Vector2(0,120) if reactor else Vector2.ZERO
		await snap("q%d"%q)
		view.show_actor = false
		var before: PackedByteArray = await snap("q%d-active-a"%q)
		view.advance(0.7)
		check(before!=await snap("q%d-active-b"%q),"Active pixels q%d"%q)
		view.operating = false
		before = await snap("q%d-offline-a"%q)
		view.advance(0.7)
		check(before==await snap("q%d-offline-b"%q),"Offline pixels q%d"%q)
		view.advance(0.1,Vector2.RIGHT)
		check(view.actor.x>0,"Crew moves offline")
		view.paused = true
		var position: Vector2 = view.actor
		var time: float = view.actor_clock
		view.advance(0.7,Vector2.RIGHT)
		check(view.actor==position and view.actor_clock==time,"Pause freezes crew")
	print("SOUTH FACING: failures=",failures,"; 4 layouts, ",view.props.size()*4," depth pairs/routes, state pixels and pause, fixed-facing bounds/anchors, rotated sockets")
	if reactor: print("REACTOR PERIMETER: 1616 collision samples over four layouts; actual station walker integration remains separate")
	quit(0 if failures==0 else 1)
