extends "res://character/bill-carry-start-west-v1/carry_start_preview_player.gd"
## Staged visual stow, using actual last submitted carry source. No save admission.
var stow_plan:Dictionary={}
var last_carry:Texture2D
var last_carry_key:=""
func rows_for(gear:String)->Dictionary:
 return frames if gear.is_empty() else equipment_frames.get(gear,{})
func add_row(plan:Array,key:String,index:int,gear:String,seconds:float=-1)->void:
 var durations:Dictionary=timing if gear.is_empty() else equipment_timing.get(gear,timing)
 plan.append({"key":key,"index":index,"seconds":seconds if seconds>0 else float(durations[key].durations[index])/1000.0})
func begin_stow(time:float,gear:String)->bool:
 var rows:Dictionary=rows_for(gear)
 for key in [last_carry_key,"carry-west","carry-start-west","carry-turn-west-north","unload-north"]:
  if not rows.has(key):return false
 if last_carry==null:return false
 var index:int=rows[last_carry_key].find(last_carry)
 if index<0 or last_carry_key not in ["carry-west","carry-start-west"]:return false
 var plan:Array=[];add_row(plan,last_carry_key,index,gear,.08)
 if last_carry_key=="carry-start-west":
  for previous in range(index-1,-1,-1):add_row(plan,last_carry_key,previous,gear)
 else:
  if index>0:
   for following in range(index+1,rows["carry-west"].size()):add_row(plan,"carry-west",following,gear)
   add_row(plan,"carry-west",0,gear)
  # Gait0 is already the exact bridge contact; skip its duplicated last2 rows.
  for previous in range(3,-1,-1):add_row(plan,"carry-start-west",previous,gear)
 # Bridge0 and turn0 are the same master. Continue through remaining yaw poses.
 for following in range(1,rows["carry-turn-west-north"].size()):add_row(plan,"carry-turn-west-north",following,gear)
 var prefix:=0.0
 for row in plan:prefix+=float(row.seconds)
 var unload_seconds:=0.0
 for following in rows["unload-north"].size():
  add_row(plan,"unload-north",following,gear);unload_seconds+=float(plan[-1].seconds)
 # Keep the original2-second unloading stage, including its final-source hold.
 if unload_seconds>2.0:return false
 plan[-1].seconds+=2.0-unload_seconds
 stow_plan={"started":time,"unload_started":time+prefix,"until":time+prefix+2.0,"gear":gear,"rows":plan}
 start_motion.clear();motion.clear();return true
func stow_active(time:float)->bool:
 return not stow_plan.is_empty() and time<float(stow_plan.until)
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
 if not stow_plan.is_empty():
  if equipment!=stow_plan.gear or time<float(stow_plan.started):stow_plan.clear()
  elif time>=float(stow_plan.until):
   if state in ["carry","unload"] and direction=="north":
    current_key="unload-north";current_equipment=equipment;phase=2.0;started=time-2.0;last_time=time;last_position=position_cells
    stow_plan.clear();return frame_at_elapsed("unload-north",2.0,equipment)
   stow_plan.clear()
  elif state in ["carry","unload"] and direction=="north":
   var cursor:float=time-float(stow_plan.started)
   for row in stow_plan.rows:
    cursor-=float(row.seconds)
    if cursor<0:return rows_for(equipment)[row.key][row.index]
  else:stow_plan.clear()
 var result:Texture2D=super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
 if state=="carry" and direction=="west" and str(motion.get("clip","")).is_empty():
  last_carry=result;last_carry_key="carry-start-west" if not start_motion.is_empty() else "carry-west"
 return result
