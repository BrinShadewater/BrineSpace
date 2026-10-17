extends "res://character/bill-carry-continuation-v1/carry_player.gd"
## Staged finite service-loss return. Not accepted by the previous checkpoint wrapper.
var return_plan:Dictionary={}
var last_carry:Texture2D
func rows_for(gear:String)->Dictionary:
 return frames if gear.is_empty() else equipment_frames.get(gear,{})
func add_row(plan:Array,key:String,index:int,gear:String,seconds:float=-1)->void:
 var durations:Dictionary=timing if gear.is_empty() else equipment_timing.get(gear,timing)
 plan.append({"key":key,"index":index,"seconds":seconds if seconds>0 else float(durations[key].durations[index])/1000.0})
func begin_return(time:float,gear:String)->bool:
 var rows:Dictionary=rows_for(gear);var key:String="carry-east"
 if not start_motion.is_empty():key="carry-start-east"
 elif str(motion.get("clip","")).begins_with("carry-turn-"):key=str(motion.clip)
 if not rows.has(key) or not rows.has("unload-east") or last_carry==null:return false
 var index:int=rows[key].find(last_carry)
 if index<0:return false
 var plan:Array=[];add_row(plan,key,index,gear,.08)
 if key.begins_with("carry-turn-"):
  if key.get_slice("-",3)!="east":return false
  for following in range(index+1,rows[key].size()):add_row(plan,key,following,gear)
 elif key=="carry-start-east":
  for previous in range(index-1,-1,-1):add_row(plan,key,previous,gear)
 else:
  # Finish only the remainder of this leg cycle, then settle through the exact
  # shared gait0/bridge-last contact back to the held master.
  if index>0:
   for following in range(index+1,rows[key].size()):add_row(plan,key,following,gear)
   add_row(plan,key,0,gear)
  for previous in range(rows["carry-start-east"].size()-1,-1,-1):add_row(plan,"carry-start-east",previous,gear)
 for following in rows["unload-east"].size():add_row(plan,"unload-east",following,gear)
 var duration:=0.0
 for row in plan:duration+=float(row.seconds)
 return_plan={"started":time,"until":time+duration,"gear":gear,"rows":plan}
 return true
func return_active(time:float)->bool:
 return not return_plan.is_empty() and time<float(return_plan.until)
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
 if not return_plan.is_empty():
  if equipment!=return_plan.gear or time<float(return_plan.started) or time>=float(return_plan.until):return_plan.clear()
  else:
   var cursor:float=time-float(return_plan.started)
   for row in return_plan.rows:
    cursor-=float(row.seconds)
    if cursor<0:return rows_for(equipment)[row.key][row.index]
 var result:Texture2D=super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
 if state=="carry":last_carry=result
 return result
func snapshot()->Dictionary:
 var data=super.snapshot();data.carry_binding="bill-east-return1";data.carry_return=return_plan.duplicate(true);return data
func restore_snapshot(_data:Dictionary)->void:
 # No silent partial restore: this candidate still needs paired lifecycle admission.
 return
