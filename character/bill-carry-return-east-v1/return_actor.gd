extends "res://character/bill-carry-continuation-v1/carry_actor.gd"
## Staged visual settling interval. Full needs/hazard/restore integration remains open.
func update(main,delta:float)->void:
 var now:float=main.get_visual_time_seconds();preview_time=now
 if preview_player!=null and not preview_player.return_plan.is_empty():
  if dead or not active or movement_medium!="dry":preview_player.return_plan.clear()
  elif preview_player.return_active(now):return
  else:preview_player.return_plan.clear()
 var interrupted:bool=preview_player!=null and active and not dead and movement_medium=="dry" and stage=="workshop_carry" and direction=="east" and not service_available(main,goal_cell)
 if interrupted:preview_player.begin_return(now,"diving-helmet" if helmet_equipped else "")
 super.update(main,delta)
 if interrupted:
  if stage=="workshop_carry":preview_player.return_plan.clear()
  else:
   planted_until=-1;planted_clip="";preview_player.start_motion.clear();preview_player.motion.clear()
func snapshot()->Dictionary:
 var data=super.snapshot();data.carry_binding="bill-east-return1";return data
func restore_snapshot(_main,_data:Dictionary,_staged:=false)->void:
 return # Unsupported lifecycle must not look like a successful old-wrapper restore.
func animation_state()->String:
 # Keep both bare and equipped sources on the carry player while the finite
 # visual return runs; controller stage/next goal already reflect cancellation.
 if preview_player!=null and preview_player.return_active(preview_time):return "carry"
 return super.animation_state()
