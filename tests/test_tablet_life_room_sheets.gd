extends SceneTree
const VIEWS=[preload("res://rooms/whole-room/hydroponics_view.gd"),preload("res://rooms/whole-room/reactor_view.gd"),preload("res://rooms/whole-room/med_bay_view.gd"),preload("res://rooms/whole-room/underwater_life_support_view.gd"),preload("res://rooms/whole-room/crew_hab_view.gd")]
var failures:=0
class PropCanvas extends Node2D:
 var renderer
 var prop:Dictionary
 var shell_only:=false
 func _draw():
  renderer.painter=self
  if shell_only:
   renderer.draw_wall(Rect2(-120,-70,240,12),true)
   renderer.draw_cap(Rect2(100,-80,12,12))
  else:renderer.draw_prop_base(prop)
  renderer.painter=renderer
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func view(script,preview:=false):
 var v=script.new();v.embedded=true;v.hide()
 if preview:v.set_meta("layout_editor_preview",true)
 root.add_child(v);v.set_process(false);v.machine_clock=0.5;return v
func settle():
 for i in 3:await process_frame
 await RenderingServer.frame_post_draw
func picture(v,p,shell:=false)->PackedByteArray:
 var vp=SubViewport.new();vp.size=Vector2i(384,384);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp)
 var canvas=PropCanvas.new();canvas.position=Vector2(192,192);canvas.renderer=v;canvas.prop=p;canvas.shell_only=shell;vp.add_child(canvas)
 await process_frame;await RenderingServer.frame_post_draw
 var im=vp.get_texture().get_image();check(im.get_used_rect().has_area(),"Original fallback visible")
 var bytes=im.get_data();vp.queue_free();await process_frame;return bytes
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 for script in VIEWS:
  root.set_meta("tablet_controls",false);var reference=view(script);await settle()
  var before=Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED)
  root.set_meta("tablet_controls",true);var tablet=view(script);await settle()
  var extra=Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED)-before
  print("TABLET_SHEET_ADDITION ",script.resource_path," bytes=",extra)
  check(extra<1024*1024,"Tablet constructor must defer unused equipment sheet: "+script.resource_path)
  var assigned=view(script);var replacement_image=Image.create(2,2,false,Image.FORMAT_RGBA8);replacement_image.fill(Color.GREEN);var assigned_texture=ImageTexture.create_from_image(replacement_image)
  assigned.life_texture=assigned_texture;check(assigned.life_texture==assigned_texture,"Assignment before first access overrides pending source");assigned.life_texture=null;check(assigned.life_texture==null,"Clearing explicit assignment does not reload old source");assigned.queue_free()
  for quarter in 4:
   tablet.quarter=quarter;reference.quarter=quarter;tablet.rebuild();reference.rebuild()
   var item:Dictionary=reference.life_items[0]
   var p={"id":item.id,"rect":item.rect,"registration":item,"center":Vector2.ZERO,"sort_y":item.rect.end.y}
   check(await picture(tablet,p)==await picture(reference,p.duplicate(true)),"Original equipment pixels exact: "+script.resource_path+" q"+str(quarter))
  check(await picture(tablet,{},true)==await picture(reference,{},true),"Legacy shell pixels exact: "+script.resource_path)
  var a=tablet.life_texture;check(a!=null and a.get_image().get_data()==reference.life_texture.get_image().get_data(),"First access keeps complete original source pixels")
  var second=tablet.life_texture;check(a==second,"Repeated access reuses uploaded sheet")
  var im=Image.create(2,2,false,Image.FORMAT_RGBA8);im.fill(Color.RED);var texture=ImageTexture.create_from_image(im)
  tablet.life_texture=texture;check(tablet.life_texture==texture,"Existing texture assignments retain their value")
  var preview=view(script,true);check(preview.get("_life_texture")!=null,"Tablet editor preview stays eager");preview.queue_free()
  tablet.queue_free();reference.queue_free();await settle()
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing original art")
 print("TABLET LIFE ROOM SHEETS failures=",failures);quit(1 if failures else 0)
