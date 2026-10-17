extends RefCounted
const SAVE=preload("res://scripts/run_save.gd")
const ACTOR=preload("res://character/bill-carry-return-east-v2/return_actor.gd")
const PLAYER=preload("res://character/bill-carry-return-east-v2/return_player.gd")
static func valid_candidate(data:Dictionary)->bool:
 if not SAVE.problem(data).is_empty():return false
 if not data.get("crew") is Dictionary or not data.crew.get("playback") is Dictionary or not data.crew.playback.get("bill") is Dictionary or not data.crew.playback.bill.get("water") is Dictionary:return false
 var actor:Dictionary=data.crew.bill;var player:Dictionary=data.crew.playback.bill.water
 if not ACTOR.valid_return_snapshot(actor) or not PLAYER.valid_return_snapshot(player):return false
 var plan:Dictionary=player.carry_return;var clock:float=data.state.visual_time_seconds
 if not plan.is_empty():
  if clock<plan.started or clock>=plan.until or absf(actor.carry_return_until-plan.until)>.00001 or plan.gear!=("diving-helmet" if actor.helmet_equipped else ""):return false
 else:
  if actor.carry_return_until!=-1:return false
  var copy:Dictionary=data.duplicate(true);copy.crew.bill.carry_binding="bill-east-turn3-start3-gait2";copy.crew.playback.bill.water.carry_binding="bill-east-turn3-start3-gait2"
  if not preload("res://character/bill-carry-continuation-v1/checkpoint.gd").valid_candidate(copy):return false
 return true
static func restore_staged(game,data:Dictionary)->bool:
 if not valid_candidate(data) or not game.grid_view.human_water_player.admits_loaded_snapshot(data.crew.playback.bill.water):return false
 if not await SAVE.restore_staged(game,data):return false
 var actor=ACTOR.new();actor.preview_player=game.grid_view.human_water_player
 await actor.restore_snapshot(game,data.crew.bill,true);game.bill_npc=actor
 return true
