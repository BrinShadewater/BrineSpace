extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
class FallbackCanvas extends Grid:
 func _ready():draw_target=self;set_process(false)
 func _get_main():return self
 func get_visual_time_seconds():return 0.5
 func _draw():_draw_brine_core_overlay(Rect2(0,0,256,256))
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func picture(eager:bool)->Dictionary:
 var vp:=SubViewport.new();vp.size=Vector2i(256,256);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp)
 var canvas:=FallbackCanvas.new()
 if eager:canvas._load_brine_core_overlays()
 vp.add_child(canvas)
 await process_frame;await RenderingServer.frame_post_draw
 var pixels:=vp.get_texture().get_image().get_data()
 var count:=canvas.brine_core_overlays.size()
 vp.queue_free();await process_frame
 return {"pixels":pixels,"count":count}
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 root.set_meta("tablet_controls",true)
 var game=load("res://scenes/main.tscn").instantiate()
 game.run_save_path="user://fixture.loop";game.meta.save_path="user://fixture.meta";game.Preferences.save_path="user://fixture.cfg"
 root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game._set_paused(true,false)
 check(game.grid_view._uses_layered_art({"id":"brine_core"}),"Actual core uses layered artwork")
 check(game.grid_view.brine_core_overlays.is_empty(),"Tablet must not retain unused legacy BRINE overlays")
 check(game.grid_view.space_background_texture==null,"Tablet must not retain unused legacy space image")
 game.queue_free();await process_frame
 root.set_meta("tablet_controls",false)
 var reference:Dictionary=await picture(true)
 root.set_meta("tablet_controls",true)
 var fallback:Dictionary=await picture(false)
 check(reference.count==5 and fallback.count==5,"Explicit legacy draw still loads all original fallback textures")
 check(reference.pixels==fallback.pixels,"Lazy legacy overlay exactly matches eager native pixels")
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"Original artwork remains available")
 print("TABLET LEGACY OVERLAY STORAGE failures=",failures)
 quit(1 if failures else 0)
