extends SceneTree
const View=preload("res://assets/observation-office-v1/completed_room_view.gd")
class Preview extends Node2D:
	var room
	var foundation: Texture2D
	func _draw() -> void:
		draw_rect(Rect2(0,0,1000,1100),Color("12262b"))
		var origin:=Vector2(500,505)
		var zoom:=1.85
		draw_set_transform(origin,0,Vector2.ONE*zoom)
		draw_texture_rect_region(foundation,Rect2(-192,181.632,384,384.0*596/1934),Rect2(25,138,1934,596),Color(.72,.78,.80))
		room.configure_embedded(0,[],true,0)
		room.render_into(self,origin,zoom,true)
		draw_set_transform(origin,0,Vector2.ONE*zoom)
		preload("res://rooms/whole-room/north_wall.gd").draw_into(self,"observation_room",Vector2i.ZERO,false,false,room)
		room.render_into(self,origin,zoom,false,false)
		draw_set_transform(Vector2.ZERO)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1000,1100)
	root.content_scale_size=root.size
	preload("res://scripts/room_layout_store.gd").path="res://output/observation-preview-layouts.json"
	var room:=View.new()
	room.embedded=true
	room.hide()
	root.add_child(room)
	var preview:=Preview.new()
	preview.room=room
	var image:=Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, "res://rooms/foundation-v1/foundation-silt-v1.png")
	preview.foundation=ImageTexture.create_from_image(image)
	root.add_child(preview)
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png("res://assets/observation-office-v1/completed-room.png")==OK)
	room.configure_embedded(0,[2],true,0)
	var visited: Dictionary={Vector2i(0,21):true}
	var queue: Array=[Vector2i(0,21)]
	while not queue.is_empty():
		var cell: Vector2i=queue.pop_front()
		for direction in [Vector2i.UP,Vector2i.DOWN,Vector2i.LEFT,Vector2i.RIGHT]:
			var next: Vector2i=cell+direction
			if abs(next.x)>22 or abs(next.y)>22 or visited.has(next): continue
			if room.can_stand(Vector2(next)*8):
				visited[next]=true
				queue.append(next)
	assert(visited.has(Vector2i(0,-2)),"Window approach must remain reachable around desk")
	for prop in room.props: assert(Rect2(-180,-180,360,360).grow(.1).encloses(room.prop_visual_bounds(prop)))
	for path in ["res://assets/observation-office-v1/completed_room_view.gd","res://assets/observation-office-v1/render_completed_room.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var f:=FileAccess.open(path+".uid",FileAccess.WRITE)
			f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("COMPLETED OBSERVATION PREVIEW PASS: five props, native riser/foundation, window access and sprite bounds")
	quit()
