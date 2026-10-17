extends RefCounted
const SAVE=preload("res://scripts/run_save.gd")
const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/floor_checkpoint.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const FINISH=preload("res://character/bill-floor-case-north-v1/finish_plan.gd")
const ACTOR=preload("res://character/bill-floor-case-north-v1/finish_actor.gd")
const PLAYER=preload("res://character/bill-floor-case-north-v1/finish_player.gd")
static func problem(data:Dictionary)->String:
 var reason:String=FLOOR_SAVE.problem(data)
 if not reason.is_empty():return reason
 if not data.get("crew") is Dictionary or not data.crew.get("bill") is Dictionary or not data.crew.get("playback") is Dictionary or not data.crew.playback.get("bill") is Dictionary or not data.crew.playback.bill.get("water") is Dictionary:return "Bill finite-exit crew"
 var actor:Dictionary=data.crew.bill;var player:Dictionary=data.crew.playback.bill.water
 var plan:Variant=player.get("finish_exit",{})
 if not ACTOR.valid_finish_snapshot(actor) or not FINISH.valid(plan):return "Bill finite-exit schema"
 if actor.get("finish_binding","")!=player.get("finish_binding",""):return "Bill finite-exit binding"
 if actor.has("finish_binding") and actor.finish_binding!=FINISH.FINISH_BINDING:return "Bill finite-exit binding"
 if actor.get("finish_exit",{}).is_empty()!=plan.is_empty():return "Bill finite-exit pairing"
 if plan.is_empty():return ""
 if actor.get("finish_binding")!=FINISH.FINISH_BINDING:return "Bill finite-exit binding"
 var clock:float=data.state.visual_time_seconds
 if clock<float(plan.started) or clock>=float(plan.until):return "Bill finite-exit clock"
 if plan.gear!=("diving-helmet" if actor.helmet_equipped else "") or player.get("equipment","")!=plan.gear:return "Bill finite-exit gear"
 if not player.carry_start.is_empty() or not player.carry_stow.is_empty():return "Bill finite-exit overlap"
 var entry:Dictionary=actor.finish_exit;var room:Dictionary={}
 for item in data.state.placed_rooms:
  if item.pos==entry.cell:room=item;break
 if room.get("id")!="salvage_workshop":return "Bill finite-exit owning room"
 var anchor:Vector2=entry.foot-(Vector2(entry.cell)+Vector2.ONE*.5)*384
 var expected:Dictionary={"version":1,"source":FLOOR.SOURCE,"anchor":anchor}
 if not FLOOR.valid_payload(expected):return "Bill finite-exit contact"
 if clock>=float(plan.release_at) and FLOOR.payload(room)!=expected:return "Bill finite-exit released floor case"
 return ""
static func detached_player(player):
 var candidate=PLAYER.new()
 for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","carry_banks","active_binding"]:candidate.set(field,player.get(field).duplicate(true) if player.get(field) is Dictionary else player.get(field))
 return candidate
static func write(game,path:String)->Error:
 var data:Dictionary=SAVE.capture(game)
 if not problem(data).is_empty() or not detached_player(game.grid_view.human_water_player).admits_loaded_snapshot(data.crew.playback.bill.water):return ERR_INVALID_DATA
 return SAVE.write(game,path)
static func read(path:String)->Dictionary:
 var data:Dictionary=SAVE.read(path)
 return data if not data.is_empty() and problem(data).is_empty() else {}
static func restore_staged(game,data:Dictionary)->bool:
 if not problem(data).is_empty():return false
 var candidate=detached_player(game.grid_view.human_water_player)
 if not candidate.admits_loaded_snapshot(data.crew.playback.bill.water):return false
 # Normal restore remains responsible for the whole station. Explicit candidate
 # fields are rebound only after complete detached admission, never partially.
 var normal:Dictionary=data.duplicate(true)
 for value in [normal.crew.bill,normal.crew.playback.bill.water]:value.erase("finish_exit");value.erase("finish_binding")
 if not await FLOOR_SAVE.restore_staged(game,normal):return false
 game.grid_view.human_water_player=candidate
 var actor=ACTOR.new();game.bill_npc=actor
 await actor.restore_snapshot(game,data.crew.bill,true)
 candidate.restore_snapshot(data.crew.playback.bill.water)
 return true
