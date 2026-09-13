extends SceneTree
const Lighting=preload("res://rooms/whole-room/room_lighting.gd")
const SOURCES=["res://rooms/underwater/galley-v1/galley_view.gd","res://rooms/underwater/cold-store-v1/cold_store_view.gd","res://rooms/underwater/salvage-workshop-v1/workshop_view.gd","res://rooms/full-wall-v1/command_center_view.gd"]
const OUT="res://output/equipment-grounding-v1"
class Preview extends Node2D:
	var room
	var origin: Vector2
	func _draw() -> void:
		room.render_into(self,origin,1.0,true)
		draw_set_transform(origin)
		Lighting.draw_equipment_shadows(self,room.props,1.0,room)
		room.render_into(self,origin,1.0,false,false)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1600,900)
	root.content_scale_size=root.size
	DirAccess.make_dir_recursive_absolute(OUT)
	var background=ColorRect.new()
	background.size=Vector2(1600,900)
	background.color=Color("20292c")
	root.add_child(background)
	var previews=[]
	for i in range(SOURCES.size()):
		var room=load(SOURCES[i]).new()
		room.embedded=true
		root.add_child(room)
		room.hide()
		room.configure_embedded(0,[],true,2.0)
		var preview=Preview.new()
		preview.room=room
		preview.origin=Vector2(200+i*400,460)
		root.add_child(preview)
		previews.append(preview)
	for q in range(4):
		for preview in previews:
			preview.room.configure_embedded(q,[],true,2.0)
			preview.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var result=root.get_texture().get_image().save_png(OUT+"/q%d.png"%q)
		if result!=OK: quit(1); return
	print("GROUNDING CAPTURES: Galley, Cold Store, Salvage, Command; four rotations")
	quit()
