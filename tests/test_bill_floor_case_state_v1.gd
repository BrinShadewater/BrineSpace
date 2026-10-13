extends SceneTree
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/floor_checkpoint.gd")
var checks:=0
var failures:=0
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
 for invalid_state in [null,false,[],{"placed_rooms":true}]:
  check(not FLOOR_SAVE.problem({"state":invalid_state}).is_empty(),"Malformed top-level candidate state rejected without exception")
 var cell:=Vector2i(20,21);var room:Dictionary={"id":"salvage_workshop","pos":cell};var rooms:Array=[room]
 var payload:Dictionary={"version":1,"source":FLOOR.SOURCE,"anchor":Vector2(-112,128)}
 check(FLOOR.valid_rooms(rooms) and FLOOR.payload(room).is_empty(),"Legacy room stays empty")
 room[FLOOR.FIELD]=payload.duplicate(true);check(FLOOR.valid_rooms(rooms),"Valid one-case room state")
 for invalid in [null,[],{}, {"version":1,"source":"unknown","anchor":Vector2.ZERO},{"version":2,"source":FLOOR.SOURCE,"anchor":Vector2.ZERO},{"version":1.0,"source":FLOOR.SOURCE,"anchor":Vector2.ZERO},{"version":1,"source":FLOOR.SOURCE,"anchor":Vector2(NAN,0)},{"version":1,"source":FLOOR.SOURCE,"anchor":Vector2(193,0)},{"version":1,"source":FLOOR.SOURCE,"anchor":[0,0]},{"version":1,"source":FLOOR.SOURCE,"anchor":Vector2.ZERO,"extra":true}]:
  room[FLOOR.FIELD]=invalid;check(not FLOOR.valid_rooms(rooms) and FLOOR.payload(room).is_empty(),"Malformed case rejected and not drawn")
 room[FLOOR.FIELD]=payload.duplicate(true);room.id="galley";check(not FLOOR.valid_rooms(rooms),"Other rooms reject case state")
 room.id="salvage_workshop";room.erase(FLOOR.FIELD)
 var before:Dictionary={"stage":"workshop_unload","goal":"curiosity","cell":cell,"foot":(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(-112,128),"active":true,"dead":false,"medium":"dry","service":true,"until":2.0}
 var after:Dictionary=before.duplicate(true);after.stage="";after.goal="primary-work"
 for label in ["early","active","dead","water","service","fire","moved","removed","wrong-room","no-plan"]:
  var prior:Dictionary=before.duplicate(true);var next:Dictionary=after.duplicate(true);var test_rooms:Array=rooms.duplicate(true);var time:=2.0
  match label:
   "early":time=1.999
   "active":next.active=false
   "dead":next.dead=true
   "water":next.medium="exterior"
   "service":next.service=false
   "fire":next.goal="fire-retreat"
   "moved":next.foot+=Vector2.ONE
   "removed":test_rooms.clear()
   "wrong-room":test_rooms[0].id="galley"
   "no-plan":prior.until=-1.0
  var untouched:Array=test_rooms.duplicate(true)
  check(not FLOOR.observe_completed(test_rooms,prior,next,time) and test_rooms==untouched,"Interrupted/non-completion is atomic: "+label)
 check(FLOOR.observe_completed(rooms,before,after,2.0),"Actual completion deposits one case")
 check(FLOOR.payload(room)==payload,"Case anchor independent of actor and gear")
 before.foot+=(Vector2(8,0));after.foot=before.foot
 check(FLOOR.observe_completed(rooms,before,after,2.0) and room[FLOOR.FIELD].size()==3 and room[FLOOR.FIELD].anchor==Vector2(-104,128),"Later delivery replaces single room case without accumulation")
 rooms.clear();check(FLOOR.valid_rooms(rooms),"Removing room removes its case state")
 rooms.append({"id":"salvage_workshop","pos":cell});check(FLOOR.payload(rooms[0]).is_empty(),"Rebuilt room does not inherit stale case")
 print("BILL FLOOR CASE STATE V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
