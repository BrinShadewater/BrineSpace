extends "res://character/veld-carry-west-start-master-v1/workshop_motion_preview.gd"
## Authoring-only phase2 stop for the actual default workshop route.
var stop_elapsed:=-1.0
var stop_deceleration:=.24
var stop_target:=Vector2.INF
var stop_speed:=0.0
func animation_state()->String:
 if stop_elapsed>=0 and stage=="workshop_carry":return "carry-stop-phase2"
 return super.animation_state()
func action_elapsed()->float:
 if stop_elapsed>=0 and stage=="workshop_carry":
  return stop_elapsed/stop_deceleration*.24 if stop_elapsed<stop_deceleration else .24+stop_elapsed-stop_deceleration
 return super.action_elapsed()
func update(main,delta:float)->void:
 super.update(main,delta)
 if stage!="workshop_carry" or movement_medium!="dry":stop_elapsed=-1;stop_target=Vector2.INF
func move(delta:float)->void:
 if stop_elapsed>=0:
  var before:float=minf(stop_elapsed,stop_deceleration)
  stop_elapsed=minf(stop_deceleration+.08,stop_elapsed+delta)
  var after:float=minf(stop_elapsed,stop_deceleration)
  # Integrate the linear speed ramp; keep original navigation/collision handling.
  var travel:float=stop_speed*((after-before)-(after*after-before*before)/(2*stop_deceleration))
  if travel>0:super.move(travel/(movement_rate()*flood_speed))
  if stop_elapsed>=stop_deceleration+.08:
   stop_elapsed=-1;stop_target=Vector2.INF;path.clear()
   super.arrive()
  return
 if preview_player!=null and stage=="workshop_carry" and movement_medium=="dry" and start_elapsed<0 and preview_time>=planted_until and direction=="west" and path.size()==1:
  var speed:float=movement_rate()*flood_speed
  var distance:float=foot.distance_to(path[0])
  if distance>0 and distance<=speed*.24*.5:
   var gear:String="diving-helmet" if helmet_equipped else ""
   var bank:Dictionary=preview_player.frames if gear.is_empty() else preview_player.equipment_frames[gear]
   var texture:Texture2D=preview_player.frame_at_elapsed("carry-west",fmod(preview_player.phase,preview_player.cycle_seconds("carry-west",gear)),gear)
   if bank.get("carry-west",[]).find(texture)==2:
    stop_target=path[0];stop_speed=speed;stop_deceleration=2*distance/speed;stop_elapsed=0
    return
 super.move(delta)
func arrive()->void:
 if stop_elapsed>=0:
  # Retain this already-consumed real waypoint through the final planted80ms.
  path=[stop_target];state="walk"
  return
 super.arrive()
