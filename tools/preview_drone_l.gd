extends SceneTree
## Native composition study; leaves gameplay and rotated room art unchanged.
class Composition extends Node2D:
	var room
	var installation: ImageTexture
	var straight: ImageTexture
	var straight_bounds: Rect2
	func _draw() -> void:
		draw_rect(Rect2(0,0,900,900),Color("102a33"))
		room.configure_embedded(0,[1,2],false,0.0)
		room.layout=[{"cell":Vector2i.ZERO,"rotation":3,"kind":4}]
		room.edges=room.Geometry.edges(room.layout)
		for edge in room.edges: edge.open=edge.port
		assert(room.Geometry.has_port(room.layout[0],1) and room.Geometry.has_port(room.layout[0],2))
		assert(not room.Geometry.has_port(room.layout[0],0) and not room.Geometry.has_port(room.layout[0],3))
		room.props.clear()
		room.dressing=null
		room.render_into(self,Vector2(450,450),1.9)
		var fit:=minf(366.0/straight_bounds.size.x,360.0/straight_bounds.size.y)
		var target:=Rect2(Vector2(450,450)+Vector2(-184,-196)*1.9,straight_bounds.size*fit*1.9)
		draw_texture_rect_region(straight,target,straight_bounds)
		var source_region:=Rect2(883,699,363,469)
		var prop_scale:=minf(78.0/source_region.size.x,108.0/source_region.size.y)
		var prop_size:=source_region.size*prop_scale
		var prop_rect:=Rect2(Vector2(178-prop_size.x,62),prop_size)
		assert(not prop_rect.intersects(Rect2(0,-36,192,72)))
		assert(not prop_rect.intersects(Rect2(-36,0,72,192)))
		draw_texture_rect_region(installation,Rect2(Vector2(450,450)+prop_rect.position*1.9,prop_rect.size*1.9),source_region)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(900,900)
	root.content_scale_size=root.size
	var room=load("res://rooms/underwater/rare-dead-ends/isolation_vault_view.gd").new()
	room.embedded=true
	room.hide()
	root.add_child(room)
	var source:=Image.new()
	assert(source.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/l-shaped-studies/drone-clean-v1.png"))==OK)
	var composition:=Composition.new()
	composition.room=room
	composition.installation=ImageTexture.create_from_image(source)
	var straight_image:=Image.new()
	assert(straight_image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/l-shaped-studies/drone-straight-clean-v1.png"))==OK)
	composition.straight=ImageTexture.create_from_image(straight_image)
	composition.straight_bounds=Rect2(straight_image.get_used_rect())
	root.add_child(composition)
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png("res://rooms/underwater/l-shaped-studies/drone-room-v3.png")==OK)
	print("DRONE L ROOM COMPOSITION PASS")
	quit()
