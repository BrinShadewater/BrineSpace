extends SceneTree
class Card extends Node2D:
	var room
	func _draw() -> void:
		if room==null:return
		room.configure_embedded(0,[],false,0.0)
		room.render_into(self,Vector2(256,256),1.16)
func _init() -> void:call_deferred("run")
func run() -> void:
	root.size=Vector2i(512,512)
	root.content_scale_size=root.size
	root.transparent_bg=true
	var card:=Card.new()
	root.add_child(card)
	for id in ["pressure_control","listening_post","isolation_vault"]:
		var room=load("res://rooms/underwater/rare-dead-ends/%s_view.gd" % id).new()
		room.embedded=true
		room.hide()
		root.add_child(room)
		card.room=room
		card.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		assert(root.get_texture().get_image().save_png("res://rooms/underwater/rare-dead-ends/%s-card-flush-v1.png" % id)==OK)
		card.room=null
		card.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		room.free()
	print("RARE ROOM CARDS PASS")
	quit()
