extends SceneTree
## Historical early study only. Final shader requires the per-frame protected_pixels
## binding supplied by material-bake.gd. Use that exporter for current reproduction;
## native-material captures predate final helmet protection and tablet selection.
const OUT="res://character/james-tablet-east-matte-v3/"
const SOURCE="res://character/james-tablet-east-belt-fixed-source-v2/"
var failures:=0
var records:Array=[]
func _initialize():call_deferred("run")
func check(ok:bool,message:String):
 if not ok:failures+=1;push_error(message)
func run():
 if DisplayServer.get_name()=="headless" or not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
 root.size=Vector2i(800,500)
 root.content_scale_size=Vector2i(800,500)
 var background:=ColorRect.new();background.color=Color("303b40");background.size=Vector2(800,500);root.add_child(background)
 var label:=Label.new();label.text="James East material program study: master / selected / staged colour";label.position=Vector2(12,8);root.add_child(label)
 for mode in ["bare","helmet"]:
  var data:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(SOURCE+mode+"-manifest.json"))
  var state:Dictionary=data.states.filter(func(s):return s.id=="inspect-east")[0]
  var sprites:Array=[]
  for col in range(3):
   var sprite:=Sprite2D.new();sprite.centered=false;sprite.position=Vector2(50+col*240,40+(200 if mode=="helmet" else 0));sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sprite);sprites.append(sprite)
  var master:=Image.load_from_file(SOURCE.path_join(state.frameFiles[0]));sprites[0].texture=ImageTexture.create_from_image(master)
  var material:=ShaderMaterial.new();material.shader=load(OUT+"material-study.gdshader");sprites[2].material=material
  var dir:String=OUT+"native-material/"+mode;DirAccess.make_dir_recursive_absolute(dir)
  for i in range(state.frameFiles.size()):
   var im:=Image.load_from_file(SOURCE.path_join(state.frameFiles[i]));check(im!=null,"Selected source loads")
   var texture:=ImageTexture.create_from_image(im);sprites[1].texture=texture;sprites[2].texture=texture
   material.set_shader_parameter("apply_correction",i>0 and i<state.frameFiles.size()-1)
   await process_frame;await RenderingServer.frame_post_draw
   if i in [0,20,40,60,80,83,100,120,140]:
    var file:String=dir+"/"+str(i).pad_zeros(3)+".png";check(root.get_texture().get_image().save_png(file)==OK,"Native material study capture")
    records.append({"mode":mode,"index":i,"capture":file})
  for sprite in sprites:sprite.queue_free()
  await process_frame
 var evidence:=FileAccess.open(OUT+"native-material-evidence.json",FileAccess.WRITE)
 evidence.store_string(JSON.stringify({"complete":true,"failures":failures,"sourceSlotsRendered":282,"records":records,"productionInstalled":false,"scope":"Standalone native colour-program study,282original textures rendered through shader,18sample captures. Not normal player/actor/task/Continue or full revised source admission. Fixed green channel clamp and bounded pale-violet equipment colour selection; no alpha or UV changes in shader. Pixel-level baked alpha/source geometry validation still required before production use."},"  "))
 for path in [get_script().resource_path,OUT+"material-study.gdshader"]:
  if not FileAccess.file_exists(path+".uid"):
   var uid:=FileAccess.open(path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES MATERIAL STUDY:282source slots; ",failures," failures;18captures")
 quit(1 if failures else 0)
