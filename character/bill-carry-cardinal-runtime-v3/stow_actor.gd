extends "res://character/bill-carry-cardinal-runtime-v2/stow_actor.gd"
const BINDING=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd").BINDING
func update(main,delta:float)->void:
 super.update(main,delta)
 if not active or dead or movement_medium!="dry" or goal in ["fire-retreat","flood-retreat"]:
  planted_until=-1;planted_clip=""
  if preview_player!=null:
   preview_player.start_motion.clear();preview_player.stow_plan.clear();preview_player.last_carry=null;preview_player.last_carry_key="";preview_player.last_carry_time=-1
   if preview_player.motion.get("state","")=="carry":preview_player.motion.clear()
func snapshot()->Dictionary:
 var data=super.snapshot();data.carry_binding=BINDING
 data.carry_pivot={"clock":preview_time,"until":planted_until,"clip":planted_clip} if not planted_clip.is_empty() and preview_time<planted_until else {}
 data.carry_arrival={"clock":preview_time,"until":float(preview_player.stow_plan.until),"unload_started":float(preview_player.stow_plan.unload_started)} if preview_player!=null and not preview_player.stow_plan.is_empty() else {}
 return data
static func valid_carry_snapshot(data:Variant)->bool:
 if not data is Dictionary or data.get("carry_binding","")!=BINDING or not data.get("carry_arrival") is Dictionary:return false
 var copy:Dictionary=data.duplicate(true);copy.carry_binding="bill-east-turn3-start3-gait2"
 if not preload("res://character/bill-carry-continuation-v1/carry_actor.gd").valid_carry_snapshot(copy):return false
 var arrival:Dictionary=data.carry_arrival
 if arrival.is_empty():return true
 if arrival.size()!=3 or not data.carry_pivot.is_empty():return false
 for key in ["clock","until","unload_started"]:
  if not preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd").finite_nonnegative(arrival.get(key)):return false
 if arrival.until<=arrival.clock or absf(arrival.until-arrival.unload_started-2)>.00001:return false
 return data.active and not data.get("dead",false) and data.get("movement_medium","dry")=="dry" and data.direction=="north" and data.stage=="workshop_unload" and data.path.is_empty() and data.goal not in ["fire-retreat","flood-retreat"]
func restore_snapshot(main,data:Dictionary,staged:=false)->void:
 if not valid_carry_snapshot(data):return
 await super.restore_snapshot(main,data,staged)
 var pivot:Dictionary=data.carry_pivot;var arrival:Dictionary=data.carry_arrival
 preview_time=float(arrival.get("clock",pivot.get("clock",main.get_visual_time_seconds())));planted_until=float(pivot.get("until",-1));planted_clip=str(pivot.get("clip",""))
