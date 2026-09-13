extends SceneTree

const DroneArt=preload("res://scripts/drone_art.gd")

class Preview extends Node2D:
	func _draw() -> void:
		var states=[
			{"center":Vector2(150,155),"working":false,"travelling":false},
			{"center":Vector2(450,155),"working":false,"travelling":true},
			{"center":Vector2(750,155),"working":true,"travelling":false},
		]
		for state in states:
			DroneArt.draw_drone(self,"construction",state.center,220,1.25,state.working,state.travelling)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	root.size=Vector2i(900,320)
	root.content_scale_size=root.size
	var background=ColorRect.new()
	background.size=root.size
	background.color=Color("273233")
	root.add_child(background)
	root.add_child(Preview.new())
	await process_frame
	await RenderingServer.frame_post_draw
	var folder="res://output/construction-owner-repair-2026-09-12/drone-material/states"
	DirAccess.make_dir_recursive_absolute(folder)
	assert(root.get_texture().get_image().save_png(folder+"/docked-travelling-working.png")==OK)
	var uid_path="res://tools/capture_construction_drone_material_states.gd.uid"
	if not FileAccess.file_exists(uid_path):
		var uid_file=FileAccess.open(uid_path,FileAccess.WRITE)
		uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
		uid_file.close()
	print("CONSTRUCTION DRONE MATERIAL: docked, travelling and articulated working states")
	quit()
