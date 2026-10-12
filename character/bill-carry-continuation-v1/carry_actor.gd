extends "res://character/bill-carry-turn-east-south-motion-v3/carry_motion_preview.gd"
## Candidate planted-pivot persistence; production actor remains unchanged.
const BINDING="bill-east-turn3-start3-gait2"
func update(main,delta:float)->void:
 super.update(main,delta)
 if not active or dead or movement_medium!="dry" or animation_state()!="carry" or path.is_empty():
  planted_until=-1;planted_clip=""
  if preview_player!=null:
   preview_player.start_motion.clear()
   if preview_player.motion.get("state","")=="carry":preview_player.motion.clear()
   if preview_player.current_key.begins_with("carry-"):preview_player.current_key="";preview_player.phase=0;preview_player.last_time=-1
func snapshot()->Dictionary:
 var data=super.snapshot();data.carry_binding=BINDING
 data.carry_pivot={"clock":preview_time,"until":planted_until,"clip":planted_clip} if not planted_clip.is_empty() and preview_time<planted_until else {}
 return data
static func valid_carry_snapshot(data:Variant)->bool:
 if not preload("res://scripts/major_bill_npc.gd").valid_bill_snapshot(data):return false
 if data.get("carry_binding","")!=BINDING or not data.get("carry_pivot") is Dictionary:return false
 var pivot:Dictionary=data.carry_pivot
 if pivot.is_empty():return true
 if pivot.size()!=3 or not pivot.get("clip") is String or pivot.clip.get_slice_count("-")!=4:return false
 if pivot.clip.get_slice("-",0)!="carry" or pivot.clip.get_slice("-",1)!="turn":return false
 var before:String=pivot.clip.get_slice("-",2);var after:String=pivot.clip.get_slice("-",3)
 if before not in ["north","south","east","west"] or after not in ["north","south","east","west"] or before==after or after!=data.direction:return false
 for key in ["clock","until"]:
  if not (pivot.get(key) is float or pivot.get(key) is int) or not is_finite(float(pivot[key])):return false
 if pivot.clock<0 or pivot.until<=pivot.clock or pivot.until-pivot.clock>1.60001:return false
 return data.active and not data.get("dead",false) and data.get("movement_medium","dry")=="dry" and not data.path.is_empty() and data.stage=="workshop_carry"
func restore_snapshot(main,data:Dictionary,staged:=false)->void:
 if not valid_carry_snapshot(data):return
 await super.restore_snapshot(main,data,staged)
 var pivot:Dictionary=data.carry_pivot;preview_time=float(pivot.get("clock",main.get_visual_time_seconds()));planted_until=float(pivot.get("until",-1));planted_clip=str(pivot.get("clip",""))
