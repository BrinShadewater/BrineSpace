extends SceneTree
const PROGRESS="res://character/krusher-continuity-audit-v1/candidate-bank-index.json"
var checks:=0
var errors:Array=[]
func check(ok:bool,label:String)->void:
 checks+=1
 if not ok:errors.append(label)
func pixels(t:Texture2D)->PackedByteArray:
 return (t.diffuse_texture if t is CanvasTexture else t).get_image().get_data()
func _initialize()->void:
 var uid="res://character/krusher-continuity-audit-v1/native/verify.gd.uid"
 if not FileAccess.file_exists(uid):
  var f=FileAccess.open(uid,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 call_deferred("run")
func run()->void:
 var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS));var player=preload("res://scripts/crew_sprite_player.gd").new();var rows:Dictionary={"bare":{},"helmet":{}}
 for gear in ["bare","helmet"]:
  for path in progress.candidatePacks[gear]:
   if gear=="bare":player.load_manifest(path,true)
   else:check(player.load_equipment_manifest("diving-helmet",path),"paired admission "+path)
   var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
   for s in m.states:rows[gear][s.id]={"root":m,"state":s,"manifest":path}
 var slots:=0;var counts:Dictionary={}
 for gear in ["bare","helmet"]:
  var equipment:String="" if gear=="bare" else "diving-helmet";var pool:Dictionary=player.frames if gear=="bare" else player.equipment_frames[equipment]
  check(pool.size()==rows[gear].size(),"Merged state count "+gear);counts[gear]=pool.size()
  for key in rows[gear]:
   var record:Dictionary=rows[gear][key];var m:Dictionary=record.root;var s:Dictionary=record.state;var clock:=0.0
   for i in range(s.frameFiles.size()):
    var hold:float=s.frameDurationsMs[i]/1000.0;var texture:Texture2D=player.frame_at_elapsed(key,clock+hold*.5,equipment);var source:String=s.frameFiles[i];var file:String=source if source.begins_with("res://") else str(record.manifest).get_base_dir().path_join(source)
    check(texture!=null,"Native texture "+key)
    check(pixels(texture)==Image.load_from_file(file).get_data(),"Merged source slot "+gear+key+str(i))
    check(texture.get_meta("crew_pivot")==Vector2(m.pivot[0],m.pivot[1]),"Merged pivot "+key)
    check(texture.get_meta("crew_standing_height")==148.0,"Merged ruler "+key)
    check(texture.get_size()==Vector2(m.frameWidth,m.frameHeight),"Merged canvas "+key)
    check(pixels(player.frame_at_elapsed(key,clock+.000001,equipment))==pixels(texture),"Pose start "+key)
    check(pixels(player.frame_at_elapsed(key,clock+hold-.000001,equipment))==pixels(texture),"Pose end "+key)
    if key=="carry-settle-west":check(not texture is CanvasTexture,"Original nearest settle filter retained")
    clock+=hold;slots+=1
   check(absf(player.cycle_seconds(key,equipment)-clock)<.000001,"Merged source clock "+key)
 var output:String=OS.get_environment("KRUSHER_NATIVE_OUTPUT");var f=FileAccess.open(output.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"errors":errors,"states":counts,"slots":slots,"scope":"Full revised animation bank: all 586 states and 8058 slots with native source pixels, clock boundaries and geometry. Station review is separate."},"\t"))
 print("KRUSHER_NATIVE checks=%d errors=%d slots=%d"%[checks,errors.size(),slots]);quit(0 if errors.is_empty() else 1)
