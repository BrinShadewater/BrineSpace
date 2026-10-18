extends SceneTree
const Dressing=preload("res://rooms/whole-room/room_dressing.gd")
class Host extends Node2D:
 var life_items:Array=[]
 var props:Array=[]
 var operating:=false
 var dressing
 var prop:Dictionary={}
 var texture_key:String
 var painter:CanvasItem=self
 func life_point(_prop:Dictionary,point:Vector2)->Vector2:return point*0.15
 func _draw():
  if dressing!=null and not prop.is_empty() and not texture_key.is_empty():dressing.draw_sprite(prop,texture_key)
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func host_in(view:SubViewport)->Host:
 var host:=Host.new();view.add_child(host);return host
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var path:="res://rooms/underwater/batch-two/cryo-composition-v3.json"
 root.set_meta("tablet_controls",true)
 var viewport:=SubViewport.new();viewport.size=Vector2i(256,256);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
 var tablet:=host_in(viewport);tablet.dressing=Dressing.new(tablet,path)
 check(tablet.dressing.textures.is_empty(),"Tablet construction must retain registrations without loading unused dressing textures")
 check(not tablet.life_items.is_empty(),"Deferred dressing preserves furniture registration")
 var item:Dictionary=tablet.dressing.profile.furniture[0];tablet.prop={"registration":tablet.dressing.registration(item)};tablet.texture_key=item.texture
 tablet.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 var shown:=viewport.get_texture().get_image();var tablet_pixels:=shown.get_data();var shown_count:int=tablet.dressing.textures.size()
 check(shown.get_used_rect().has_area(),"Native comparison contains visible registered artwork")
 check(shown_count==1,"First dressing draw loads just the requested sheet")
 var source:Image=tablet.dressing.textures[item.texture].get_image();var original:=Image.new();original.load_png_from_buffer(FileAccess.get_file_as_bytes(tablet.dressing.profile.textures[item.texture]))
 check(source.get_data()==original.get_data(),"First-use source pixels remain exact")
 tablet.dressing.draw_supported(tablet.prop)
 check(tablet.dressing.textures.size()==shown_count,"Hidden supported editor props do not load art")
 tablet.queue_free();await process_frame
 root.set_meta("tablet_controls",false)
 var desktop:=host_in(viewport);desktop.dressing=Dressing.new(desktop,path)
 check(desktop.dressing.textures.size()==desktop.dressing.profile.textures.size(),"Desktop keeps eager composition loading")
 check(desktop.life_items.size()==item_count(path),"All original furniture registrations remain available")
 desktop.prop={"registration":desktop.dressing.registration(item)};desktop.texture_key=item.texture;desktop.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 check(viewport.get_texture().get_image().get_data()==tablet_pixels,"Tablet deferred and desktop eager drawing produce identical native pixels")
 desktop.queue_free();await process_frame
 root.set_meta("tablet_controls",true)
 var preview:=host_in(viewport);preview.set_meta("layout_editor_preview",true);preview.dressing=Dressing.new(preview,path)
 check(preview.dressing.textures.size()==preview.dressing.profile.textures.size(),"Explicit editor previews preserve eager source availability")
 preview.queue_free();await process_frame
 var pool=preload("res://scripts/crew_texture_pool.gd").new()
 var first:=host_in(viewport);first.set_meta("room_texture_pool",pool);first.dressing=Dressing.new(first,path)
 var second:=host_in(viewport);second.set_meta("room_texture_pool",pool);second.dressing=Dressing.new(second,path)
 check(first.dressing.textures.is_empty() and second.dressing.textures.is_empty(),"Shared pool stays lazy during tablet construction")
 var shared_a:Texture2D=first.dressing._texture(item.texture);var shared_b:Texture2D=second.dressing._texture(item.texture)
 check(is_same(shared_a,shared_b) and pool.stats.uploads==1,"First-use textures honor immutable pool sharing across rooms")
 check(is_same(shared_a,first.dressing._texture(item.texture)) and pool.stats.uploads==1,"Repeated first-use sheet lookup does not upload again")
 for key in first.dressing.profile.textures:
  var uploaded:Texture2D=first.dressing._texture(key);var original_image:=Image.new();original_image.load_png_from_buffer(FileAccess.get_file_as_bytes(first.dressing.profile.textures[key]))
  check(uploaded.get_image().get_data()==original_image.get_data(),"All lazily loaded composition pixels match source: "+key)
 viewport.queue_free();await process_frame
 print("TABLET DRESSING STORAGE failures=",failures)
 quit(1 if failures else 0)
func item_count(path:String)->int:return JSON.parse_string(FileAccess.get_file_as_string(path)).furniture.size()
