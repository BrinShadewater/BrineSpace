extends SceneTree
const Base=preload("res://rooms/whole-room/nursery_whole_view.gd")
const Connected=preload("res://rooms/whole-room/connected_rooms_view.gd")
const STORAGE=preload("res://rooms/production-ten/storage_bay_view.gd")
const LIFE="res://legacy/default/rooms/whole-room/life-support-candidate.png"
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func hidden(script,tablet:bool,preview:=false):
 root.set_meta("tablet_controls",tablet)
 var view=script.new();view.embedded=true;view.hide()
 if preview:view.set_meta("layout_editor_preview",true)
 root.add_child(view);view.set_process(false);return view
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 Base.shared_source_textures.clear()
 var tablet=hidden(STORAGE,true)
 check(not Base.shared_source_textures.has(Base.SOURCE),"Tablet inherited nursery sheet stays unuploaded")
 check(not Base.shared_source_textures.has(LIFE),"Tablet inherited life sheet stays unuploaded")
 var reference=hidden(STORAGE,false)
 check(Base.shared_source_textures.has(Base.SOURCE) and Base.shared_source_textures.has(LIFE),"Desktop retains both inherited eager uploads")
 check(tablet.texture.get_image().get_data()==reference.texture.get_image().get_data(),"Inherited nursery demand returns original pixels")
 check(tablet.texture==reference.texture,"Inherited source retains existing shared upload ownership")
 var old=ImageTexture.create_from_image(Image.create(2,3,false,Image.FORMAT_RGBA8));tablet.texture=old
 check(tablet.texture==old,"Explicit texture setter remains authoritative")
 for script in [Base,Connected]:
  Base.shared_source_textures.clear()
  var a=hidden(script,true)
  check(not Base.shared_source_textures.has(Base.SOURCE),"Standalone tablet inherited source remains lazy")
  if script==Connected:check(a._life_texture==null,"Connected tablet default life sheet remains lazy")
  var b=hidden(script,false)
  check(a.texture.get_image().get_data()==b.texture.get_image().get_data(),"Standalone base fallback pixels exact")
  if script==Connected:check(a.life_texture.get_image().get_data()==b.life_texture.get_image().get_data(),"Standalone life fallback pixels exact")
  var editor=hidden(script,true,true)
  check(editor._base_texture!=null,"Editor preview retains eager base source independently of shared cache")
  if script==Connected:check(editor._life_texture!=null,"Editor preview retains eager life source")
  a.queue_free();b.queue_free();editor.queue_free();await process_frame
 tablet.queue_free();reference.queue_free();await process_frame
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"Original sources remain available")
 print("TABLET BASE ROOM SOURCES failures=",failures);quit(1 if failures else 0)
