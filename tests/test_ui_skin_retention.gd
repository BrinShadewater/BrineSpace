extends SceneTree
const Hull=preload("res://scripts/ui_hull_style.gd")
const Component=preload("res://scripts/ui_component_style.gd")
class MultiSkin extends Node2D:
 var style:StyleBox
 var first_width:=240.0
 func _draw():
  style.draw(get_canvas_item(),Rect2(0,0,first_width,100))
  style.draw(get_canvas_item(),Rect2(240,0,160,100))
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func image(view:SubViewport)->Image:return view.get_texture().get_image()
func exercise(script:Script,kind:String,internal:=false):
 var view:=SubViewport.new();view.size=Vector2i(400,100);view.disable_3d=true;view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
 var panel:=Panel.new();panel.size=Vector2(240,100);var style=script.new();panel.add_theme_stylebox_override("panel",style);view.add_child(panel,false,Node.INTERNAL_MODE_FRONT if internal else Node.INTERNAL_MODE_DISABLED)
 var second:=Panel.new();second.size=Vector2(160,100);second.position=Vector2(240,0);second.add_theme_stylebox_override("panel",style);view.add_child(second)
 await process_frame;await RenderingServer.frame_post_draw
 var before:=image(view).get_data()
 image(view).save_png("user://skin-"+kind+"-before.png")
 # Eviction must not invalidate retained canvas commands which haven't redrawn.
 if kind=="hull":Hull._art.clear()
 else:Component.artwork.clear()
 await process_frame;await RenderingServer.frame_post_draw
 check(before==image(view).get_data(),kind+" skin stays rendered after shared lookup eviction")
 image(view).save_png("user://skin-"+kind+"-after.png")
 if style.get("skin_lease")!=null:
  check(style.skin_lease.textures.size()==2,kind+" shared style holds each live drawing canvas")
  var old:WeakRef=weakref(style.skin_lease.textures[panel.get_canvas_item()].values()[0])
  panel.size.x=220
  await process_frame;await RenderingServer.frame_post_draw
  check(style.skin_lease.textures.size()==2,kind+" resize replaces its lease rather than accumulating old sizes")
  check(old.get_ref()==null,kind+" obsolete skin is freed despite lookup metadata")
  panel.queue_free()
  while is_instance_valid(panel):await process_frame
  check(style.skin_lease.textures.size()==1,kind+" freed canvas releases its texture")
 if not internal:
  second.queue_free()
  while is_instance_valid(second):await process_frame
  var multi:=MultiSkin.new();multi.style=style;view.add_child(multi)
  await process_frame;await RenderingServer.frame_post_draw
  check(before==image(view).get_data(),kind+" one canvas retains all differently sized skin draws")
  var stale:WeakRef=weakref(style.skin_lease.textures[multi.get_canvas_item()].values()[0])
  multi.first_width=200;multi.queue_redraw()
  await process_frame;await RenderingServer.frame_post_draw
  check(stale.get_ref()==null and style.skin_lease.textures[multi.get_canvas_item()].size()==2,kind+" next canvas draw replaces obsolete textures without losing current ones")
 view.queue_free()
 while is_instance_valid(view):await process_frame
 if style.get("skin_lease")!=null:check(style.skin_lease.textures.is_empty(),kind+" scene exit releases all leases")
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 await exercise(Hull,"hull");await exercise(Component,"component");await exercise(Component,"internal",true)
 root.gui_embed_subwindows=true
 var popup:=PopupMenu.new();var popup_style=Component.new()
 popup.add_theme_stylebox_override("panel",popup_style)
 popup.add_item("Short");popup.add_item("A much longer item")
 root.add_child(popup);popup.popup(Rect2i(20,20,260,130))
 await process_frame;await RenderingServer.frame_post_draw
 check(not popup_style.skin_lease.textures.is_empty(),"Real PopupMenu internal panel draws with retained skin")
 popup.queue_free()
 while is_instance_valid(popup):await process_frame
 check(popup_style.skin_lease.textures.is_empty(),"Real PopupMenu destruction releases internal canvas leases")
 print("UI SKIN RETENTION failures=",failures)
 quit(1 if failures else 0)
