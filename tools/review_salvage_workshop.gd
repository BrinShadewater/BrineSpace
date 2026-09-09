extends SceneTree
const View=preload("res://rooms/underwater/salvage-workshop-v1/workshop_view.gd")
class Canvas extends Node2D:
	var room
	var running:=false
	var at:=Vector2(256,256)
	var zoom:=1.16
	var open: Array=[]
	var clock:=0.0
	func _draw() -> void:
		room.configure_embedded(0,open,running,clock)
		room.render_into(self,at,zoom)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(512,512)
	root.content_scale_size=root.size
	root.transparent_bg=true
	DirAccess.make_dir_recursive_absolute("res://output/salvage-workshop-v1")
	var room:=View.new()
	room.embedded=true
	room.hide()
	root.add_child(room)
	var canvas:=Canvas.new()
	canvas.room=room
	root.add_child(canvas)
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png("res://rooms/underwater/salvage-workshop-v1/card.png")==OK)
	canvas.open=[2]
	canvas.running=true
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png("res://output/salvage-workshop-v1/open.png")==OK)
	var active_image:=root.get_texture().get_image()
	canvas.clock=.7
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var moved:=root.get_texture().get_image()
	assert(active_image.get_data()!=moved.get_data(),"Operating indicator changes")
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	assert(moved.get_data()==root.get_texture().get_image().get_data(),"Frozen clock holds native image")
	canvas.running=false
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var offline:=root.get_texture().get_image()
	canvas.clock=2.0
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	assert(offline.get_data()==root.get_texture().get_image().get_data(),"Offline indicator stops")
	assert(room.props.size()==2)
	for prop in room.props:
		assert(Rect2(-180,-180,360,360).grow(0.01).encloses(room.prop_visual_bounds(prop)))
	for y in range(0,161,4):
		assert(room.Geometry.can_stand(Vector2(104,y),room.layout,room.props,room.edges),"South approach blocked")
	assert(not room.Geometry.has_port(room.layout[0],0))
	assert(room.Geometry.has_port(room.layout[0],2))
	assert(not room.can_stand(Vector2(-120,96)),"Bookshelf lacks collision")
	print("WORKSHOP ART PASS: native card, two registered pieces, clear south approach and blocked shelves")
	for path in ["res://tools/review_salvage_workshop.gd","res://rooms/underwater/salvage-workshop-v1/workshop_view.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var f:=FileAccess.open(path+".uid",FileAccess.WRITE)
			f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	quit()
