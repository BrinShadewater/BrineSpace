extends RefCounted
const ACTOR=preload("res://character/bill-carry-cardinal-runtime-v3/stow_actor.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
static func valid(data:Dictionary)->bool:
 if data.get("crew")==null:return true
 var crew:Dictionary=data.get("crew",{})
 var actor:Dictionary=crew.get("bill",{})
 var player:Dictionary=crew.get("playback",{}).get("bill",{}).get("water",{})
 if not actor.has("carry_binding") and not player.has("carry_binding"):return true
 return valid_bound(data)
static func valid_bound(data:Dictionary)->bool:
 if not data.get("crew") is Dictionary or not data.crew.get("playback") is Dictionary or not data.crew.playback.get("bill") is Dictionary or not data.crew.playback.bill.get("water") is Dictionary:return false
 var actor:Dictionary=data.crew.bill;var player:Dictionary=data.crew.playback.bill.water
 var binding:String=str(player.get("carry_binding",""))
 if actor.get("carry_binding","")!=binding or not preload("res://scripts/bill_carry_player.gd").supported_binding(binding):return false
 var actor_schema:Dictionary=actor.duplicate(true);var player_schema:Dictionary=player.duplicate(true)
 actor_schema.carry_binding=ACTOR.BINDING;player_schema.carry_binding=PLAYER.BINDING
 if not ACTOR.valid_carry_snapshot(actor_schema) or not PLAYER.valid_carry_snapshot(player_schema):return false
 var clock:float=data.state.visual_time_seconds;var gear:String="diving-helmet" if actor.helmet_equipped else ""
 var entry:Dictionary=player.carry_start;var plan:Dictionary=player.carry_stow
 # Direct elapsed furniture/death rendering does not advance the generic player.
 # Its remembered gear only binds the active carry program.
 if player.get("equipment","")!=gear and (not entry.is_empty() or not plan.is_empty() or not actor.carry_pivot.is_empty()):return false
 if not entry.is_empty():
  if actor.stage!="workshop_carry" or actor.direction!=entry.direction or actor.get("movement_medium","dry")!="dry" or actor.get("dead",false) or not actor.active or actor.path.is_empty():return false
  if clock<entry.started or clock-entry.started>.337:return false
 if not plan.is_empty():
  var arrival:Dictionary=actor.carry_arrival
  if arrival.is_empty() or clock<plan.started or clock>=plan.until or absf(arrival.clock-clock)>.00001 or absf(arrival.until-plan.until)>.00001 or absf(arrival.unload_started-plan.unload_started)>.00001:return false
 elif not actor.carry_arrival.is_empty():return false
 if not actor.carry_pivot.is_empty():
  var pivot:Dictionary=actor.carry_pivot
  if absf(clock-pivot.clock)>.00001 or player.motion.get("clip","")!=pivot.clip or player.motion.get("direction","")!=actor.direction:return false
  var opposite:bool=pivot.clip.get_slice("-",2)+"-"+pivot.clip.get_slice("-",3) in ["east-west","west-east","north-south","south-north"]
  if absf(pivot.until-float(player.motion.started)-(1.6 if opposite else .8))>.00001:return false
 return true
