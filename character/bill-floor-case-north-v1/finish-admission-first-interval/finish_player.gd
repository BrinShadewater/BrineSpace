extends "res://scripts/bill_carry_player.gd"
const FINISH=preload("res://character/bill-floor-case-north-v1/finish_plan.gd")
var finish_exit:Dictionary={}
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
 if not finish_exit.is_empty():
  if equipment!=finish_exit.gear or time<float(finish_exit.started) or time>=float(finish_exit.until):finish_exit.clear()
  elif state=="carry" and direction=="north":return FINISH.texture_at(self,finish_exit,time)
  else:finish_exit.clear()
 return super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
func snapshot()->Dictionary:
 var data:Dictionary=super.snapshot();data.finish_exit=finish_exit.duplicate(true);data.finish_binding=FINISH.FINISH_BINDING;return data
func admits_loaded_snapshot(data:Dictionary)->bool:
 if not super.admits_loaded_snapshot(data):return false
 if not data.get("finish_exit",{}) is Dictionary or not FINISH.valid(data.get("finish_exit",{})):return false
 if data.has("finish_binding") and data.finish_binding!=FINISH.FINISH_BINDING:return false
 if not data.get("finish_exit",{}).is_empty():
  if not data.carry_start.is_empty() or not data.carry_stow.is_empty():return false
  if data.get("finish_binding")!=FINISH.FINISH_BINDING or data.finish_exit.gear!=data.get("equipment",""):return false
  var probe=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd").new()
  for field in BANK_FIELDS:probe.set(field,get(field).duplicate(true))
  apply_bank(probe,carry_banks[data.carry_binding])
  if not preload("res://character/bill-floor-case-north-v1/finish_sources.gd").matches(probe,data.finish_exit.gear):return false
 return true
func restore_snapshot(data:Dictionary)->void:
 if not admits_loaded_snapshot(data):return
 super.restore_snapshot(data)
 finish_exit=data.get("finish_exit",{}).duplicate(true)
