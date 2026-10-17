extends SceneTree
const OUT="res://character/james-side-motion-review-2026-10-02/"
func _initialize():call_deferred("run")
func run():
 if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
 var old:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"nine-head-package-evidence.json"))
 var atlas:=Image.load_from_file(OUT+"bent-head-generated-v2.png");atlas.convert(Image.FORMAT_RGBA8)
 var checks:=0;var failures:=0;var records:Array=[]
 DirAccess.make_dir_recursive_absolute(OUT+"bent-head-candidates-v2")
 for i in range(3):
  var row:Dictionary=old.records[i+6]
  var source:=Image.load_from_file("res://"+str(row.source));source.convert(Image.FORMAT_RGBA8)
  var cell:=atlas.get_region(Rect2i(i*724,0,724,724));cell.resize(64,64,Image.INTERPOLATE_LANCZOS)
  var areas:Array=[Rect2i(17,12,32,35),Rect2i(22,14,30,33),Rect2i(21,12,30,35)]
  var head:=cell.get_region(areas[i]);head.resize(25,29,Image.INTERPOLATE_LANCZOS)
  var w:Array=row.window;var window:=Rect2i(w[0],w[1],w[2],w[3])
  var output:Image=source.duplicate();output.fill_rect(window,Color(0,0,0,0))
  var at:=Vector2i(row.placement[0],row.placement[1]);output.blit_rect(head,Rect2i(0,0,25,29),at)
  for y in range(256):
   for x in range(256):
    if not window.has_point(Vector2i(x,y)):
     checks+=1
     if output.get_pixel(x,y)!=source.get_pixel(x,y):failures+=1
  var file:String="bent-head-candidates-v2/"+row.key+"-"+str(row.index).pad_zeros(3)+".png";output.save_png(OUT+file)
  row=row.duplicate(true);row.candidate=file;row.generatedCell=[i*724,0,724,724];row.extract=[areas[i].position.x,areas[i].position.y,areas[i].size.x,areas[i].size.y];records.append(row)
 var report:=FileAccess.open(OUT+"bent-v2-package-evidence.json",FileAccess.WRITE)
 report.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"status":"three-pose unselected bent-pitch candidate","scope":"Explicit generated source cell extraction; original RGBA outside rectangles exact. Rectangles include collar pixels. Not full family/helmet/turn/native activity acceptance."},"  "))
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  var file:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES BENT V2: ",checks,"checks; ",failures,"failures; unselected")
 quit(1 if failures else 0)
