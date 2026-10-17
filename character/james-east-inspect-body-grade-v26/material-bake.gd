extends SceneTree
const OUT="res://character/james-east-inspect-body-grade-v26/"
const SOURCE="res://character/james-tablet-east-matte-v3/"
var failures:=0
var checks:=0
var records:Array=[]
func _initialize():call_deferred("run")
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func selected(pixel:Color,point:Vector2i) -> bool:
 if pixel.a<=0 or point.x<56 or point.x>=110 or point.y<24 or point.y>=172:return false
 var r:=roundi(pixel.r*255.);var g:=roundi(pixel.g*255.);var b:=roundi(pixel.b*255.)
 # Continuous violet selection, not semantic hair/fabric segmentation.
 return minf(r,b)-g>2.0 and absf(r-b)<20.0 and r+g+b>48
func run():
 if DisplayServer.get_name()=="headless" or not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
 var view:=SubViewport.new();view.size=Vector2i(184,184);view.transparent_bg=true;view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
 var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;view.add_child(sprite)
 var material:=ShaderMaterial.new();material.shader=load(OUT+"body-material.gdshader");sprite.material=material
 var bare_pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(SOURCE+"bare-manifest.json"))
 var bare_state:Dictionary=bare_pack.states.filter(func(s):return s.id=="inspect-east")[0]
 for mode in ["bare","helmet"]:
  var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(SOURCE+mode+"-manifest.json"))
  var state:Dictionary=pack.states.filter(func(s):return s.id=="inspect-east")[0]
  var paths:Array=[]
  var dir:String=OUT+"candidate-frames/"+mode;DirAccess.make_dir_recursive_absolute(dir)
  for i in range(state.frameFiles.size()):
   var original:=Image.load_from_file(SOURCE.path_join(state.frameFiles[i]));original.convert(Image.FORMAT_RGBA8)
   var bare:=Image.load_from_file(SOURCE.path_join(bare_state.frameFiles[i]));bare.convert(Image.FORMAT_RGBA8)
   var protection:=Image.create(184,184,false,Image.FORMAT_RGBA8);protection.fill(Color(0,0,0,1))
   if mode=="helmet":
    for y in range(184):
     for x in range(184):
      if original.get_pixel(x,y)!=bare.get_pixel(x,y):protection.set_pixel(x,y,Color(1,0,0,1))
   material.set_shader_parameter("protected_pixels",ImageTexture.create_from_image(protection))
   sprite.texture=ImageTexture.create_from_image(original);material.set_shader_parameter("apply_correction",i>0 and i<140)
   await process_frame;await RenderingServer.frame_post_draw
   var rendered:=view.get_texture().get_image();rendered.convert(Image.FORMAT_RGBA8)
   var output:Image=original.duplicate();var edited:=0;var marked:=0;var alpha_difference:=0
   for y in range(184):
    for x in range(184):
     var at:=Vector2i(x,y);var before:=original.get_pixelv(at);var after:=rendered.get_pixelv(at)
     alpha_difference=maxi(alpha_difference,absi(roundi(before.a*255)-roundi(after.a*255)))
     var r:=roundi(before.r*255);var g:=roundi(before.g*255);var b:=roundi(before.b*255)
     var spill:bool=10*g>13*r and 10*g>13*b and g>70
     if i>0 and i<140 and selected(before,at) and protection.get_pixelv(at).r<.5:
      marked+=1;after.a=before.a;output.set_pixelv(at,after)
      if output.get_pixelv(at)!=before:edited+=1
   check(alpha_difference<=1,"Native offscreen alpha quantization <=1 "+mode+str(i))
   var orig:PackedByteArray=original.get_data();var baked:PackedByteArray=output.get_data()
   for pixel in range(184*184):
    check(orig[pixel*4+3]==baked[pixel*4+3],"Original alpha retained "+mode+str(i))
   if i in [0,140]:check(orig==baked,"Exact standing master endpoint")
   var path:String="candidate-frames/"+mode+"/"+str(i).pad_zeros(3)+".png";paths.append(path)
   check(output.save_png(OUT+path)==OK,"Baked material candidate saves")
   records.append({"mode":mode,"index":i,"markedPixels":marked,"changedPixels":edited,"sourceAlphaExact":true,"outsideMaterialSelectionExact":true,"nativeAlphaMaxDifference":alpha_difference})
  for s in pack.states:
   if s.id in ["inspect-east","interact-east"]:s.frameFiles=paths.duplicate()
   else:
    var new_paths:Array=[]
    for rel in s.frameFiles:new_paths.append("candidate-frames/"+mode+"/"+rel.get_file())
    s.frameFiles=new_paths
   s.provenance.materialProgram="Native smooth violet-chroma correction bounded to body/hair region, skin/amber excluded by chroma, shared helmet differences exact. Selected matte tablet sources preserved, original alpha/outside selector exact, endpoints exact. Not semantic segmentation."
  pack.name="James East source-preserving native material candidate "+mode;pack.status="staged_full_cycle_review_pending"
  var file:=FileAccess.open(OUT+mode+"-manifest.json",FileAccess.WRITE);file.store_string(JSON.stringify(pack,"  "))
 var evidence:=FileAccess.open(OUT+"material-bake-evidence.json",FileAccess.WRITE)
 evidence.store_string(JSON.stringify({"complete":true,"checks":checks,"failures":failures,"records":records,"productionInstalled":false,"scope":"Native editable material-program authoring, all282original images. Original alpha and all RGB outside bounded colour selection retained exactly; no geometry, UV, body fitting or timing changes. Render target alpha +/-1 compared then restored original byte. Actual normal loader/controller/native worksite admission remains pending."},"  "))
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  var uid:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES BODY MATERIAL BAKE: ",checks," checks; ",failures," failures;282frames")
 quit(1 if failures else 0)
