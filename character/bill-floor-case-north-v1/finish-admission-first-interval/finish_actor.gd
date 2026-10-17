extends "res://scripts/bill_carry_npc.gd"
const FINISH=preload("res://character/bill-floor-case-north-v1/finish_plan.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
var finish_cell:=Vector2i(-1,-1)
var finish_foot:=Vector2.ZERO
func eligible(main)->bool:
 return active and not dead and movement_medium=="dry" and goal not in ["fire-retreat","flood-retreat"] and direction=="north" and can_stand(foot) and main.occupied.has(finish_cell) and main.occupied[finish_cell].get("id")=="salvage_workshop" and foot==finish_foot
func update(main,delta:float)->void:
 super.update(main,delta)
 if not preview_player.finish_exit.is_empty() and not eligible(main):preview_player.finish_exit.clear()
func advance_work_return(main,_delta:float)->bool:
 var now:float=main.get_visual_time_seconds()
 if not preview_player.finish_exit.is_empty():
  if not eligible(main) or now>=float(preview_player.finish_exit.until):preview_player.finish_exit.clear();return false
  return true # Hook runs after normal needs and actual fire/flood dispatch.
 if stage!="workshop_unload" or direction!="north" or service_available(main,goal_cell):return false
 var gear:String="diving-helmet" if helmet_equipped else ""
 var shown:Texture2D=preview_player.frame("carry","north",now,foot/CELL,gear)
 var plan:Dictionary=FINISH.create(preview_player,shown,gear,now)
 if plan.is_empty():return false
 finish_cell=goal_cell;finish_foot=foot
 if not eligible(main):return false
 preview_player.finish_exit=plan;goal="";stage="";state="idle";path.clear();timer=0
 planted_until=-1;planted_clip="";activity="setting down recovered parts"
 return true
func animation_state()->String:
 if preview_player!=null and not preview_player.finish_exit.is_empty():return "carry"
 return super.animation_state()
func action_elapsed()->float:
 if preview_player!=null and not preview_player.finish_exit.is_empty():return -1.0
 return super.action_elapsed()
func observe_finish(main,shown:Texture2D)->void:
 var plan:Dictionary=preview_player.finish_exit
 if plan.is_empty() or not eligible(main) or main.visual_time_seconds<float(plan.release_at):return
 if FINISH.texture_at(preview_player,plan,main.visual_time_seconds)!=shown:return
 var index:int=preview_player.rows_for(plan.gear)["unload-north"].find(shown)
 if index<8:return
 var room:Dictionary=main.occupied[finish_cell]
 var payload:Dictionary={"version":1,"source":FLOOR.SOURCE,"anchor":finish_foot-(Vector2(finish_cell)+Vector2.ONE*.5)*CELL}
 if FLOOR.valid_payload(payload) and (not room.has(FLOOR.FIELD) or FLOOR.valid_payload(room[FLOOR.FIELD])):room[FLOOR.FIELD]=payload
func set_helmet_equipped(value:bool)->bool:
 var old:bool=helmet_equipped;var accepted:bool=super.set_helmet_equipped(value)
 if accepted and old!=value and preview_player!=null:preview_player.finish_exit.clear()
 return accepted
func die()->void:
 if preview_player!=null:preview_player.finish_exit.clear()
 super.die()
func snapshot()->Dictionary:
 var data:Dictionary=super.snapshot();data.finish_exit={"cell":finish_cell,"foot":finish_foot} if preview_player!=null and not preview_player.finish_exit.is_empty() else {};data.finish_binding=FINISH.FINISH_BINDING;return data
static func valid_finish_snapshot(data:Dictionary)->bool:
 if not data.get("finish_exit",{}) is Dictionary:return false
 var entry:Dictionary=data.get("finish_exit",{})
 if data.has("finish_binding") and data.finish_binding!=FINISH.FINISH_BINDING:return false
 if entry.is_empty():return true
 if data.get("finish_binding")!=FINISH.FINISH_BINDING or entry.size()!=2 or not entry.get("cell") is Vector2i or not entry.get("foot") is Vector2:return false
 if not entry.foot.is_finite() or entry.cell.x<0 or entry.cell.y<0 or entry.cell.x>=40 or entry.cell.y>=40:return false
 if not data.get("path") is PackedVector2Array or not data.get("carry_pivot",{}) is Dictionary or not data.get("carry_arrival",{}) is Dictionary:return false
 return data.get("active",false) and not data.get("dead",false) and data.get("movement_medium") == "dry" and data.get("direction")=="north" and data.get("stage")=="" and data.get("state")=="idle" and data.get("goal")=="" and data.get("path",PackedVector2Array()).is_empty() and data.get("foot")==entry.foot and data.get("timer") == 0 and data.get("carry_pivot",{}).is_empty() and data.get("carry_arrival",{}).is_empty()
func restore_snapshot(main,data:Dictionary,staged:=false)->void:
 if not valid_finish_snapshot(data):return
 await super.restore_snapshot(main,data,staged)
 var entry:Dictionary=data.get("finish_exit",{})
 finish_cell=entry.get("cell",Vector2i(-1,-1));finish_foot=entry.get("foot",Vector2.ZERO)
