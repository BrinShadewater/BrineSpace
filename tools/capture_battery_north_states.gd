extends SceneTree
const View=preload("res://rooms/full-wall-v1/battery_array_view.gd")
const Content=preload("res://scripts/room_content_canvas.gd")

class Preview extends Node2D:
	var room
	var origin: Vector2
	func _draw() -> void:
		draw_set_transform(origin,0,Vector2.ONE)
		room.painter=self
		for prop in room.props:room.draw_registered_prop(prop)

func _init() -> void:call_deferred("run")
func run() -> void:
	root.size=Vector2i(1200,400);root.content_scale_size=root.size
	var background=ColorRect.new();background.size=Vector2(1200,400);background.color=Color("413b32");root.add_child(background)
	var previews=[]
	for state in range(3):
		var room=View.new();root.add_child(room);room.hide()
		room.configure_embedded(0,[],state>0,float(state))
		var preview=Preview.new();preview.room=room;preview.origin=Vector2(200+state*400,240)
		root.add_child(preview);previews.append(preview)
	await process_frame;await RenderingServer.frame_post_draw
	var folder="res://output/battery-owner-north-repair-2026-09-12/states"
	DirAccess.make_dir_recursive_absolute(folder)
	assert(root.get_texture().get_image().save_png(folder+"/direct.png")==OK)
	for preview in previews:
		preview.hide()
		var canvas=Content.new();root.add_child(canvas);canvas.draw_origin=preview.origin
		var queue=[]
		for prop in preview.room.props:queue.append({"kind":"prop","prop":prop})
		canvas.submit(preview.room,queue)
	await process_frame;await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png(folder+"/retained.png")==OK)
	var path="res://tools/capture_battery_north_states.gd.uid"
	if not FileAccess.file_exists(path):
		var uid_file=FileAccess.open(path,FileAccess.WRITE)
		uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid_file.close()
	print("BATTERY NORTH STATES: q0 offline and two operating clocks, direct and retained")
	quit()
