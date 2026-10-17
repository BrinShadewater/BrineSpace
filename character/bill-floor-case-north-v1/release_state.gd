extends RefCounted
## Staged inferred release cue: first rising source after the lowest held crouch.
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const RELEASE_INDEX=8
const CUE_HASHES={"":"926d854ae0128a0af5855eeb3359b339990badaf7285fb3b9b6610c2de8da092","diving-helmet":"b268f84b4532f78dc2e6323e4620eb9982148bd4996ccd3d05ffa5dc1189df15"}
static var checked_cues:Dictionary={}
static func matches_plan_source(player,texture:Texture2D,gear:String,time:float)->bool:
 var plan:Dictionary=player.stow_plan
 if plan.is_empty() or plan.get("gear")!=gear or time<float(plan.get("started",INF)) or time>=float(plan.get("until",-1)):return false
 var cursor:float=time-float(plan.started);var pool:Dictionary=player.rows_for(gear)
 for row in plan.get("rows",[]):
  cursor-=float(row.seconds)
  if cursor<0:return pool.get(row.key,[]).size()>int(row.index) and pool[row.key][row.index]==texture
 return false
static func cue_available(player,gear:String)->bool:
 var pool:Dictionary=player.rows_for(gear)
 if not pool.get("unload-north") is Array or pool["unload-north"].size()!=14:return false
 var cue:Texture2D=pool["unload-north"][RELEASE_INDEX]
 if cue==null or not CUE_HASHES.has(gear):return false
 var id:int=cue.get_instance_id()
 if not checked_cues.has(id):checked_cues[id]=cue.get_image().get_data().hex_encode().sha256_text()==CUE_HASHES[gear]
 return checked_cues[id]
static func observe_source(game,texture:Texture2D)->bool:
 var actor=game.bill_npc;var player=game.grid_view.human_water_player
 if texture==null or not actor.active or actor.dead or actor.movement_medium!="dry" or actor.stage!="workshop_unload" or actor.direction!="north" or actor.goal!="curiosity":return false
 if not actor.service_available(game,actor.goal_cell) or not game.occupied.has(actor.goal_cell):return false
 var room:Dictionary=game.occupied[actor.goal_cell]
 if room.get("id")!="salvage_workshop":return false
 var gear:String="diving-helmet" if actor.helmet_equipped else ""
 if not matches_plan_source(player,texture,gear,game.visual_time_seconds):return false
 if not cue_available(player,gear):return false
 var index:int=player.rows_for(gear)["unload-north"].find(texture)
 if index<RELEASE_INDEX:return false
 var anchor:Vector2=actor.foot-(Vector2(actor.goal_cell)+Vector2.ONE*.5)*384
 var payload:Dictionary={"version":1,"source":FLOOR.SOURCE,"anchor":anchor}
 if not FLOOR.valid_payload(payload):return false
 if room.has(FLOOR.FIELD) and not FLOOR.valid_payload(room[FLOOR.FIELD]):return false
 if FLOOR.payload(room)==payload:return false
 room[FLOOR.FIELD]=payload;return true
