extends SceneTree
const View=preload("res://rooms/underwater/galley-v1/galley_view.gd")
const Content=preload("res://scripts/room_content_canvas.gd")
class Preview extends Node2D:
	var room
	var origin: Vector2
	func _draw() -> void:
		draw_set_transform(origin,0,Vector2.ONE*.75)
		room.painter=self
		for prop in room.props:room.draw_registered_prop(prop)
		room.draw_actor()
func _init() -> void:call_deferred("run")
func run() -> void:
	root.size=Vector2i(1200,900);root.content_scale_size=root.size
	var background=ColorRect.new();background.size=Vector2(1200,900);background.color=Color("413b32");root.add_child(background)
	var previews=[]
	for row in range(3):
		for q in range(4):
			var room=View.new();root.add_child(room);room.hide()
			room.configure_embedded(q,[],row>0,float(row))
			room.external_actor_texture=room.load_source_texture("res://character/major-bill-v3/rotations/south.png")
			room.external_actor_texture.set_meta("major_bill_v2",true)
			room.external_actor_texture.set_meta("crew_pivot",Vector2(92,172))
			room.external_actor_texture.set_meta("crew_standing_height",148.0)
			room.actor=Vector2(0,50)
			var preview=Preview.new();preview.room=room;preview.origin=Vector2(150+q*300,150+row*300)
			root.add_child(preview);previews.append(preview)
	await process_frame
	await RenderingServer.frame_post_draw
	var folder="res://output/galley-owner-repair-2026-09-12/crew-scale"
	DirAccess.make_dir_recursive_absolute(folder)
	assert(root.get_texture().get_image().save_png(folder+"/direct.png")==OK)
	print("GALLEY CREW SCALE: production Bill reference, four orientations")
	quit()
