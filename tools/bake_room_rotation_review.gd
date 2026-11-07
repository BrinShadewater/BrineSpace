extends SceneTree
const View = preload("res://rooms/whole-room/nursery_south_facing.gd")
class TileReviewView extends View:
	func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
		super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
		for edge in edges: edge.aperture = 72.0
	func draw_room_floor(center: Vector2) -> void:
		for y in range(8):
			for x in range(8):
				painter.draw_texture_rect_region(texture,Rect2(center+Vector2(-192+x*48,-192+y*48),Vector2(48,48)),Rect2(571,552,120,120))
		# Center one full 48-unit tile on the room/door axes. Border tiles
		# are half-width where they meet the unchanged 384-unit room edge.
		for seam in [-168,-120,-72,-24,24,72,120,168]:
			painter.draw_line(center+Vector2(seam,-184),center+Vector2(seam,184),Color("202830"),1.0)
			painter.draw_line(center+Vector2(-184,seam),center+Vector2(184,seam),Color("202830"),1.0)
		for prop in props:
			if prop.center!=center: continue
			var at := Vector2(prop.rect.get_center().x,prop.rect.end.y+10)
			painter.draw_texture_rect_region(texture,Rect2(at-Vector2(30,4),Vector2(60,8)),Rect2(249,474,181,26))
class Review extends Node2D:
	var rooms: Array = []
	func _draw() -> void:
		draw_rect(Rect2(0,0,1600,1680),Color("141c24"))
		draw_string(ThemeDB.fallback_font,Vector2(44,44),"MYCELIUM NURSERY / FOUR ROTATIONS",HORIZONTAL_ALIGNMENT_LEFT,-1,27,Color("e2ebe7"))
		draw_string(ThemeDB.fallback_font,Vector2(44,74),"48 x 48 floor tiles / 1.5-tile-wide doorways / south-facing props / unused sockets sealed",HORIZONTAL_ALIGNMENT_LEFT,-1,19,Color("adbdc5"))
		for q in range(4):
			var at := Vector2(400+(q%2)*800,465+(q/2)*790)
			var room = rooms[q]
			var door := (2+q)%4
			room.configure_embedded(q,[door],true,0.7)
			# A short neutral continuation makes the connected exit explicit.
			var direction: Vector2 = Vector2(room.Geometry.DIRS[door])
			var size := Vector2(72,35) if door%2==0 else Vector2(35,72)
			var stub := at+direction*207*1.65
			draw_rect(Rect2(stub-size*1.65*0.5,size*1.65),Color("303740"))
			room.render_into(self,at,1.65)
			draw_string(ThemeDB.fallback_font,Vector2(at.x-350,at.y-359),"%d degrees  /  open %s"%[q*90,["NORTH","EAST","SOUTH","WEST"][door]],HORIZONTAL_ALIGNMENT_LEFT,-1,23,Color("ded7bc"))
		draw_string(ThemeDB.fallback_font,Vector2(44,1645),"Current assembly, not final bible approval: no animated door leaf or department-finish revision shown.",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("adbdc5"))
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size = Vector2i(1600,1680)
	root.content_scale_size = Vector2i(1600,1680)
	var review := Review.new()
	review.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	for q in range(4):
		var room := View.new()
		room.embedded = true
		room.hide()
		root.add_child(room)
		room.configure_embedded(q,[(2+q)%4],true,0.7)
		var open_count := 0
		for edge in room.edges:
			if edge.open: open_count += 1
		assert(open_count==1 and room.edges.size()==4)
		assert(room.Geometry.OPENING==72.0 and room.Geometry.FLOOR_TILE==48.0)
		for prop in room.props:
			assert(Rect2(-180,-180,360,360).encloses(room.prop_visual_bounds(prop)))
		var edge: Dictionary = room.edges[(2+q)%4]
		var walls: Array = room.Geometry.wall_rects(edge)
		var gap: float = walls[1].position.x-walls[0].end.x if edge.horizontal else walls[1].position.y-walls[0].end.y
		assert(is_equal_approx(gap,72.0))
		review.rooms.append(room)
	root.add_child(review)
	await process_frame
	await RenderingServer.frame_post_draw
	var out := "res://output/whole-room-pilot-01/nursery-four-rotation-locked-fit.png"
	assert(not FileAccess.file_exists(out))
	assert(root.get_texture().get_image().save_png(out)==OK)
	print("ROTATION REVIEW: four production assemblies, verified 72-unit openings, 48-unit tiles and complete prop containment")
	quit()
