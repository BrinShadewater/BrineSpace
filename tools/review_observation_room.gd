extends SceneTree
const View=preload("res://rooms/underwater/observation-room-v1/observation_room_view.gd")
class Canvas extends Node2D:
	var room
	var running:=false
	var at:=Vector2(256,256)
	var zoom:=1.16
	var open: Array=[]
	func _draw() -> void:
		room.configure_embedded(0,open,running,0)
		room.render_into(self,at,zoom)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(512,512)
	root.content_scale_size=root.size
	root.transparent_bg=true
	DirAccess.make_dir_recursive_absolute("res://output/observation-room-v1")
	var room:=View.new()
	room.embedded=true
	room.hide()
	root.add_child(room)
	var canvas:=Canvas.new()
	canvas.room=room
	root.add_child(canvas)
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png("res://rooms/underwater/observation-room-v1/card.png")==OK)
	canvas.open=[2]
	canvas.running=true
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png("res://output/observation-room-v1/open.png")==OK)
	assert(room.props.size()==5)
	for prop in room.props:
		assert(Rect2(-180,-180,360,360).grow(0.01).encloses(room.prop_visual_bounds(prop)))
	for y in range(0,161,4):
		assert(room.Geometry.can_stand(Vector2(104,y),room.layout,room.props,room.edges),"South approach blocked")
	assert(not room.Geometry.has_port(room.layout[0],0))
	assert(room.Geometry.has_port(room.layout[0],2))
	assert(not room.can_stand(Vector2(-155,60)),"Bookshelf lacks collision")
	print("OBSERVATION ART PASS: native card, five registered pieces, clear south approach and blocked shelves")
	quit()
