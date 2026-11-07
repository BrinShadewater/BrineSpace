extends RefCounted
## Explicit candidate save wrapper; standard Title Continue still selects normal crew.
const SAVE=preload("res://scripts/run_save.gd")
const ACTOR=preload("res://character/bill-carry-cardinal-runtime-v3/stow_actor.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
static func valid_candidate(data:Dictionary)->bool:
 if not SAVE.problem(data).is_empty():return false
 if not data.get("crew") is Dictionary or not data.crew.get("playback") is Dictionary or not data.crew.playback.get("bill") is Dictionary or not data.crew.playback.bill.get("water") is Dictionary:return false
 var actor:Dictionary=data.crew.bill;var player:Dictionary=data.crew.playback.bill.water
 if not ACTOR.valid_carry_snapshot(actor) or not PLAYER.valid_carry_snapshot(player):return false
 var clock:float=data.state.visual_time_seconds;var gear:String="diving-helmet" if actor.helmet_equipped else ""
 if player.get("equipment","")!=gear:return false
 var entry:Dictionary=player.carry_start;var plan:Dictionary=player.carry_stow
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
static func restore_staged(game,data:Dictionary)->bool:
 if not valid_candidate(data) or not game.grid_view.human_water_player.admits_loaded_snapshot(data.crew.playback.bill.water):return false
 if not await SAVE.restore_staged(game,data):return false
 var actor=ACTOR.new();actor.preview_player=game.grid_view.human_water_player
 await actor.restore_snapshot(game,data.crew.bill,true);game.bill_npc=actor
 return true
