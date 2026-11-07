extends SceneTree
const NPC=preload("res://scripts/bill_npc.gd")
var checks:=0
var failures:=0
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var actor:=NPC.new()
 check(actor.has_method("_template_row_blockers"),"Row broad phase exists")
 if not actor.has_method("_template_row_blockers"):quit(1);return
 var blockers:Array[Rect2]=[Rect2(-176,-176,24,24),Rect2(-50,-50,20,20),Rect2(32,0,32,32),Rect2(-180,176,360,.05),Rect2(-180,-.05,360,.05)]
 var original_checks:=0;var filtered_checks:=0
 for y in range(-176,177,16):
  var rows:Array[Rect2]=actor._template_row_blockers(blockers,float(y))
  for x in range(-176,177,16):
   var a:=Vector2(x,y)
   for delta in [Vector2.ZERO,Vector2(16,0),Vector2(0,16),Vector2(16,16),Vector2(-16,16)]:
    original_checks+=blockers.size();filtered_checks+=rows.size()
    check(NPC._template_segment_clear(a,a+delta,rows)==NPC._template_segment_clear(a,a+delta,blockers),"Exact half-open row sweep")
 check(filtered_checks<original_checks/2,"Broad phase removes most irrelevant blockers")
 print("NAVIGATION TEMPLATE ROWS ",JSON.stringify({"checks":checks,"failures":failures,"original_candidates":original_checks,"row_candidates":filtered_checks}));quit(1 if failures else 0)
