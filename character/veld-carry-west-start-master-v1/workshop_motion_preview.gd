extends "res://character/veld-cargo-east-master-family-v1/workshop_motion_preview.gd"
## Authoring-only movement study; no normal selection or interruption/checkpoint acceptance.
var start_elapsed:=-1.0
var start_heading:=""
func animation_state()->String:
 if start_elapsed>=0 and stage=="workshop_carry":return "carry-start"
 return super.animation_state()
func action_elapsed()->float:
 if start_elapsed>=0 and stage=="workshop_carry":return start_elapsed
 return super.action_elapsed()
func update(main,delta:float)->void:
 super.update(main,delta)
 if stage!="workshop_carry" or movement_medium!="dry":start_elapsed=-1;start_heading=""
func move(delta:float)->void:
 if preview_player==null or stage!="workshop_carry" or movement_medium!="dry" or path.is_empty():
  start_elapsed=-1;start_heading="";super.move(delta);return
 var gear:String="diving-helmet" if helmet_equipped else ""
 var key:String="carry-start-"+direction
 if start_elapsed>=0:
  var duration:float=preview_player.cycle_seconds(key,gear)
  var previous:float=start_elapsed;start_elapsed=minf(duration,start_elapsed+delta)
  # First planted source holds80ms, then accelerate over remaining240ms.
  var speed_before:float=clampf((previous-.08)/.24,0,1)
  var speed_after:float=clampf((start_elapsed-.08)/.24,0,1)
  super.move(delta*(speed_before+speed_after)*.5)
  if start_elapsed>=duration:
   start_elapsed=-1;start_heading=""
   # Transition endpoint is exactly carry row0; start its distance phase here.
   preview_player.current_key=""
   preview_player.motion={"state":"carry","direction":direction,"clip":"","started":preview_time}
  return
 var rows:Dictionary=preview_player.frames if gear.is_empty() else preview_player.equipment_frames.get(gear,{})
 var ready:bool=preview_time>=planted_until and (held_entry or not planted_clip.is_empty())
 if ready and direction=="west" and travel_heading(foot,path[0],direction)==direction and rows.has(key):
  start_elapsed=0;start_heading=direction;held_entry=false;planted_until=-1;planted_clip=""
  return
 super.move(delta)
