extends "res://scripts/major_bill_npc.gd"
## Authoring preview only. Not selected gameplay or a checkpoint-compatible actor.
var preview_player
var preview_time:=0.0
var planted_until:=-1.0
var planted_clip:=""
func update(main,delta:float)->void:
 preview_time=main.get_visual_time_seconds()
 super.update(main,delta)
func move(delta:float)->void:
 if preview_player==null or animation_state()!="carry" or movement_medium!="dry" or path.is_empty():
  planted_until=-1;planted_clip="";super.move(delta);return
 if preview_time<planted_until:return
 planted_until=-1;planted_clip=""
 var heading:String=travel_heading(foot,path[0],direction)
 var key:String="carry-turn-"+direction+"-"+heading
 var gear:String="diving-helmet" if helmet_equipped else ""
 var rows:Dictionary=preview_player.frames if gear.is_empty() else preview_player.equipment_frames.get(gear,{})
 if heading!=direction and rows.has(key):
  # Seed the old facing before the physical heading changes. Rendering owns pixels;
  # this prototype owns the stationary interval and stops at each real waypoint.
  preview_player.frame("carry",direction,preview_time,foot/384.0,gear)
  direction=heading;state="walk";planted_clip=key
  planted_until=preview_time+preview_player.cycle_seconds(key,gear)
  preview_player.frame("carry",direction,preview_time,foot/384.0,gear)
  return
 # Do not consume the next segment in the same update; its heading must be turned
 # before moving. Navigation geometry, route points and movement speed stay intact.
 var segment_seconds:float=foot.distance_to(path[0])/(movement_rate()*flood_speed)
 super.move(minf(delta,segment_seconds))
