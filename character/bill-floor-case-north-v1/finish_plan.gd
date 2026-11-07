extends RefCounted
## Staged ordinary service exit using unchanged, remaining North unload sources.
const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")
const FINISH_BINDING="bill-north-finish1-case4"
const DURATIONS=[35,35,45,45,50,50,50,50,45,45,35,60,60,35]
static func finite(value:Variant)->bool:
 return (value is float or value is int) and is_finite(float(value)) and float(value)>=0
static func valid(plan:Variant)->bool:
 if not plan is Dictionary:return false
 if plan.is_empty():return true
 if plan.size()!=5 or plan.get("gear") not in ["","diving-helmet"] or not plan.get("rows") is Array or plan.rows.is_empty():return false
 for key in ["started","until","release_at"]:
  if not finite(plan.get(key)):return false
 if absf(float(plan.until)-float(plan.release_at)-.28)>.00001:return false
 var first:Variant=plan.rows[0]
 if not first is Dictionary or not first.get("index") is int or first.index<0 or first.index>13 or plan.rows.size()!=14-first.index:return false
 var cursor:=0.0
 for index in first.index:cursor+=float(DURATIONS[index])/1000.0
 var elapsed:float=float(plan.started)-(float(plan.release_at)-.36)
 var remaining:float=cursor+float(DURATIONS[first.index])/1000.0-elapsed
 if elapsed<0 or remaining<=0 or remaining>float(DURATIONS[first.index])/1000.0+.00001:return false
 var total:=0.0
 for offset in plan.rows.size():
  var row:Variant=plan.rows[offset]
  if not row is Dictionary or row.size()!=2 or not row.get("index") is int or row.index!=first.index+offset or not finite(row.get("seconds")) or row.seconds<=0:return false
  var expected:float=remaining if offset==0 else float(DURATIONS[row.index])/1000.0
  if absf(float(row.seconds)-expected)>.00001:return false
  total+=float(row.seconds)
 return absf(float(plan.until)-float(plan.started)-total)<.00001
static func create(player,shown:Texture2D,gear:String,time:float)->Dictionary:
 if not RELEASE.cue_available(player,gear) or not RELEASE.matches_plan_source(player,shown,gear,time):return {}
 var index:int=player.rows_for(gear)["unload-north"].find(shown)
 if index<0:return {} # Arrival/turn prefixes are distinct unresolved exits.
 var durations:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
 var lengths:Array=durations["unload-north"].durations
 var started:float=player.stow_plan.unload_started
 var elapsed:float=time-started;var cursor:=0.0
 for previous in index:cursor+=float(lengths[previous])/1000.0
 var remaining:float=cursor+float(lengths[index])/1000.0-elapsed
 if remaining<=0:return {} # Extended terminal hold is already outside authored rise.
 var rows:Array=[{"index":index,"seconds":remaining}];var total:float=remaining
 for following in range(index+1,14):
  var seconds:float=float(lengths[following])/1000.0
  rows.append({"index":following,"seconds":seconds});total+=seconds
 return {"gear":gear,"started":time,"until":time+total,"release_at":started+.36,"rows":rows}
static func texture_at(player,plan:Dictionary,time:float)->Texture2D:
 if plan.is_empty() or time<float(plan.started) or time>=float(plan.until):return null
 var cursor:float=time-float(plan.started)
 for row in plan.rows:
  cursor-=float(row.seconds)
  if cursor<0:return player.rows_for(plan.gear)["unload-north"][row.index]
 return null
