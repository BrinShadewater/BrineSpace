extends SceneTree
const OUT="res://character/james-side-motion-review-2026-10-02/"
func _initialize():call_deferred("run")
func run():
 if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
 var source:=Image.load_from_file("res://character/james-cargo-material-joined-v1/frames/bare/carry-east/000.png");source.convert(Image.FORMAT_RGBA8)
 var atlas:=Image.load_from_file(OUT+"head-closeup-generated.png");atlas.convert(Image.FORMAT_RGBA8)
 # Explicit source normalization/extraction, not whole-body replacement.
 var cell:=atlas.get_region(Rect2i(0,0,418,418));cell.resize(64,64,Image.INTERPOLATE_LANCZOS)
 var head:=cell.get_region(Rect2i(18,10,30,32));head.resize(25,29,Image.INTERPOLATE_LANCZOS)
 var output:Image=source.duplicate();var window:=Rect2i(128,71,30,32)
 output.fill_rect(window,Color(0,0,0,0));output.blit_rect(head,Rect2i(0,0,25,29),Vector2i(130,74))
 var checks:=0;var failures:=0
 for y in range(256):
  for x in range(256):
   if not window.has_point(Vector2i(x,y)):
    checks+=1
    if output.get_pixel(x,y)!=source.get_pixel(x,y):failures+=1
 output.save_png(OUT+"carry-east-000-head-candidate.png")
 var report:=FileAccess.open(OUT+"head-package-evidence.json",FileAccess.WRITE)
 report.store_string(JSON.stringify({"checks":checks,"failures":failures,"sourceWindow":[128,71,30,32],"generatedCell":[0,0,418,418],"nativeHeadExtract":[18,10,30,32],"headSize":[25,29],"placement":[130,74],"status":"single-pose source-authoring candidate unselected","scope":"Generated head/neck extraction registered at original collar, original RGBA outside rectangular window exact. Window can include collar/backpack pixels; not semantic head protection. One pose only; no complete family or helmet/turn/runtime acceptance."},"  "))
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  var file:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES HEAD PACKAGE: ",checks,"checks; ",failures,"failures; single unselected pose")
 quit(1 if failures else 0)
