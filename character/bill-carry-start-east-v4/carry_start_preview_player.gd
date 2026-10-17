extends "res://scripts/crew_sprite_player.gd"
## Authoring preview only; bridge snapshot/interruption lifecycle remains unimplemented.
var start_motion:Dictionary={}
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
 if not start_motion.is_empty():
  if state!="carry" or direction!="east" or equipment!=start_motion.gear or time<start_motion.started:
   start_motion.clear()
  elif time-start_motion.started<cycle_seconds("carry-start-east",equipment):
   return frame_at_elapsed("carry-start-east",time-start_motion.started,equipment)
  else:
   start_motion.clear();current_key="carry-east";phase=.104;started=time-.104;last_time=time;last_position=position_cells
 var previous:String=motion.get("clip","")
 var finished:bool=state=="carry" and direction=="east" and previous.begins_with("carry-turn-") and time>=float(motion.get("started",time))+cycle_seconds(previous,equipment)
 var normal:Texture2D=super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
 var rows:Dictionary=frames if equipment.is_empty() else equipment_frames.get(equipment,{})
 if finished and rows.has("carry-start-east"):
  start_motion={"started":time,"gear":equipment}
  return frame_at_elapsed("carry-start-east",0,equipment)
 return normal
