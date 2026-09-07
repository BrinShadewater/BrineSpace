extends SceneTree
const TYPES = [preload("res://rooms/whole-room/nursery_south_facing.gd"),preload("res://rooms/whole-room/life_support_view.gd"),preload("res://rooms/whole-room/hydroponics_view.gd"),preload("res://rooms/whole-room/reactor_view.gd")]
const Lighting = preload("res://rooms/whole-room/room_lighting.gd")
class Review extends Node2D:
	var rooms: Array = []
	var opened := false
	var scale_room := 1.45
	func at(i: int) -> Vector2:
		return Vector2(365+(i%2)*384*scale_room,395+(i/2)*384*scale_room)
	func _draw() -> void:
		draw_rect(Rect2(0,0,1290,1300),Color("161e26"))
		draw_string(ThemeDB.fallback_font,Vector2(58,45),"CONNECTED ROOMS / DOOR PANEL STUDY",HORIZONTAL_ALIGNMENT_LEFT,-1,27,Color("dce5dc"))
		draw_string(ThemeDB.fallback_font,Vector2(58,75),"72-unit apertures / paired north sconces / %s"%("OPEN" if opened else "CLOSED"),HORIZONTAL_ALIGNMENT_LEFT,-1,19,Color("a8bdb2"))
		for i in range(4):
			rooms[i].render_into(self,at(i),scale_room,true,false)
			draw_set_transform(at(i),0,Vector2.ONE*scale_room)
			Lighting.draw_pools(self,1)
			draw_set_transform(Vector2.ZERO)
		for i in range(4): rooms[i].render_into(self,at(i),scale_room,false,false)
		for i in range(4):
			draw_set_transform(at(i),0,Vector2.ONE*scale_room)
			Lighting.draw_fixtures(self,1)
			draw_set_transform(Vector2.ZERO)
		# Exactly one assembly per shared edge; procedural visual proposal only.
		for edge in [[0,1],[0,2],[1,3],[2,3]]:
			var center: Vector2 = (at(edge[0])+at(edge[1]))*0.5
			var vertical: bool = edge[1]-edge[0]==1
			draw_set_transform(center,PI/2 if vertical else 0,Vector2.ONE*scale_room)
			if not opened:
				for side in [-1,1]:
					var panel := Rect2(-36 if side==-1 else 0,-6,36,12)
					draw_rect(panel,Color("18262e"))
					draw_rect(panel.grow(-1),Color("879791"))
					draw_line(panel.position+Vector2(2,3),panel.position+Vector2(34,3),Color("c8d0bc"),1)
					draw_line(panel.position+Vector2(3,9),panel.position+Vector2(33,9),Color("4d6260"),1)
				draw_line(Vector2(0,-6),Vector2(0,6),Color("132329"),1)
			else:
				draw_rect(Rect2(-38,-6,2,12),Color("879791"))
				draw_rect(Rect2(36,-6,2,12),Color("879791"))
			for side in [-1,1]:
				draw_rect(Rect2(side*39-2,-4,4,8),Color("263c3b"))
				draw_rect(Rect2(side*39-1,-2,2,4),Color("91d4b0"))
			draw_set_transform(Vector2.ZERO)
		draw_string(ThemeDB.fallback_font,Vector2(58,1275),"Preview-only door leaves; not final art or gameplay. Existing floor sampling left unchanged for review.",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("a8bdb2"))
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size = Vector2i(1290,1300)
	root.content_scale_size = root.size
	var review := Review.new()
	var sides := [[1,2],[2,3],[0,1],[0,3]]
	for i in range(4):
		var room = TYPES[i].new()
		room.embedded = true
		root.add_child(room)
		room.hide()
		room.configure_embedded(0,sides[i],true,0.7,[3] if i==1 else ([0] if i==2 else ([0,3] if i==3 else [])))
		review.rooms.append(room)
	root.add_child(review)
	for opened in [false,true]:
		review.opened = opened
		review.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var out := "res://output/whole-room-pilot-01/connected-door-panels-v2-%s.png"%("open" if opened else "closed")
		assert(not FileAccess.file_exists(out))
		assert(root.get_texture().get_image().save_png(out)==OK)
	print("DOOR PREVIEW: closed/open native four-room studies; no production mutation")
	quit()
