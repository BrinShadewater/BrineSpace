extends SceneTree
## Native composition study; leaves gameplay and rotated room art unchanged.
class Composition extends Node2D:
	var room
	var installation: ImageTexture
	var art_bounds: Rect2
	func _draw() -> void:
		draw_rect(Rect2(0,0,900,900),Color("102a33"))
		room.configure_embedded(0,[2],false,0.0)
		room.props.clear()
		room.dressing=null
		room.render_into(self,Vector2(450,450),1.9)
		draw_texture_rect_region(installation,Rect2(450-184*1.9,450-196*1.9,368*1.9,368*1.9),art_bounds)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(900,900)
	root.content_scale_size=root.size
	var room=load("res://rooms/underwater/rare-dead-ends/isolation_vault_view.gd").new()
	room.embedded=true
	room.hide()
	root.add_child(room)
	var source:=Image.new()
	assert(source.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/rare-dead-ends/isolation-u-flush-clean-v1.png"))==OK)
	var composition:=Composition.new()
	composition.room=room
	composition.installation=ImageTexture.create_from_image(source)
	composition.art_bounds=Rect2(source.get_used_rect())
	root.add_child(composition)
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png("res://rooms/underwater/rare-dead-ends/isolation-u-flush-room-v1.png")==OK)
	print("LISTENING U ROOM COMPOSITION PASS")
	quit()
