extends SceneTree
const CONTRACT="res://character/james-diagnostics-edge-study-v29/source-contract.json"
const SHADER="res://character/james-diagnostics-edge-study-v29/edge-material.gdshader"
const OUT="res://character/james-diagnostics-edge-study-v29/"
var checks:=0
var failures:=0
func check(ok:bool,why:String):
 checks+=1
 if not ok:failures+=1;push_error(why)
func _initialize():call_deferred("run")
func run():
 var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
 if DisplayServer.get_name()=="headless" or OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
 var viewport:=SubViewport.new();viewport.size=Vector2i(184,184);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
 var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;viewport.add_child(sprite)
 var material:=ShaderMaterial.new();material.shader=load(SHADER);sprite.material=material
 var contract:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(CONTRACT));var records:Array=[]
 DirAccess.make_dir_recursive_absolute(OUT+"frames")
 for row in contract.records:
  var source:=Image.load_from_file(row.source);source.convert(Image.FORMAT_RGBA8)
  check(source.get_size()==Vector2i(184,184),"Declared source canvas")
  var mask:=Image.create(184,184,false,Image.FORMAT_RGBA8);mask.fill(Color(0,0,0,1));var selected:=0
  for y in range(184):
   for x in range(184):
    var before:=source.get_pixel(x,y);var rr:=roundi(before.r*255);var gg:=roundi(before.g*255);var bb:=roundi(before.b*255);var aa:=roundi(before.a*255)
    if aa==0 or 10*gg<=13*rr or 10*gg<=13*bb or gg<=20:continue
    var edge:bool=aa<128
    if not edge:
     for dy in [-1,0,1]:
      for dx in [-1,0,1]:
       var nx:int=x+dx;var ny:int=y+dy
       if nx<0 or nx>=184 or ny<0 or ny>=184 or roundi(source.get_pixel(nx,ny).a*255)==0:edge=true
    if edge:mask.set_pixel(x,y,Color(1,0,0,1));selected+=1
  sprite.texture=ImageTexture.create_from_image(source);material.set_shader_parameter("admission_pixels",ImageTexture.create_from_image(mask))
  await process_frame;await RenderingServer.frame_post_draw
  var rendered:=viewport.get_texture().get_image();rendered.convert(Image.FORMAT_RGBA8);var output:Image=source.duplicate();var changed:=0
  for y in range(184):
   for x in range(184):
    if mask.get_pixel(x,y).r<.5:continue
    var original:=source.get_pixel(x,y);var after:=rendered.get_pixel(x,y)
    # Retain exact original R/B/alpha. Only admitted native material green output.
    output.set_pixel(x,y,Color(original.r,after.g,original.b,original.a))
    if output.get_pixel(x,y)!=original:changed+=1
  var path:String="frames/"+row.mode+"-"+row.direction+"-"+str(row.slot).pad_zeros(3)+".png"
  check(output.save_png(OUT+path)==OK,"Native material study saved")
  records.append({"mode":row.mode,"direction":row.direction,"slot":row.slot,"source":row.source,"candidate":OUT+path,"selectedPixels":selected,"changedPixels":changed})
 var evidence:=FileAccess.open(OUT+"native-evidence.json",FileAccess.WRITE);evidence.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"normalChanged":false,"scope":"18 representative native green-channel material studies. Original R/B/alpha and all RGB outside byte-defined edge admission retained. Not all864sources or runtime/room acceptance."},"  "))
 for path in [get_script().resource_path,SHADER]:
  if not FileAccess.file_exists(path+".uid"):
   var file:=FileAccess.open(path+".uid",FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES EDGE STUDY: ",checks," checks; ",failures," failures;18sources")
 quit(1 if failures else 0)
