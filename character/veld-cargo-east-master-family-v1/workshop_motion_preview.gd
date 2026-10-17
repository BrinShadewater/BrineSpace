extends "res://scripts/veld_npc.gd"
## Fixture-only coordinated cargo preview; not selected or checkpoint compatible.
var preview_player
var preview_time:=0.0
var planted_until:=-1.0
var planted_clip:=""
var arrival_pending:=false
var held_entry:=false
func animation_state()->String:
 if held_entry and stage=="workshop_carry":return "carry-held"
 return super.animation_state()
func update(main,delta:float)->void:
 preview_time=main.get_visual_time_seconds()
 if arrival_pending:
  # Authoring-only hold. Interruption/needs/Continue integration is not certified.
  if preview_time<planted_until:return
  arrival_pending=false;planted_until=-1;planted_clip=""
  super.arrive()
  return
 var previous:String=stage
 super.update(main,delta)
 if previous=="workshop_pickup" and stage=="workshop_carry":held_entry=true
func plant(heading:String)->bool:
 var key:String="carry-turn-"+direction+"-"+heading
 var gear:String="diving-helmet" if helmet_equipped else ""
 var rows:Dictionary=preview_player.frames if gear.is_empty() else preview_player.equipment_frames.get(gear,{})
 if heading==direction or not rows.has(key):return false
 preview_player.frame("carry",direction,preview_time,foot/384.0,gear)
 direction=heading;state="walk";held_entry=false;planted_clip=key
 planted_until=preview_time+preview_player.cycle_seconds(key,gear)
 preview_player.frame("carry",direction,preview_time,foot/384.0,gear)
 return true
func move(delta:float)->void:
 if preview_player==null or stage!="workshop_carry" or movement_medium!="dry" or path.is_empty():
  held_entry=false;planted_until=-1;planted_clip="";super.move(delta);return
 if preview_time<planted_until:return
 planted_until=-1;planted_clip=""
 if plant(travel_heading(foot,path[0],direction)):return
 held_entry=false
 # Stop on each real waypoint so a new heading is turned before translating.
 var segment_seconds:float=foot.distance_to(path[0])/(movement_rate()*flood_speed)
 super.move(minf(delta,segment_seconds))
func arrive()->void:
 if preview_player!=null and stage=="workshop_carry" and movement_medium=="dry" and plant("north"):
  arrival_pending=true
  return
 super.arrive()
