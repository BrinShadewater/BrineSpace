extends SceneTree
const View=preload("res://rooms/production-ten/command_center_view.gd")
class Preview extends Node2D:
	var room
	func _draw() -> void:
		draw_rect(Rect2(0,0,1440,600),Color("34474b"))
		var centers=[Vector2(0,-140),Vector2(140,0),Vector2(0,140),Vector2(-140,0)]
		room.painter=self
		for col in range(4):
			for row in range(3):
				room.operating=row>0
				room.machine_clock=0.0 if row<2 else 1.0
				for item in range(3):
					var prop={"id":["command_table","command_comms","command_systems"][item],"rect":Rect2(centers[col]-Vector2(42,26),Vector2(84,52)),"registration":{}}
					var bounds: Rect2=room._overhead_bounds(prop)
					draw_set_transform(Vector2(60+360*col+120*item,100+200*row)-bounds.get_center()*0.85,0,Vector2.ONE*0.85)
					room.draw_registered_prop(prop)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1440,600); root.content_scale_size=root.size
	var room=View.new(); var preview=Preview.new(); preview.room=room
	root.add_child(preview)
	await process_frame
	await RenderingServer.frame_post_draw
	var folder="res://output/command-owner-repair-2026-09-12/equipment-states"
	DirAccess.make_dir_recursive_absolute(folder)
	assert(root.get_texture().get_image().save_png(folder+"/states.png")==OK)
	preview.hide()
	var background=ColorRect.new(); background.color=Color("34474b"); background.size=Vector2(1440,600); root.add_child(background)
	var centers=[Vector2(0,-140),Vector2(140,0),Vector2(0,140),Vector2(-140,0)]
	for col in range(4):
		for row in range(3):
			for item in range(3):
				room.operating=row>0; room.machine_clock=0.0 if row<2 else 1.0
				var prop={"id":["command_table","command_comms","command_systems"][item],"rect":Rect2(centers[col]-Vector2(42,26),Vector2(84,52)),"registration":{}}
				var canvas=preload("res://scripts/room_content_canvas.gd").new()
				root.add_child(canvas)
				canvas.draw_scale=0.85
				canvas.draw_origin=Vector2(60+360*col+120*item,100+200*row)-room._overhead_bounds(prop).get_center()*0.85
				canvas.submit(room,[{"kind":"prop","prop":prop}])
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png(folder+"/retained.png")==OK)
	room.free(); quit()
