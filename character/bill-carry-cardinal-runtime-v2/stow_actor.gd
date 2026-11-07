extends "res://character/bill-carry-cardinal-runtime-v1/carry_actor.gd"
## Staged workshop arrival. Only the normal unloading timer waits for settle/yaw.
func arrive()->void:
 var stowing:bool=not dead and active and movement_medium=="dry" and stage=="workshop_carry" and preview_player!=null
 if stowing:
  stowing=preview_player.begin_stow(preview_time,"diving-helmet" if helmet_equipped else "",direction)
 super.arrive()
 if stowing and (stage!="workshop_unload" or direction!="north"):preview_player.stow_plan.clear()
func animation_state()->String:
 if preview_player!=null and preview_player.stow_active(preview_time) and stage=="workshop_unload":return "carry"
 return super.animation_state()
func action_elapsed()->float:
 if preview_player!=null and preview_player.stow_active(preview_time) and stage=="workshop_unload":return -1.0
 return super.action_elapsed()
func update(main,delta:float)->void:
 preview_time=main.get_visual_time_seconds()
 if preview_player!=null and not preview_player.stow_plan.is_empty():
  if dead or not active or movement_medium!="dry" or ("diving-helmet" if helmet_equipped else "")!=preview_player.stow_plan.gear or stage!="workshop_unload" or direction!="north" or goal in ["fire-retreat","flood-retreat"] or preview_time<float(preview_player.stow_plan.started) or not can_stand(foot):preview_player.stow_plan.clear()
 var waiting:bool=preview_player!=null and not preview_player.stow_plan.is_empty() and preview_time<float(preview_player.stow_plan.unload_started)
 var saved_timer:float=timer
 super.update(main,delta)
 if preview_player==null:return
 if not preview_player.stow_plan.is_empty() and (dead or not active or movement_medium!="dry" or stage!="workshop_unload" or direction!="north" or goal in ["fire-retreat","flood-retreat"]):preview_player.stow_plan.clear()
 if waiting and not preview_player.stow_plan.is_empty():timer=saved_timer
func move(delta:float)->void:
 if preview_player!=null and preview_player.stow_active(preview_time) and stage=="workshop_unload" and movement_medium=="dry" and not dead and goal not in ["fire-retreat","flood-retreat"]:return
 super.move(delta)
