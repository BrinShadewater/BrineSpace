extends SceneTree
const Grain=preload("res://rooms/whole-room/room_floor.gd")
const Tiles=preload("res://rooms/whole-room/modular_floor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const Views=[preload("res://rooms/full-wall-v1/life_support_view.gd"),preload("res://rooms/full-wall-v1/hydroponics_bay_view.gd"),preload("res://rooms/full-wall-v1/crew_hab_view.gd")]
var checks:=0
var failures:=0
class Surface extends Node2D:
	var view:Node
	var factor:=1.0
	var origin:=Vector2(256,256)
	func _draw():
		draw_set_transform(origin,0,Vector2.ONE*factor)
		Grain.draw_profile_floor(view,self,Vector2.ZERO)
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace("\\","/"):
		push_error("Profile-floor test requires isolated user directory");quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	var capture:=SubViewport.new();capture.size=Vector2i(512,512);capture.transparent_bg=true
	capture.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(capture)
	var surface:=Surface.new();capture.add_child(surface)
	for script in Views:
		var view=script.new();view.embedded=true;root.add_child(view);view.hide()
		surface.view=view
		check(not Grain.profile_for(view).is_empty(),"Actual floor profile")
		if Grain.profile_for(view).is_empty():quit(1);return
		for quarter in range(4):
			view.configure_embedded(quarter,[],true,0.0)
			for tiled in [true,false]:
				Tiles.enabled=tiled
				for scale_value in [0.73,1.0]:
					surface.factor=scale_value;surface.origin=Vector2(256.5,256.5)
					for edited in [false,true]:
						view.set_meta("layout_draft",{"tile/0/0":[2,1],"floor/material/1/1":2} if edited else {})
						Grain.department_grains.clear();Grain.load_unused_profile_grain=false
						surface.queue_redraw();await frame()
						var candidate:Image=capture.get_texture().get_image()
						check(Grain.department_grains.is_empty()==tiled,"Only legacy drawing loads a legacy image")
						check(not candidate.is_invisible(),"Selected floor visibly rendered")
						Grain.load_unused_profile_grain=true;surface.queue_redraw();await frame()
						check(not Grain.department_grains.is_empty(),"Reference reproduces original extra upload")
						check(candidate.get_data()==capture.get_texture().get_image().get_data(),"Exact floor pixels: q%d tiled%s scale%s edited%s"%[quarter,tiled,scale_value,edited])
		view.queue_free();surface.view=null;await frame()
	Grain.load_unused_profile_grain=false;Tiles.enabled=true
	capture.queue_free();await frame()
	print("PROFILE FLOOR LOADING: %d checks; %d failures"%[checks,failures]);quit(1 if failures else 0)
