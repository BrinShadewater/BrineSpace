extends "res://character/bill-carry-cardinal-runtime-v1/carry_player.gd"
## Staged cardinal arrival from the actual submitted source. Snapshot admission open.
var stow_plan:Dictionary={}
var last_carry:Texture2D
var last_carry_key:=""
var last_carry_gear:=""
var last_carry_time:=-1.0
func load_candidates()->bool:
 if not super.load_candidates():return false
 load_manifest("res://character/bill-unload-north-rise-v1/bare-manifest.json",true)
 return load_equipment_manifest("diving-helmet","res://character/bill-unload-north-rise-v1/helmet-manifest.json")
func rows_for(gear:String)->Dictionary:
 return frames if gear.is_empty() else equipment_frames.get(gear,{})
func add_row(plan:Array,key:String,index:int,gear:String,seconds:float=-1)->void:
 var durations:Dictionary=timing if gear.is_empty() else equipment_timing.get(gear,timing)
 plan.append({"key":key,"index":index,"seconds":seconds if seconds>0 else float(durations[key].durations[index])/1000.0})
func begin_stow(time:float,gear:String,direction:String="")->bool:
 if direction.is_empty():direction=last_carry_key.get_slice("-",last_carry_key.get_slice_count("-")-1)
 var rows:Dictionary=rows_for(gear)
 var gait:String="carry-"+direction;var bridge:String="carry-start-"+direction;var turn:String="carry-turn-"+direction+"-north"
 if last_carry==null or last_carry_gear!=gear or time<last_carry_time or time-last_carry_time>.1:return false
 for key in [last_carry_key,gait,bridge,"unload-north"]:
  if not rows.has(key):return false
 if direction!="north" and not rows.has(turn):return false
 var index:int=rows[last_carry_key].find(last_carry)
 if index<0 or last_carry_key not in [gait,bridge]:return false
 var plan:Array=[];add_row(plan,last_carry_key,index,gear,.08)
 if last_carry_key==bridge:
  # Last two entry rows duplicate gait contact: don't replay both on settling.
  for previous in range(mini(index-1,3),-1,-1):add_row(plan,bridge,previous,gear)
 else:
  if index>0:
   for following in range(index+1,rows[gait].size()):add_row(plan,gait,following,gear)
   add_row(plan,gait,0,gear)
  for previous in range(3,-1,-1):add_row(plan,bridge,previous,gear)
 if direction!="north":
  for following in range(1,rows[turn].size()):add_row(plan,turn,following,gear)
 var prefix:=0.0
 for row in plan:prefix+=float(row.seconds)
 var unload_seconds:=0.0
 for following in rows["unload-north"].size():
  add_row(plan,"unload-north",following,gear);unload_seconds+=float(plan[-1].seconds)
 if unload_seconds>2.0:return false
 plan[-1].seconds+=2.0-unload_seconds
 stow_plan={"started":time,"unload_started":time+prefix,"until":time+prefix+2.0,"gear":gear,"arrival_direction":direction,"rows":plan}
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
 if state=="carry" and str(motion.get("clip","")).is_empty():
  var key:String="carry-start-"+direction if not start_motion.is_empty() else "carry-"+direction
  if rows_for(equipment).get(key,[]).has(result):
   last_carry=result;last_carry_key=key;last_carry_gear=equipment;last_carry_time=time
 elif state!="carry":last_carry=null;last_carry_key="";last_carry_time=-1
 return result
