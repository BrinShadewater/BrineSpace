extends RefCounted
## Explicit candidate wrapper. Standard title Continue still uses production actors.
const SAVE=preload("res://scripts/run_save.gd")
const ACTOR=preload("res://character/bill-carry-continuation-v1/carry_actor.gd")
const PLAYER=preload("res://character/bill-carry-continuation-v1/carry_player.gd")
static func valid_candidate(data:Dictionary)->bool:
 if not SAVE.problem(data).is_empty():return false
 if not data.get("crew") is Dictionary or not data.crew.get("playback") is Dictionary:return false
 if not data.crew.playback.get("bill") is Dictionary or not data.crew.playback.bill.get("water") is Dictionary:return false
 if not ACTOR.valid_carry_snapshot(data.crew.bill):return false
 var actor:Dictionary=data.crew.bill;var player:Dictionary=data.crew.playback.bill.water
 if not PLAYER.valid_carry_snapshot(player):return false
 var clock:float=data.state.visual_time_seconds
 if not player.carry_start.is_empty():
  if actor.stage!="workshop_carry" or actor.direction!="east" or actor.get("movement_medium","dry")!="dry" or actor.get("dead",false) or actor.path.is_empty():return false
  if player.carry_start.gear!=("diving-helmet" if actor.helmet_equipped else ""):return false
  var elapsed:float=clock-player.carry_start.started
  if elapsed<0 or elapsed>.337:return false
 if not actor.carry_pivot.is_empty():
  var p:Dictionary=actor.carry_pivot
  if absf(clock-p.clock)>.00001 or player.motion.get("clip","")!=p.clip or player.motion.get("direction","")!=actor.direction:return false
  var opposite:bool=p.clip.get_slice("-",2)+"-"+p.clip.get_slice("-",3) in ["east-west","west-east","north-south","south-north"]
  if absf(p.until-float(player.motion.started)-(1.6 if opposite else .8))>.00001:return false
 return true
static func restore_staged(game,data:Dictionary)->bool:
 if not valid_candidate(data):return false
 if not await SAVE.restore_staged(game,data):return false
 var actor=ACTOR.new();actor.preview_player=game.grid_view.human_water_player
 await actor.restore_snapshot(game,data.crew.bill,true);game.bill_npc=actor
 return true
