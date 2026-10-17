extends "res://scripts/veld_npc.gd"
## Staged cargo motion: ordinary update retains needs/service/safety priority.
var preview_player
var preview_time:=0.0
var held_entry:=false
var start_elapsed:=-1.0
var stop_elapsed:=-1.0
var stop_deceleration:=.24
var stop_target:=Vector2.INF
var stop_speed:=0.0
var turn_elapsed:=-1.0
var turn_duration:=0.0
var turn_key:=""
var arrival_pending:=false
var motion_gear:=false
var motion_goal:=""
var motion_cell:=Vector2i.ZERO

func clear_cargo_motion()->void:
 held_entry=false;start_elapsed=-1;stop_elapsed=-1;stop_target=Vector2.INF
 turn_elapsed=-1;turn_key="";arrival_pending=false
func motion_active()->bool:
 return start_elapsed>=0 or stop_elapsed>=0 or turn_elapsed>=0 or held_entry
func cargo_context_valid()->bool:
 return not dead and active and stage=="workshop_carry" and movement_medium=="dry" and not path.is_empty() and helmet_equipped==motion_gear and goal==motion_goal and goal_cell==motion_cell
func bind_cargo_context()->void:
 motion_gear=helmet_equipped;motion_goal=goal;motion_cell=goal_cell
func animation_state()->String:
 if cargo_context_valid():
  if turn_elapsed>=0:return turn_key.trim_suffix("-"+direction)
  if stop_elapsed>=0:return "carry-stop-phase2"
  if start_elapsed>=0:return "carry-start"
  if held_entry:return "carry-held"
 return super.animation_state()
func action_elapsed()->float:
 if cargo_context_valid():
  if turn_elapsed>=0:return turn_elapsed
  if start_elapsed>=0:return start_elapsed
  if stop_elapsed>=0:return stop_elapsed/stop_deceleration*.24 if stop_elapsed<stop_deceleration else .24+stop_elapsed-stop_deceleration
 return super.action_elapsed()
func update(main,delta:float)->void:
 preview_time=main.get_visual_time_seconds()
 if dead:clear_cargo_motion()
 if motion_active() and not cargo_context_valid():clear_cargo_motion()
 var previous:String=stage
 # No arrival early-return: inherited update runs its normal guards every tick.
 super.update(main,delta)
 if previous=="workshop_pickup" and stage=="workshop_carry":
  bind_cargo_context();held_entry=true
 if motion_active() and not cargo_context_valid():clear_cargo_motion()
func plant(heading:String)->bool:
 var key:String="carry-turn-"+direction+"-"+heading
 var gear:String="diving-helmet" if helmet_equipped else ""
 var rows:Dictionary=preview_player.frames if gear.is_empty() else preview_player.equipment_frames.get(gear,{})
 if heading==direction or not rows.has(key):return false
 bind_cargo_context();turn_key=key;turn_elapsed=0;turn_duration=preview_player.cycle_seconds(key,gear)
 direction=heading;state="walk";held_entry=false
 return true
func move(delta:float)->void:
 if preview_player==null or stage!="workshop_carry" or movement_medium!="dry" or path.is_empty():
  clear_cargo_motion();super.move(delta);return
 if motion_active() and not cargo_context_valid():clear_cargo_motion()
 if turn_elapsed>=0:
  turn_elapsed=minf(turn_duration,turn_elapsed+delta)
  if turn_elapsed>=turn_duration:
   turn_elapsed=-1;turn_key=""
   if arrival_pending:
    arrival_pending=false;path.clear();super.arrive()
   else:held_entry=true
  return
 if stop_elapsed>=0:
  var previous:float=stop_elapsed
  var before:float=minf(previous,stop_deceleration)
  stop_elapsed=minf(stop_deceleration+.08,previous+delta)
  var after:float=minf(stop_elapsed,stop_deceleration)
  var travel:float=stop_speed*((after-before)-(after*after-before*before)/(2*stop_deceleration))
  var prior_foot:Vector2=foot
  if travel>0:super.move(travel/(movement_rate()*flood_speed))
  if travel>0 and foot==prior_foot and not path.is_empty():stop_elapsed=previous
  if stop_elapsed>=stop_deceleration+.08:
   stop_elapsed=-1;stop_target=Vector2.INF;path.clear();arrive()
  return
 var gear:String="diving-helmet" if helmet_equipped else ""
 if start_elapsed>=0:
  var previous:float=start_elapsed;start_elapsed=minf(.32,start_elapsed+delta)
  var speed_before:float=clampf((previous-.08)/.24,0,1)
  var speed_after:float=clampf((start_elapsed-.08)/.24,0,1)
  var prior_foot:Vector2=foot
  super.move(delta*(speed_before+speed_after)*.5)
  if previous>=.08 and foot==prior_foot and not path.is_empty():start_elapsed=previous
  if start_elapsed>=.32:
   start_elapsed=-1
   preview_player.current_key=""
   preview_player.motion={"state":"carry","direction":direction,"clip":"","started":preview_time}
  return
 if held_entry and direction=="west" and travel_heading(foot,path[0],direction)==direction:
  bind_cargo_context();start_elapsed=0;held_entry=false;return
 if direction=="west" and path.size()==1:
  var speed:float=movement_rate()*flood_speed
  var distance:float=foot.distance_to(path[0])
  if distance>0 and distance<=speed*.24*.5:
   var bank:Dictionary=preview_player.frames if gear.is_empty() else preview_player.equipment_frames[gear]
   var texture:Texture2D=preview_player.frame_at_elapsed("carry-west",fmod(preview_player.phase,preview_player.cycle_seconds("carry-west",gear)),gear)
   if bank.get("carry-west",[]).find(texture)==2:
    bind_cargo_context();stop_target=path[0];stop_speed=speed;stop_deceleration=2*distance/speed;stop_elapsed=0;return
 if plant(travel_heading(foot,path[0],direction)):return
 held_entry=false
 var segment_seconds:float=foot.distance_to(path[0])/(movement_rate()*flood_speed)
 super.move(minf(delta,segment_seconds))
func arrive()->void:
 if stop_elapsed>=0:
  path=[stop_target];state="walk";return
 if preview_player!=null and stage=="workshop_carry" and movement_medium=="dry":
  # Keep the real consumed endpoint while inherited update runs during the turn.
  path=[foot]
  if plant("north"):
   arrival_pending=true;return
  path.clear()
 super.arrive()
