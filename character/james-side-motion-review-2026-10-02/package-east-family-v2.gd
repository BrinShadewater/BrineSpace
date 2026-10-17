extends SceneTree
const OUT="res://character/james-side-motion-review-2026-10-02/"
const SOURCE="res://character/james-cargo-material-joined-v1/"
func _initialize():call_deferred("run")
func run():
 if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
 var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(SOURCE+"bare-manifest.json"))
 var prior:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"nine-head-package-evidence.json"))
 var bent:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"bent-v2-package-evidence.json"))
 var originals:Dictionary={};var candidates:Dictionary={};var windows:Dictionary={}
 var checks:=0;var failures:=0;var records:Array=[]
 for state in pack.states:
  if state.id in ["pickup-east","carry-east","unload-east"]:
   originals[state.id]=[]
   for path in state.frameFiles:
    var im:=Image.load_from_file(SOURCE.path_join(path));im.convert(Image.FORMAT_RGBA8);originals[state.id].append(im)
 candidates["carry-east"]=[];windows["carry-east"]=[]
 for i in range(6):
  var im:=Image.load_from_file(OUT+prior.records[i].candidate)
  # Remove original goggle pixels beyond the earlier30px extraction window.
  im.fill_rect(Rect2i(158,71,6,32),Color(0,0,0,0))
  candidates["carry-east"].append(im);windows["carry-east"].append(Rect2i(128,71,36,32))
 candidates["pickup-east"]=[originals["pickup-east"][0].duplicate()];windows["pickup-east"]=[Rect2i()]
 for i in range(3):
  candidates["pickup-east"].append(Image.load_from_file(OUT+bent.records[i].candidate))
  var w:Array=bent.records[i].window;windows["pickup-east"].append(Rect2i(w[0],w[1],w[2],w[3]))
 # One authored upright head reused at both held poses, with fixed collar placement.
 var atlas:=Image.load_from_file(OUT+"head-closeup-generated.png");atlas.convert(Image.FORMAT_RGBA8)
 var cell:=atlas.get_region(Rect2i(0,0,418,418));cell.resize(64,64,Image.INTERPOLATE_LANCZOS)
 var head:=cell.get_region(Rect2i(18,10,30,32));head.resize(25,29,Image.INTERPOLATE_LANCZOS)
 for i in [4,5]:
  var im:Image=originals["pickup-east"][i].duplicate();var w:=Rect2i(131,71,30,32)
  im.fill_rect(w,Color(0,0,0,0));im.blit_rect(head,Rect2i(0,0,25,29),Vector2i(133,74));candidates["pickup-east"].append(im);windows["pickup-east"].append(w)
 candidates["unload-east"]=[];windows["unload-east"]=[]
 for i in range(6):
  checks+=1
  if originals["pickup-east"][5-i].get_data()!=originals["unload-east"][i].get_data():failures+=1
  candidates["unload-east"].append(candidates["pickup-east"][5-i].duplicate());windows["unload-east"].append(windows["pickup-east"][5-i])
 var selected:Array=[]
 DirAccess.make_dir_recursive_absolute(OUT+"east-family-v2")
 for state in pack.states:
  if not candidates.has(state.id):continue
  var paths:Array=[]
  for i in range(6):
   var im:Image=candidates[state.id][i];im.convert(Image.FORMAT_RGBA8);var original:Image=originals[state.id][i];var w:Rect2i=windows[state.id][i]
   for y in range(256):
    for x in range(256):
     if not w.has_point(Vector2i(x,y)):
      checks+=1
      if im.get_pixel(x,y)!=original.get_pixel(x,y):failures+=1
   var path:String="east-family-v2/"+state.id+"-"+str(i).pad_zeros(3)+".png";im.save_png(OUT+path);paths.append(path)
   records.append({"key":state.id,"index":i,"source":SOURCE.path_join(state.frameFiles[i]),"candidate":path,"window":[w.position.x,w.position.y,w.size.x,w.size.y]})
  state=state.duplicate(true);state.frameFiles=paths;state.provenance["headRepair"]="Generated upright and bent head/collar sources, explicit local source extraction/fit; original RGBA outside recorded window retained. Pickup/unload exact reverse sources reused; original clocks/registration. Staged bare only; helmet/turn joins pending."
  selected.append(state)
 pack=pack.duplicate(true);pack.states=selected;pack.name="James East cargo head family v2 staged bare";pack.status="staged_bare_family_review_pending_helmet_turn_joins"
 var manifest:=FileAccess.open(OUT+"east-family-v2-bare-manifest.json",FileAccess.WRITE);manifest.store_string(JSON.stringify(pack,"  "))
 var report:=FileAccess.open(OUT+"east-family-v2-evidence.json",FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"status":"unselected bare family candidate","scope":"All18East pickup/carry/unload slots; exact original RGBA outside recorded rectangles and exact six reverse aliases. Source clocks/pivot/ruler preserved. Not paired helmet, turn admission, autonomous gameplay or full James acceptance."},"  "))
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  var file:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES EAST FAMILY V2: ",checks,"checks; ",failures,"failures;18unselected slots")
 quit(1 if failures else 0)
