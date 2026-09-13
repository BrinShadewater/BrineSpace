extends SceneTree
const View=preload("res://rooms/underwater/cold-store-v1/cold_store_view.gd")
const Content=preload("res://scripts/room_content_canvas.gd")
class Preview extends Node2D:
	var room
	var origin: Vector2
	func _draw() -> void:
		draw_set_transform(origin,0,Vector2.ONE*.75)
		room.painter=self
		for prop in room.props:room.draw_registered_prop(prop)
func _init() -> void:call_deferred("run")
func run() -> void:
	root.size=Vector2i(1200,900);root.content_scale_size=root.size
	var background=ColorRect.new();background.size=Vector2(1200,900);background.color=Color("413b32");root.add_child(background)
	var previews=[]
	for row in range(3):
		for q in range(4):
			var room=View.new();root.add_child(room);room.hide()
			room.configure_embedded(q,[],row>0,float(row))
			var preview=Preview.new();preview.room=room;preview.origin=Vector2(150+q*300,150+row*300)
			root.add_child(preview);previews.append(preview)
	await process_frame
	await RenderingServer.frame_post_draw
	var folder="res://output/cold-store-owner-repair-2026-09-12/furnishing-states"
	DirAccess.make_dir_recursive_absolute(folder)
	assert(root.get_texture().get_image().save_png(folder+"/direct.png")==OK)
	var canvases=[]
	for preview in previews:
		preview.hide()
		var canvas=Content.new();root.add_child(canvas);canvas.draw_origin=preview.origin;canvas.draw_scale=.75
		var queue=[]
		for prop in preview.room.props:queue.append({"kind":"prop","prop":prop})
		canvas.submit(preview.room,queue)
		canvases.append(canvas)
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png(folder+"/retained.png")==OK)
	# Reuse the same static slots across both power transitions.
	for powered in [false,true]:
		for i in range(previews.size()):
			var room=previews[i].room;room.operating=powered
			var queue=[]
			for prop in room.props:queue.append({"kind":"prop","prop":prop})
			canvases[i].submit(room,queue)
		await process_frame
		await RenderingServer.frame_post_draw
		assert(root.get_texture().get_image().save_png(folder+"/transition-%s.png"%str(powered))==OK)
	print("COLD STORE FURNISHING STATES: 4 rotations x off/on/two clocks, direct and retained")
	quit()
