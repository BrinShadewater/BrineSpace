extends SceneTree
## Isolated native geometry/art-fit study. No main scene, economy or saves.
const G = preload("res://tools/modular_room_geometry.gd")
const Door = preload("res://rooms/doors/department_door.gd")
const Nursery = preload("res://rooms/whole-room/nursery_south_facing.gd")
const Life = preload("res://rooms/whole-room/life_support_view.gd")
const NarrowGeometry = preload("res://rooms/underwater/corridor_geometry.gd")
const HullArt = preload("res://rooms/underwater/corridor_surfaces.gd")
const OUT := "res://output/underwater-corridor-v8"
var failures := 0

class Study extends Node2D:
	var rooms: Array = []
	var materials: Dictionary
	var quarter := 0
	var actor := Vector2.ZERO
	var zoom := 0.9
	var origin := Vector2.ZERO
	var show_grid := false
	var guide := -1
	var hull_textures: Array = []
	var powered := true
	var door_frame := 9
	var sealed_seam := -1
	var cycle_clock := 0.0
	var cycle_seam := 2
	var cycle_reverse := false
	var paused := false
	var actor_direction := "south"
	func tick(delta: float) -> void:
		if paused: return
		cycle_clock = minf(cycle_clock+delta,4.0)
		var t := cycle_clock
		door_frame = mini(9,roundi(t*9/0.8)) if t<0.8 else (9 if t<3.2 else maxi(0,9-roundi((t-3.2)*9/0.8)))
		var progress := clampf((t-0.8)/2.4,0,1)
		var axis := Vector2.DOWN if cycle_seam==2 else Vector2.RIGHT
		if cycle_reverse: axis = -axis
		var world_axis := G.turn(axis,quarter)
		actor_direction = "east" if world_axis.x>0 else ("west" if world_axis.x<0 else ("south" if world_axis.y>0 else "north"))
		actor = G.turn(seams[cycle_seam]+axis*lerpf(-70,70,progress),quarter)
		queue_redraw()
	var seams := [Vector2(192,0),Vector2(576,0),Vector2(768,192)]
	var centers := [Vector2.ZERO,Vector2(384,0),Vector2(768,0),Vector2(768,384)]
	# Interior 96; collar narrows to 72 over the final 32 world units.
	var straight := NarrowGeometry.straight
	var elbow := NarrowGeometry.elbow
	var straight_hull := NarrowGeometry.straight_hull
	var elbow_hull := NarrowGeometry.elbow_hull
	func transformed(poly: PackedVector2Array, center: Vector2) -> PackedVector2Array:
		var result := PackedVector2Array()
		for p in poly: result.append(G.turn(p+center,quarter))
		return result
	func configure(q: int) -> void:
		quarter = q
		rooms[0].configure_embedded(q,[(1+q)%4],false,0)
		rooms[1].configure_embedded(q,[(0+q)%4],false,0)
		var bounds := Rect2(G.turn(Vector2(-200,-200),q),Vector2.ZERO)
		for p in [Vector2(-200,584),Vector2(968,-200),Vector2(968,584)]: bounds = bounds.expand(G.turn(p,q))
		zoom = minf(1440/bounds.size.x,720/bounds.size.y)
		origin = Vector2(800,465)-bounds.get_center()*zoom
		actor = G.turn(Vector2.ZERO,q)
		queue_redraw()
	func inside_floor(p: Vector2) -> bool:
		var local := G.turn(p,-quarter)
		for c in [centers[0],centers[3]]:
			if Rect2(c-Vector2.ONE*184,Vector2.ONE*368).has_point(local): return true
		if Geometry2D.is_point_in_polygon(local-centers[1],straight): return true
		if Geometry2D.is_point_in_polygon(local-centers[2],elbow): return true
		for i in range(3):
			var size := Vector2(72,20) if i==2 else Vector2(20,72)
			if Rect2(seams[i]-size/2,size).has_point(local): return true
		return false
	func walkable(p: Vector2) -> bool:
		if not inside_floor(p): return false
		var local := G.turn(p,-quarter)
		for i in range(3):
			if i!=sealed_seam and door_frame==9: continue
			var size := Vector2(72,16) if i==2 else Vector2(16,72)
			if Rect2(seams[i]-size/2,size).grow(G.RADIUS).has_point(local): return false
		for i in range(16):
			if not inside_floor(p+Vector2.from_angle(i*TAU/16)*G.RADIUS): return false
		for index in range(2):
			var center: Vector2 = G.turn(centers[0 if index==0 else 3],quarter)
			for prop in rooms[index].props:
				if prop.rect.grow(G.RADIUS).has_point(p-center): return false
		return true
	func advance(direction: Vector2, seconds: float) -> bool:
		var next := actor+direction*100*seconds
		if not walkable(next): return false
		actor = next
		queue_redraw()
		return true
	func _draw() -> void:
		if guide>=0:
			draw_rect(Rect2(0,0,1280,1280),Color("09222d"))
			draw_set_transform(Vector2(640,640),0,Vector2.ONE*3)
			draw_colored_polygon(straight_hull if guide==0 else elbow_hull,Color("9bada8"))
			draw_colored_polygon(straight if guide==0 else elbow,Color("334951"))
			draw_set_transform(Vector2.ZERO)
			return
		draw_rect(Rect2(0,0,1600,900),Color("09222d"))
		for i in range(70):
			draw_circle(Vector2((i*137)%1600,(i*239)%900),1,Color("204550"))
		draw_string(ThemeDB.fallback_font,Vector2(35,35),"UNDERWATER HULL / CONNECTION STUDY",HORIZONTAL_ALIGNMENT_LEFT,-1,24,Color("d3e4df"))
		draw_string(ThemeDB.fallback_font,Vector2(35,65),"384 card | 96 clear corridor | 16 hull walls | 72 doorway | rotation %d"%(quarter*90),HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("8cbbb9"))
		for index in range(2):
			rooms[index].render_into(self,origin+G.turn(centers[0 if index==0 else 3],quarter)*zoom,zoom)
		draw_set_transform(origin,0,Vector2.ONE*zoom)
		for i in range(2):
			HullArt.draw_hull(self,straight_hull if i==0 else elbow_hull,straight if i==0 else elbow,centers[i+1],quarter,hull_textures,i==1,powered)
		if show_grid:
			for center in centers:
				draw_rect(Rect2(G.turn(center,quarter)-Vector2.ONE*192,Vector2.ONE*384),Color("64a7a2"),false,1)
		# Shared doors: ground layers before actor, upright parts by ground depth.
		for behind in [true,false]:
			for i in range(3):
				var seam: Vector2 = G.turn(seams[i],quarter)
				var vertical := (i!=2) != (quarter%2==1)
				draw_set_transform(origin+seam*zoom,0,Vector2.ONE*zoom)
				if i==sealed_seam:
					if behind:
						var rect := Rect2(-8,-52,16,104) if vertical else Rect2(-52,-8,104,16)
						draw_rect(rect,Color("a4afaa") if powered else Color("3b4645"))
						draw_rect(rect.grow(-2),Color("637573") if powered else Color("273130"))
					continue
				for part in Door.corridor_parts(door_frame,vertical,"generic"):
					if (part.floor or actor.y>seam.y+part.depth)==behind: Door.draw_piece(self,materials,"generic",part,1 if powered else 0)
			if behind:
				draw_set_transform(origin,0,Vector2.ONE*zoom)
				rooms[0].painter = self
				rooms[0].actor = actor
				rooms[0].walking = cycle_clock>0.8 and cycle_clock<3.2
				rooms[0].actor_clock = cycle_clock
				rooms[0].actor_direction = actor_direction
				var key := ("walk/" if rooms[0].walking else "idle/")+actor_direction
				var frames: Array = rooms[0].actor_library.actor_frames[key]
				rooms[0].external_actor_texture = frames[int(cycle_clock*6)%frames.size()]
				rooms[0].draw_actor()
				rooms[0].painter = rooms[0]
		draw_set_transform(Vector2.ZERO)
		draw_string(ThemeDB.fallback_font,Vector2(35,872),"ART KIT REVIEW / fixed hull geometry + registered surfaces / no flooding or gameplay changes",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("8cbbb9"))

func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures+=1
		push_error(message)
func run() -> void:
	if DirAccess.dir_exists_absolute(OUT):
		push_error("Refusing to overwrite corridor evidence")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1600,900)
	root.content_scale_size = root.size
	var study := Study.new()
	root.add_child(study)
	study.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	for script in [Nursery,Life]:
		var room = script.new()
		room.embedded = true
		study.add_child(room)
		study.rooms.append(room)
	study.rooms[0].actor_library.load_actor_art()
	var image := Image.new()
	check(image.load_png_from_buffer(FileAccess.get_file_as_bytes(Door.SOURCE))==OK,"Door source loads")
	study.materials = Door.make_materials(study,ImageTexture.create_from_image(image))
	study.hull_textures = HullArt.load_sources()
	var samples := 0
	for q in range(4):
		study.configure(q)
		for i in range(3):
			var axis := Vector2.RIGHT if i==2 else Vector2.DOWN
			for sign_value in [-1,1]:
				check(study.walkable(G.turn(study.seams[i]+axis*28*sign_value,q)),"Character fits inside 72-unit socket with safety margin")
				check(not study.walkable(G.turn(study.seams[i]+axis*31*sign_value,q)),"Character radius cannot cross socket jamb")
		for reverse in [false,true]:
			var route := [Vector2.ZERO,Vector2(384,0),Vector2(768,0),Vector2(768,384)]
			if reverse: route.reverse()
			study.actor = G.turn(route[0],q)
			for segment in range(3):
				var target := G.turn(route[segment+1],q)
				var direction := (target-study.actor).normalized()
				for step in range(384):
					check(study.advance(direction,0.01),"Character radius cannot pass route q%d segment%d step%d"%[q,segment,step])
					samples+=1
		study.actor = G.turn(Vector2(192,0),q)
		study.show_grid = false
		await snap(study,"rotation-%d"%q)
		study.show_grid = true
		await snap(study,"grid-%d"%q)
		study.show_grid = false
		for frame in range(10):
			study.door_frame = frame
			study.actor = G.turn(Vector2(150,0),q)
			check(study.walkable(G.turn(Vector2(192,0),q))==(frame==9),"Crossing gated by open door state")
			await snap(study,"q%d-door-%02d"%[q,frame])
		study.door_frame = 9
		study.powered = false
		await snap(study,"q%d-off"%q)
		study.powered = true
		for seam in range(3):
			study.sealed_seam = seam
			check(not study.walkable(G.turn(study.seams[seam],q)),"Sealed seam blocks traversal")
			await snap(study,"q%d-sealed-%d"%[q,seam])
		study.sealed_seam = -1
		# Outside narrow hull must remain water, not invisible full-cell floor.
		check(not study.walkable(G.turn(Vector2(384,100),q)),"Water beside corridor blocks walking")
		check(not study.walkable(G.turn(Vector2(768+100,100),q)),"Water beside elbow blocks walking")
	# Native 2x seam views: complete opening, crossing and closing; no image warping.
	for q in range(4):
		study.configure(q)
		study.cycle_seam = 2
		study.zoom = 2.0
		study.origin = Vector2(800,465)-G.turn(study.seams[2],q)*2
		for reverse in [false,true]:
			study.cycle_reverse = reverse
			study.cycle_clock = 0
			for frame in range(41):
				study.tick(0 if frame==0 else 0.1)
				check(study.walkable(study.actor),"Animated crossing keeps actor clear of closed leaves and hull")
				study.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				var crop := root.get_texture().get_image().get_region(Rect2i(608,273,384,384))
				crop.save_png(OUT.path_join("cycle-q%d-r%s-%02d.png"%[q,reverse,frame]))
				if frame==20:
					study.paused = true
					var before := study.actor
					var time := study.cycle_clock
					study.tick(0.7)
					check(study.actor==before and study.cycle_clock==time,"Pause freezes door and walker clocks")
					study.paused = false
	root.size = Vector2i(1280,1280)
	root.content_scale_size = root.size
	for index in range(2):
		study.guide = index
		await snap(study,"straight-guide" if index==0 else "corner-guide")
	print("UNDERWATER CORRIDOR %s: %d movement steps, four rotations, both travel directions, water rejection. Visual review required."%["PASS" if failures==0 else "FAIL",samples])
	quit(0 if failures==0 else 1)
func snap(study: Node2D, name: String) -> void:
	study.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT.path_join(name+".png"))
