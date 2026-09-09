extends SceneTree
var room
var clock:=0.0
var working:=true
var q:=0
class Preview extends Node2D:
	func _draw() -> void:
		var t=get_tree()
		draw_rect(Rect2(0,0,600,600),Color("17282d"))
		t.room.configure_embedded(t.q,[],t.working,t.clock)
		t.room.render_into(self,Vector2(300,300),1.4)
func _init() -> void: call_deferred("run")
func frame(preview) -> Image:
	preview.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	return root.get_texture().get_image()
func bank_pixels(image: Image) -> PackedByteArray:
	var data:=PackedByteArray()
	for prop in room.props:
		if not prop.get("full_wall",false) or not room.is_animated_prop(prop): continue
		var box: Rect2=room.prop_visual_bounds(prop)
		var region:=Rect2i(Vector2(300,300)+box.position*1.4,box.size*1.4)
		data.append_array(image.get_region(region).get_data())
	assert(not data.is_empty())
	return data
func run() -> void:
	preload("res://scripts/room_layout_store.gd").path="res://output/rollout-effects/no-owner.json"
	DirAccess.make_dir_recursive_absolute("res://output/rollout-effects")
	root.size=Vector2i(600,600);root.content_scale_size=root.size
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://rollout-effects.loop";game.meta.save_path="user://rollout-effects.meta"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop();game.running=true;game.hide()
	await process_frame
	await process_frame
	root.size=Vector2i(600,600);root.content_scale_size=root.size
	for child in game.find_children("*","CanvasLayer",true,false): child.hide()
	var preview:=Preview.new()
	root.add_child(preview)
	for id in ["life_support","biomass_digester","command_center"]:
		room=load("res://rooms/full-wall-v1/"+id+"_view.gd").new()
		room.embedded=true;root.add_child(room);room.hide()
		for rotation in range(4):
			q=rotation;working=true;clock=0
			var first:=bank_pixels(await frame(preview))
			clock=1.1
			var second:=await frame(preview)
			assert(first!=bank_pixels(second),id+" bank operating pixels must change")
			second.save_png("res://output/rollout-effects/%s-q%d-on.png"%[id,q])
			working=false
			var off:=bank_pixels(await frame(preview))
			clock=4.7
			assert(off==bank_pixels(await frame(preview)),id+" offline bank pixels must stay still")
			working=true;game._set_paused(true,false)
			clock=game.get_visual_time_seconds()
			var frozen: float=clock
			var paused_pixels:=bank_pixels(await frame(preview))
			game._process(1.1);clock=game.get_visual_time_seconds()
			assert(clock==frozen)
			assert(paused_pixels==bank_pixels(await frame(preview)),id+" paused bank pixels must stay still")
			game._set_paused(false,false);game._process(1.1);clock=game.get_visual_time_seconds()
			assert(clock>frozen)
			assert(paused_pixels!=bank_pixels(await frame(preview)),id+" resumed bank pixels must change")
		room.free()
	preview.queue_free()
	game.queue_free()
	await process_frame
	await RenderingServer.frame_post_draw
	print("ROLLOUT EFFECTS PASS: 3 rooms x 4 orientations; new bank pixels animate, offline stability, owning pause/resume clock")
	quit()
