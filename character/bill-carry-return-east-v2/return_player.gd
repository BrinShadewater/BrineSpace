extends "res://character/bill-carry-return-east-v1/return_player.gd"
const RETURN_BINDING="bill-east-return2"
func snapshot()->Dictionary:
 var data=super.snapshot();data.carry_binding=RETURN_BINDING;return data
static func valid_return_snapshot(data:Variant)->bool:
 if not data is Dictionary or data.get("carry_binding","")!=RETURN_BINDING:return false
 var copy:Dictionary=data.duplicate(true);copy.carry_binding="bill-east-turn3-start3-gait2"
 if not preload("res://character/bill-carry-continuation-v1/carry_player.gd").valid_carry_snapshot(copy):return false
 if not data.get("carry_return") is Dictionary:return false
 var plan:Dictionary=data.carry_return
 if plan.is_empty():return true
 if plan.size()!=4 or plan.get("gear") not in ["","diving-helmet"] or plan.gear!=data.get("equipment","") or not plan.get("rows") is Array or plan.rows.is_empty() or plan.rows.size()>32:return false
 for key in ["started","until"]:
  if not (plan.get(key) is float or plan.get(key) is int) or not is_finite(float(plan[key])) or plan[key]<0:return false
 var seconds:=0.0
 for row in plan.rows:
  if not row is Dictionary or row.size()!=3 or row.get("key") not in ["carry-east","carry-start-east","unload-east","carry-turn-south-east","carry-turn-north-east","carry-turn-west-east"] or not row.get("index") is int or row.index<0 or row.index>15:return false
  if not (row.get("seconds") is float or row.get("seconds") is int) or not is_finite(float(row.seconds)) or row.seconds<=0 or row.seconds>.32:return false
  seconds+=float(row.seconds)
 return seconds<3 and absf(plan.until-plan.started-seconds)<.00001 and data.carry_start.is_empty() and data.get("motion",{}).is_empty()
func admits_loaded_snapshot(data:Dictionary)->bool:
 if not valid_return_snapshot(data):return false
 var gear:String=str(data.get("equipment",""));var rows:Dictionary=rows_for(gear)
 if not data.key.is_empty() and not rows.has(data.key):return false
 var plan:Dictionary=data.carry_return
 if not plan.is_empty():
  var durations:Dictionary=timing if gear.is_empty() else equipment_timing.get(gear,timing)
  for index in plan.rows.size():
   var row:Dictionary=plan.rows[index]
   if not rows.has(row.key) or row.index>=rows[row.key].size() or not durations.has(row.key):return false
   var expected:float=.08 if index==0 else float(durations[row.key].durations[row.index])/1000.0
   if absf(row.seconds-expected)>.00001:return false
  var probe=preload("res://character/bill-carry-return-east-v1/return_player.gd").new()
  probe.frames=frames;probe.timing=timing;probe.equipment_frames=equipment_frames;probe.equipment_timing=equipment_timing
  var first:Dictionary=plan.rows[0];probe.last_carry=rows[first.key][first.index]
  if first.key=="carry-start-east":probe.start_motion={"gear":gear,"started":plan.started}
  elif str(first.key).begins_with("carry-turn-"):probe.motion={"clip":first.key}
  if not probe.begin_return(float(plan.started),gear) or probe.return_plan!=plan:return false
 return true
func restore_snapshot(data:Dictionary)->void:
 if not admits_loaded_snapshot(data):return
 current_key=data.key;current_equipment=str(data.get("equipment",""));phase=float(data.phase);last_time=float(data.last_time);started=float(data.started);last_position=data.last_position;motion=data.get("motion",{}).duplicate(true);start_motion=data.carry_start.duplicate(true);return_plan=data.carry_return.duplicate(true);last_carry=null
