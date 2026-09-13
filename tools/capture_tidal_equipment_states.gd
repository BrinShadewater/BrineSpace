extends SceneTree
const View=preload("res://rooms/underwater/tidal-condenser/tidal_condenser_view.gd")
class Preview extends Node2D:
	var room
	func _draw() -> void:
		draw_rect(Rect2(0,0,960,600),Color("34474b"))
		var centers=[Vector2(0,-140),Vector2(140,0),Vector2(0,140),Vector2(-140,0)]
		room.painter=self
		for col in range(4):
			for row in range(3):
				room.operating=row>0
				room.machine_clock=0.0 if row<2 else 1.0
				for item in range(2):
					var prop={"id":"tidal_pump" if item==0 else "tidal_monitor","rect":Rect2(centers[col]-Vector2(42,26),Vector2(84,52)),"registration":{}}
					var bounds: Rect2=room._equipment_bounds(prop)
					draw_set_transform(Vector2(60+240*col+120*item,100+200*row)-bounds.get_center()*1.2,0,Vector2.ONE*1.2)
					room.draw_registered_prop(prop)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(960,600); root.content_scale_size=root.size
	var room=View.new(); var preview=Preview.new(); preview.room=room
	root.add_child(preview)
	await process_frame
	await RenderingServer.frame_post_draw
	var folder="res://output/tidal-owner-repair-2026-09-12/equipment-states"
	DirAccess.make_dir_recursive_absolute(folder)
	assert(root.get_texture().get_image().save_png(folder+"/states.png")==OK)
	preview.hide()
	var background=ColorRect.new(); background.color=Color("34474b"); background.size=Vector2(960,600); root.add_child(background)
	var centers=[Vector2(0,-140),Vector2(140,0),Vector2(0,140),Vector2(-140,0)]
	for col in range(4):
		for row in range(3):
			for item in range(2):
				room.operating=row>0; room.machine_clock=0.0 if row<2 else 1.0
				var prop={"id":"tidal_pump" if item==0 else "tidal_monitor","rect":Rect2(centers[col]-Vector2(42,26),Vector2(84,52)),"registration":{}}
				var canvas=preload("res://scripts/room_content_canvas.gd").new()
				root.add_child(canvas)
				canvas.draw_scale=1.2
				canvas.draw_origin=Vector2(60+240*col+120*item,100+200*row)-room._equipment_bounds(prop).get_center()*1.2
				canvas.submit(room,[{"kind":"prop","prop":prop}])
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png(folder+"/retained.png")==OK)
	room.free(); quit()
