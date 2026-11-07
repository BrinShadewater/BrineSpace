extends SceneTree
const Library=preload("res://scripts/room_asset_library.gd")
const VIEWS=[preload("res://rooms/power-expansion-v1/current_turbine_view.gd"),preload("res://rooms/power-expansion-v1/heat_recovery_view.gd"),preload("res://rooms/full-wall-v1/biomass_digester_view.gd"),preload("res://scripts/james_cargo_workshop.gd")]
var failures:=0
class PropCanvas extends Node2D:
 var renderer
 var prop:Dictionary
 var actor_only:=false
 func _draw():
  if renderer==null or (prop.is_empty() and not actor_only):return
  renderer.painter=self
  if actor_only:renderer.draw_actor()
  else:renderer.draw_registered_prop(prop)
  renderer.painter=renderer
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func hidden_view(script,preview:=false):
 var view=script.new();view.hide()
 if preview:view.set_meta("layout_editor_preview",true)
 root.add_child(view);view.set_process(false);view.machine_clock=0.5;return view
func picture(view,prop:Dictionary,actor_only:=false)->PackedByteArray:
 var vp:=SubViewport.new();vp.size=Vector2i(384,384);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp)
 var canvas:=PropCanvas.new();canvas.position=Vector2(192,192);canvas.renderer=view;canvas.prop=prop;canvas.actor_only=actor_only;vp.add_child(canvas)
 await process_frame;await RenderingServer.frame_post_draw
 var image:=vp.get_texture().get_image();check(image.get_used_rect().has_area(),"Fallback draws visible original pixels")
 var bytes:=image.get_data();vp.queue_free();await process_frame;return bytes
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 for script in VIEWS:
  root.set_meta("tablet_controls",true)
  var tablet=hidden_view(script)
  if "machine_texture" in tablet:check(tablet.machine_texture==null,"Tablet must not upload unused legacy power machine: "+str(tablet.room_id))
  if "north_bench_art" in tablet:
   check(tablet.textures.is_empty(),"Tablet must not upload unused legacy workshop sheets")
   check(tablet.north_bench_art.get("library_texture")==null,"Workshop keeps directional bench metadata without texture")
  var tablet_props=tablet.props.duplicate(true)
  for prop in tablet_props:
   if prop.get("id","")=="power_machine" and prop.get("library_asset",false):check(prop.get("library_texture")==null,"Retired directional power defaults stay metadata-only")
  root.set_meta("tablet_controls",false)
  var reference=hidden_view(script)
  if "machine_texture" in reference:check(reference.machine_texture!=null,"Desktop preserves eager machine art")
  if "north_bench_art" in reference:check(reference.textures.size()==2,"Desktop preserves eager workshop art")
  for quarter in 4:
   root.set_meta("tablet_controls",true);tablet.quarter=quarter;tablet.rebuild()
   root.set_meta("tablet_controls",false);reference.quarter=quarter;reference.rebuild()
   var wanted="power_machine" if "machine_texture" in tablet else "bench"
   var a:Dictionary={};var b:Dictionary={}
   for prop in tablet.props:
    if prop.id==wanted:a=prop.duplicate(true)
   for prop in reference.props:
    if prop.id==wanted:b=prop.duplicate(true)
   check(not a.is_empty() and not b.is_empty(),"Original fallback registration remains available")
   var original:PackedByteArray=await picture(reference,b)
   root.set_meta("tablet_controls",true)
   check(await picture(tablet,a)==original,"Native fallback pixels exact: "+str(script.resource_path)+" q"+str(quarter))
  if "north_bench_art" in tablet:
   for id in ["bench","tote"]:
    var a:Dictionary={};var b:Dictionary={}
    for prop in tablet.props:
     if prop.id==id:a=prop.duplicate(true)
    for prop in reference.props:
     if prop.id==id:b=prop.duplicate(true)
    a.erase("overhead_furnishing");b.erase("overhead_furnishing")
    var original:PackedByteArray=await picture(reference,b)
    check(await picture(tablet,a)==original,"Explicit legacy workshop pixels exact: "+id)
    check(tablet.textures.has(id),"Explicit fallback loads requested legacy sheet: "+id)
   tablet.external_actor_texture=GradientTexture2D.new();reference.external_actor_texture=tablet.external_actor_texture
   tablet.actor=Vector2.ZERO;tablet.carriers=[Vector2.ZERO];tablet.show_actor=false
   reference.actor=Vector2.ZERO;reference.carriers=[Vector2.ZERO];reference.show_actor=false
   check(await picture(tablet,{},true)==await picture(reference,{},true),"Carried tote keeps original native pixels")
  if "machine_texture" in tablet:
   var a={"id":"power_machine","rect":Rect2(-135,24,270,88),"registration":{}}
   check(await picture(tablet,a)==await picture(reference,a.duplicate(true)),"Explicit raw machine fallback pixels exact")
   check(tablet.machine_texture!=null,"Explicit raw machine draw uploads original texture")
  root.set_meta("tablet_controls",true)
  var preview=hidden_view(script,true)
  if "machine_texture" in preview:check(preview.machine_texture!=null,"Editor preview preserves eager machine art")
  if "north_bench_art" in preview:check(preview.textures.size()==2 and preview.north_bench_art.library_texture!=null,"Editor preview preserves eager workshop art")
  preview.queue_free();await process_frame
  tablet.queue_free();reference.queue_free();await process_frame
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"All original fallback art remains available")
 print("TABLET LEGACY ROOM ART failures=",failures);quit(1 if failures else 0)
