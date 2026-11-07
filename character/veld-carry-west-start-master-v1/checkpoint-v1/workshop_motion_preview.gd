extends "res://character/veld-carry-west-start-master-v1/motion-clock-v1/workshop_motion_preview.gd"
## Staged actor checkpoint contract; normal RunSave selection is not changed.
func source_binding(key:String,equipped:bool)->String:
 if preview_player==null:return ""
 var gear:String="diving-helmet" if equipped else ""
 var bank:Dictionary=preview_player.frames if gear.is_empty() else preview_player.equipment_frames.get(gear,{})
 var times:Dictionary=preview_player.timing if gear.is_empty() else preview_player.equipment_timing.get(gear,{})
 if not bank.has(key) or not times.has(key):return ""
 var digest:=HashingContext.new();digest.start(HashingContext.HASH_SHA256)
 digest.update(JSON.stringify(times[key]).to_utf8_buffer())
 for texture in bank[key]:
  digest.update(texture.get_image().get_data())
  digest.update(str(texture.get_meta("crew_pivot"),texture.get_meta("crew_standing_height"),texture.get_meta("crew_depth_offset",0.0),texture.get_size(),texture.get_meta("crew_water_facing"),texture.get_meta("crew_water_kind"),texture.get_meta("crew_water_pose")).to_utf8_buffer())
 return digest.finish().hex_encode()
func cargo_binding(equipped:bool)->String:
 if preview_player==null:return ""
 var digest:=HashingContext.new();digest.start(HashingContext.HASH_SHA256)
 for key in ["carry-held-east","carry-held-west","carry-turn-east-west","carry-start-west","carry-stop-phase2-west","carry-west","carry-turn-west-north","unload-north","idle-north"]:
  var binding:String=source_binding(key,equipped)
  if binding.is_empty():return ""
  digest.update((key+":"+binding).to_utf8_buffer())
 var strides:Dictionary=preview_player.equipment_strides.get("diving-helmet",{}) if equipped else preview_player.strides
 digest.update(str(strides.get("carry-west",strides.get("carry",.12))).to_utf8_buffer())
 return digest.finish().hex_encode()
func snapshot()->Dictionary:
 var result:Dictionary=super.snapshot();var motion:Dictionary={}
 if motion_active() and cargo_context_valid():
  var kind:String="turn" if turn_elapsed>=0 else "start" if start_elapsed>=0 else "stop" if stop_elapsed>=0 else "held"
  var key:String=animation_state()+"-"+direction
  var elapsed:float=turn_elapsed if kind=="turn" else start_elapsed if kind=="start" else stop_elapsed if kind=="stop" else 0.0
  var duration:float=turn_duration if kind=="turn" else .32 if kind=="start" else stop_deceleration+.08 if kind=="stop" else 0.0
  motion={"version":1,"kind":kind,"key":key,"elapsed":elapsed,"duration":duration,"gear":motion_gear,"goal":motion_goal,"cell":motion_cell,"endpoint":path[-1],"arrival":arrival_pending,"binding":cargo_binding(motion_gear)}
  if kind=="stop":motion.merge({"deceleration":stop_deceleration,"speed":stop_speed,"target":stop_target})
 result.veld_cargo_motion_v1=motion
 return result
static func number(value:Variant)->bool:
 return (value is float or value is int) and is_finite(float(value))
static func valid_cargo_snapshot(data:Variant)->bool:
 if not preload("res://scripts/veld_npc.gd").valid_veld_snapshot(data):return false
 var m:Variant=data.get("veld_cargo_motion_v1",{})
 if not m is Dictionary:return false
 if m.is_empty():return true
 if m.get("version")!=1 or m.get("kind") not in ["held","start","stop","turn"]:return false
 for key in ["dead","movement_medium","helmet_equipped"]:
  if not data.has(key):return false
 if data.state not in ["walk","idle"]:return false
 if data.stage!="workshop_carry" or data.dead or not data.active or data.movement_medium!="dry" or data.path.is_empty():return false
 if not m.get("gear") is bool or m.gear!=data.helmet_equipped or m.get("goal")!=data.goal or m.get("cell")!=data.goal_cell:return false
 if not m.get("endpoint") is Vector2 or not m.endpoint.is_finite() or m.endpoint!=data.path[-1]:return false
 if not m.get("arrival") is bool or not m.get("binding") is String or m.binding.length()!=64:return false
 if not number(m.get("elapsed")) or not number(m.get("duration")) or m.elapsed<0:return false
 if not m.get("key") is String or not m.key.ends_with("-"+data.direction):return false
 if m.kind=="held":return not m.arrival and m.elapsed==0 and m.duration==0 and m.key in ["carry-held-east","carry-held-west"]
 if m.duration<=0 or m.elapsed>=m.duration:return false
 if m.kind=="turn":
  if m.key not in ["carry-turn-east-west","carry-turn-west-north"]:return false
  if not is_equal_approx(m.duration,.68 if m.key=="carry-turn-east-west" else .8):return false
  if m.arrival and (m.key!="carry-turn-west-north" or data.path.size()!=1 or data.foot.distance_to(m.endpoint)>.002):return false
  return true
 if m.arrival or data.direction!="west":return false
 if m.kind=="start":return m.key=="carry-start-west" and is_equal_approx(m.duration,.32)
 if m.key!="carry-stop-phase2-west" or data.path.size()!=1:return false
 if not number(m.get("deceleration")) or m.deceleration<=0 or m.deceleration>.240001:return false
 if not number(m.get("speed")) or m.speed<=0 or m.speed>46.0001:return false
 if not is_equal_approx(m.duration,m.deceleration+.08):return false
 if not m.get("target") is Vector2 or not m.target.is_finite() or m.target!=m.endpoint:return false
 var remaining:float=m.speed*pow(maxf(0,m.deceleration-m.elapsed),2)/(2*m.deceleration)
 return absf(data.foot.distance_to(m.target)-remaining)<.02
func admits_cargo_snapshot(data:Variant)->bool:
 if not valid_cargo_snapshot(data):return false
 var m:Dictionary=data.get("veld_cargo_motion_v1",{})
 return m.is_empty() or m.binding==cargo_binding(m.gear)
func restore_snapshot(main,data:Dictionary,staged:=false)->void:
 # Validate structure AND loaded master/timing binding before mutating the actor.
 if not admits_cargo_snapshot(data):return
 await super.restore_snapshot(main,data,staged)
 clear_cargo_motion()
 if stage!="workshop_carry" or path.is_empty() or dead or not active:return
 var m:Dictionary=data.get("veld_cargo_motion_v1",{})
 if m.is_empty():return
 bind_cargo_context();preview_time=main.get_visual_time_seconds()
 match m.kind:
  "held":held_entry=true
  "start":start_elapsed=m.elapsed
  "stop":stop_elapsed=m.elapsed;stop_deceleration=m.deceleration;stop_speed=m.speed;stop_target=m.target
  "turn":turn_elapsed=m.elapsed;turn_duration=m.duration;turn_key=m.key;arrival_pending=m.arrival
