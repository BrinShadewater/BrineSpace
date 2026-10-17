extends "res://scripts/crew_sprite_player.gd"
## Authoring preview only; bridge snapshot/interruption lifecycle remains unimplemented.
var start_motion:Dictionary={}
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
 if not start_motion.is_empty():
  if state!="carry" or direction!="south" or equipment!=start_motion.gear or time<start_motion.started:
   start_motion.clear()
  elif time-start_motion.started<cycle_seconds("carry-start-south",equipment):
   return frame_at_elapsed("carry-start-south",time-start_motion.started,equipment)
  else:
   start_motion.clear();current_key="carry-south";phase=.139;started=time-.139;last_time=time;last_position=position_cells
 var changing_carry_facing:bool=motion.get("state","")=="carry" and motion.get("direction",direction)!=direction
 var entering:bool=state=="carry" and direction=="south" and current_key!="carry-south" and str(motion.get("clip","")).is_empty() and not changing_carry_facing
 var previous:String=motion.get("clip","")
 var finished:bool=state=="carry" and direction=="south" and previous.begins_with("carry-turn-") and time>=float(motion.get("started",time))+cycle_seconds(previous,equipment)
 var normal:Texture2D=super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
 var rows:Dictionary=frames if equipment.is_empty() else equipment_frames.get(equipment,{})
 if (finished or entering) and rows.has("carry-start-south"):
  start_motion={"started":time,"gear":equipment}
  return frame_at_elapsed("carry-start-south",0,equipment)
 return normal
