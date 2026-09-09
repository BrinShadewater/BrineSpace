extends SceneTree
const Effects=preload("res://rooms/full-wall-v1/rare_operating_effects.gd")
var room
var clock:=0.0
var working:=true
var q:=0
class Preview extends Node2D:
	func _draw() -> void:
		var test=get_tree()
		draw_rect(Rect2(0,0,600,600),Color("17282d"))
		test.room.configure_embedded(test.q,[],test.working,test.clock)
		test.room.render_into(self,Vector2(300,300),1.4)
func _init() -> void: call_deferred("run")
func frame(preview) -> Image:
	preview.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	return root.get_texture().get_image()
func run() -> void:
	preload("res://scripts/room_layout_store.gd").path="res://output/rare-effects-test/no-owner.json"
	DirAccess.make_dir_recursive_absolute("res://output/rare-effects-test")
	root.size=Vector2i(600,600); root.content_scale_size=root.size
	var preview:=Preview.new()
	for id in ["pressure_control","listening_post"]:
		room=load("res://rooms/full-wall-v1/"+id+"_view.gd").new()
		room.embedded=true; root.add_child(room); room.hide()
		if preview.get_parent()==null: root.add_child(preview)
		for rotation in range(4):
			q=rotation; working=true; clock=0.0
			var first:=await frame(preview)
			var instrument: Dictionary={}
			for prop in room.props:
				if Effects.owns(prop): instrument=prop; break
			assert(not instrument.is_empty())
			var before:=Effects.marks(room,instrument,id=="listening_post")
			assert(not before.is_empty())
			clock=3.0
			var second:=await frame(preview)
			assert(before!=Effects.marks(room,instrument,id=="listening_post"),"Instrument must advance")
			assert(first.get_data()!=second.get_data(),"Operating pixels must change")
			second.save_png("res://output/rare-effects-test/%s-q%d-on.png"%[id,q])
			working=false
			var off:=await frame(preview)
			assert(Effects.marks(room,instrument,id=="listening_post").is_empty(),"Offline must suppress effects")
			clock=8.0
			var off_later:=await frame(preview)
			assert(off.get_data()==off_later.get_data(),"Offline pixels must remain still")
			off.save_png("res://output/rare-effects-test/%s-q%d-off.png"%[id,q])
		room.free()
	preview.free()
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://rare-effects-test.loop"; game.meta.save_path="user://rare-effects-test.meta"
	root.add_child(game); current_scene=game; game.set_process(false); game.tick_timer.stop(); game.running=true
	game._set_paused(true,false)
	game.hide()
	room=load("res://rooms/full-wall-v1/listening_post_view.gd").new()
	room.embedded=true; root.add_child(room); room.hide()
	preview=Preview.new(); root.add_child(preview)
	q=2; working=true
	var frozen: float=game.get_visual_time_seconds()
	clock=frozen
	var paused_before:=await frame(preview)
	game._process(3.0)
	assert(game.get_visual_time_seconds()==frozen,"Owning clock must freeze while paused")
	clock=game.get_visual_time_seconds()
	var paused_after:=await frame(preview)
	assert(paused_before.get_data()==paused_after.get_data(),"Pause must freeze rendered machinery")
	game._set_paused(false,false); game._process(3.0)
	assert(game.get_visual_time_seconds()>frozen,"Owning clock must resume")
	clock=game.get_visual_time_seconds()
	var resumed:=await frame(preview)
	assert(resumed.get_data()!=paused_after.get_data(),"Resume must advance rendered machinery")
	print("RARE EFFECTS PASS: two rooms x four rotations; motion, offline pixel stability, owning pause/resume clock")
	quit()
