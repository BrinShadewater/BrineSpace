extends SceneTree
const OUT="res://character/james-side-motion-review-2026-10-02/"
func _initialize():call_deferred("run")
func run():
 if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
 var layout:Array=JSON.parse_string(FileAccess.get_file_as_string(OUT+"turn-head-layout.json"))
 var atlas:=Image.load_from_file(OUT+"turn-head-generated-v3.png");atlas.convert(Image.FORMAT_RGBA8)
 assert(atlas.get_size()==Vector2i(1629,965))
 DirAccess.make_dir_recursive_absolute(OUT+"turn-head-v3")
 var records:Array=[];var checks:=0;var failures:=0
 for n in range(6):
  var source:String="res://"+layout[n].source;var original:=Image.load_from_file(source);original.convert(Image.FORMAT_RGBA8)
  var rect:=Rect2i((n%3)*543+114,(0 if n<3 else 482)+(171 if n<3 else 106),270,288)
  var head:=atlas.get_region(rect)
  # Remove sub32 alpha dust in generated transparent area before scale fitting.
  var dust:=0
  for y in range(head.get_height()):
   for x in range(head.get_width()):
    var c:=head.get_pixel(x,y)
    if c.a<32.0/255.0 and c.a>0.0:head.set_pixel(x,y,Color(0,0,0,0));dust+=1
  head.resize(25,29,Image.INTERPOLATE_LANCZOS)
  var window:=Rect2i(128,71,36,32);var candidate:=original.duplicate()
  candidate.fill_rect(window,Color(0,0,0,0));candidate.blit_rect(head,Rect2i(0,0,25,29),Vector2i(130,74))
  for y in range(256):
   for x in range(256):
    if not window.has_point(Vector2i(x,y)):
     checks+=1
     if candidate.get_pixel(x,y)!=original.get_pixel(x,y):failures+=1
  var path:String="turn-head-v3/"+layout[n].state+"-"+str(layout[n].index).pad_zeros(3)+".png";candidate.save_png(OUT+path)
  records.append({"state":layout[n].state,"index":layout[n].index,"source":source,"candidate":path,"rawRect":[rect.position.x,rect.position.y,270,288],"window":[128,71,36,32],"placement":[130,74],"headSize":[25,29],"alphaDustCleared":dust})
 var report:=FileAccess.open(OUT+"turn-head-v3-package-evidence.json",FileAccess.WRITE)
 report.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"selected":false,"scope":"Six generated head/neck extractions into original turn sources, exact original RGBA outside rectangular collar/head window. Not shared aliases, full turn manifests, runtime admission or motion acceptance."},"  "))
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  var f:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES TURN HEAD V3: ",checks,"checks; ",failures,"failures;6unselected sources")
 quit(1 if failures else 0)
