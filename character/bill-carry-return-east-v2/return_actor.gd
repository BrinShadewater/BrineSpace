extends "res://character/bill-carry-continuation-v1/carry_actor.gd"
## Staged return holds ordinary movement, not the normal needs/hazard update.
const RETURN_BINDING="bill-east-return2"
func update(main,delta:float)->void:
 preview_time=main.get_visual_time_seconds()
 if preview_player!=null and not preview_player.return_plan.is_empty():
  if dead or not active or movement_medium!="dry" or ("diving-helmet" if helmet_equipped else "")!=preview_player.return_plan.gear or not preview_player.return_active(preview_time):preview_player.return_plan.clear()
 var interrupted:bool=preview_player!=null and active and not dead and movement_medium=="dry" and stage=="workshop_carry" and direction=="east" and not service_available(main,goal_cell)
 if interrupted:preview_player.begin_return(preview_time,"diving-helmet" if helmet_equipped else "")
 super.update(main,delta)
 if preview_player==null:return
 if interrupted:
  if stage=="workshop_carry":preview_player.return_plan.clear()
  else:planted_until=-1;planted_clip="";preview_player.start_motion.clear();preview_player.motion.clear()
 if not preview_player.return_plan.is_empty() and (dead or not active or movement_medium!="dry" or stage!="" or state not in ["idle","walk"] or goal in ["fire-retreat","flood-retreat"] or not can_stand(foot)):preview_player.return_plan.clear()
func move(delta:float)->void:
 if preview_player!=null and preview_player.return_active(preview_time):
  if movement_medium=="dry" and not dead and goal not in ["fire-retreat","flood-retreat"]:return
  preview_player.return_plan.clear()
 super.move(delta)
func animation_state()->String:
 if preview_player!=null and preview_player.return_active(preview_time):return "carry"
 return super.animation_state()
func snapshot()->Dictionary:
 var data=super.snapshot();data.carry_binding=RETURN_BINDING;data.carry_return_until=float(preview_player.return_plan.until) if preview_player!=null and not preview_player.return_plan.is_empty() else -1.0;return data
static func valid_return_snapshot(data:Variant)->bool:
 if not data is Dictionary or data.get("carry_binding","")!=RETURN_BINDING:return false
 var copy:Dictionary=data.duplicate(true);copy.carry_binding="bill-east-turn3-start3-gait2"
 if not preload("res://character/bill-carry-continuation-v1/carry_actor.gd").valid_carry_snapshot(copy):return false
 var until:Variant=data.get("carry_return_until")
 if not (until is float or until is int) or not is_finite(float(until)) or until< -1:return false
 if until!=-1 and (until<0 or not data.active or data.get("dead",false) or data.get("movement_medium","dry")!="dry" or data.direction!="east" or data.stage!="" or data.state not in ["idle","walk"] or data.goal in ["fire-retreat","flood-retreat"] or not data.carry_pivot.is_empty()):return false
 return true
func restore_snapshot(main,data:Dictionary,staged:=false)->void:
 if not valid_return_snapshot(data):return
 var copy:Dictionary=data.duplicate(true);copy.carry_binding="bill-east-turn3-start3-gait2"
 await super.restore_snapshot(main,copy,staged)
 preview_time=main.get_visual_time_seconds()
