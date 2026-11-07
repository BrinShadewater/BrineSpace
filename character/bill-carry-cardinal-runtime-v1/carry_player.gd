extends "res://scripts/crew_sprite_player.gd"
## Staged cardinal carry integration; normal selection remains unchanged.
const BANKS = [
 ["res://character/bill-carry-east-gait-v3/bare-manifest.json","res://character/bill-carry-east-gait-v3/helmet-manifest.json"],
 ["res://character/bill-carry-start-east-v4/bare-manifest.json","res://character/bill-carry-start-east-v4/helmet-manifest.json"],
 ["res://character/bill-carry-south-gait-v2/bare-manifest.json","res://character/bill-carry-south-gait-v2/helmet-manifest.json"],
 ["res://character/bill-carry-start-south-v1/bare-manifest.json","res://character/bill-carry-start-south-v1/helmet-manifest.json"],
 ["res://character/bill-carry-west-gait-v2/bare-manifest.json","res://character/bill-carry-west-gait-v2/helmet-manifest.json"],
 ["res://character/bill-carry-start-west-v2/bare-manifest.json","res://character/bill-carry-start-west-v2/helmet-manifest.json"],
 ["res://character/bill-carry-north-gait-v1/bare-manifest.json","res://character/bill-carry-north-gait-v1/helmet-manifest.json"],
 ["res://character/bill-carry-start-north-v1/bare-manifest.json","res://character/bill-carry-start-north-v1/helmet-manifest.json"]
]
var start_motion:Dictionary={}
func load_candidates()->bool:
 for pair in BANKS:
  load_manifest(pair[0],true)
  if not load_equipment_manifest("diving-helmet",pair[1]):return false
 return true
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
 if not start_motion.is_empty():
  if state!="carry" or direction!=start_motion.direction or equipment!=start_motion.gear or time<start_motion.started:
   start_motion.clear()
  elif time-start_motion.started<cycle_seconds("carry-start-"+direction,equipment):
   return frame_at_elapsed("carry-start-"+direction,time-start_motion.started,equipment)
  else:
   var resume:float=.104 if direction=="east" else .139
   start_motion.clear();current_key="carry-"+direction;phase=resume;started=time-resume;last_time=time;last_position=position_cells
 var changing:bool=motion.get("state","")=="carry" and motion.get("direction",direction)!=direction
 var entering:bool=state=="carry" and current_key!="carry-"+direction and str(motion.get("clip","")).is_empty() and not changing
 var previous:String=motion.get("clip","")
 var finished:bool=state=="carry" and previous.begins_with("carry-turn-") and motion.get("direction","")==direction and time>=float(motion.get("started",time))+cycle_seconds(previous,equipment)
 var normal:Texture2D=super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
 var rows:Dictionary=frames if equipment.is_empty() else equipment_frames.get(equipment,{})
 if (finished or entering) and rows.has("carry-start-"+direction):
  start_motion={"started":time,"gear":equipment,"direction":direction}
  return frame_at_elapsed("carry-start-"+direction,0,equipment)
 return normal
