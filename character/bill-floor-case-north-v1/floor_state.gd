extends RefCounted
## Staged cosmetic room state: latest deposited case, no inventory or collision rules.
const FIELD="bill_floor_case"
const SOURCE="bill-north-case4"
static func valid_payload(data:Variant)->bool:
 if not data is Dictionary or data.size()!=3 or data.get("version")!=1 or not data.get("version") is int or data.get("source")!=SOURCE:return false
 var anchor:Variant=data.get("anchor")
 return anchor is Vector2 and anchor.is_finite() and absf(anchor.x)<=192 and absf(anchor.y)<=192
static func valid_rooms(rooms:Variant)->bool:
 if not rooms is Array:return false
 for room in rooms:
  if not room is Dictionary:return false
  if room.has(FIELD) and (room.get("id")!="salvage_workshop" or not valid_payload(room[FIELD])):return false
 return true
static func payload(room:Dictionary)->Dictionary:
 return room[FIELD] if room.get("id")=="salvage_workshop" and valid_payload(room.get(FIELD)) else {}
static func capture_actor(game,service_cell:Vector2i=Vector2i(-1,-1))->Dictionary:
 var a=game.bill_npc;var p=game.grid_view.human_water_player
 var cell:Vector2i=a.goal_cell if service_cell==Vector2i(-1,-1) else service_cell
 return {"stage":a.stage,"goal":a.goal,"cell":a.goal_cell,"foot":a.foot,"active":a.active,"dead":a.dead,"medium":a.movement_medium,"service":a.service_available(game,cell),"until":float(p.stow_plan.get("until",-1))}
static func observe_completed(rooms:Array,before:Dictionary,after:Dictionary,time:float)->bool:
 if before.get("stage")!="workshop_unload" or after.get("stage")=="workshop_unload" or before.get("goal")!="curiosity":return false
 if not is_finite(time) or not before.get("until") is float or before.until<0 or time<before.until:return false
 for state in [before,after]:
  if not state.get("active",false) or state.get("dead",true) or state.get("medium")!="dry" or not state.get("service",false) or state.get("goal") in ["fire-retreat","flood-retreat"]:return false
 if not before.get("cell") is Vector2i or not before.get("foot") is Vector2 or after.get("foot")!=before.foot:return false
 var anchor:Vector2=before.foot-(Vector2(before.cell)+Vector2.ONE*.5)*384
 var data:Dictionary={"version":1,"source":SOURCE,"anchor":anchor}
 if not valid_payload(data):return false
 for room in rooms:
  if room.get("pos")==before.cell and room.get("id")=="salvage_workshop":
   room[FIELD]=data;return true
 return false
