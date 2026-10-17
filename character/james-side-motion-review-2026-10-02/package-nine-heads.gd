extends SceneTree
const OUT="res://character/james-side-motion-review-2026-10-02/"
func _initialize():call_deferred("run")
func run():
 if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
 var layout:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"head-closeup-layout.json"))
 var atlas:=Image.load_from_file(OUT+"head-closeup-generated.png");atlas.convert(Image.FORMAT_RGBA8)
 var checks:=0;var failures:=0;var records:Array=[]
 DirAccess.make_dir_recursive_absolute(OUT+"head-candidates")
 for row in layout.cells:
  var i:int=row.cell
  var source:=Image.load_from_file("res://"+str(row.source));source.convert(Image.FORMAT_RGBA8)
  var cell:=atlas.get_region(Rect2i((i%3)*418,(i/3)*418,418,418));cell.resize(64,64,Image.INTERPOLATE_LANCZOS)
  var area:=Rect2i(18,10,30,32)
  if i==6:area=Rect2i(17,10,32,32)
  if i==7:area=Rect2i(22,10,30,32)
  if i==8:area=Rect2i(21,10,30,32)
  var window:=Rect2i(Vector2i(row.crop[0],row.crop[1])+area.position,area.size)
  var head:=cell.get_region(area);head.resize(25,29,Image.INTERPOLATE_LANCZOS)
  var output:Image=source.duplicate();output.fill_rect(window,Color(0,0,0,0))
  var at:Vector2i=window.position+Vector2i((window.size.x-25)/2,3)
  output.blit_rect(head,Rect2i(0,0,25,29),at)
  for y in range(256):
   for x in range(256):
    if not window.has_point(Vector2i(x,y)):
     checks+=1
     if output.get_pixel(x,y)!=source.get_pixel(x,y):failures+=1
  var file:String="head-candidates/"+row.key+"-"+str(row.index).pad_zeros(3)+".png";output.save_png(OUT+file)
  records.append({"source":row.source,"cell":i,"key":row.key,"index":row.index,"window":[window.position.x,window.position.y,window.size.x,window.size.y],"placement":[at.x,at.y],"candidate":file})
 var report:=FileAccess.open(OUT+"nine-head-package-evidence.json",FileAccess.WRITE)
 report.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"status":"nine-pose unselected head/neck study","scope":"Generated source cell extraction, original RGBA outside recorded rectangles exact. Includes collar pixels; body registration/clocks unchanged. Missing remaining held/pickup/unload alias/turn joins and paired helmet; no family/runtime acceptance."},"  "))
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  var file:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES NINE HEADS: ",checks,"checks; ",failures,"failures; unselected")
 quit(1 if failures else 0)
