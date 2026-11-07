extends "res://character/bill-carry-cardinal-runtime-v2/stow_player.gd"
const BINDING="bill-cardinal-arrival3-eastg3s4-southg2s1-westg2s2-northg1s1-rise1"
const DIRECTIONS=["east","south","west","north"]
func carry_binding()->String:
 return BINDING
func snapshot()->Dictionary:
 var data=super.snapshot();data.carry_binding=carry_binding();data.carry_start=start_motion.duplicate(true);data.carry_stow=stow_plan.duplicate(true);data.carry_cache={}
 if last_carry!=null and rows_for(last_carry_gear).has(last_carry_key):
  var index:int=rows_for(last_carry_gear)[last_carry_key].find(last_carry)
  if index>=0:data.carry_cache={"key":last_carry_key,"index":index,"gear":last_carry_gear,"time":last_carry_time}
 return data
static func finite_nonnegative(value:Variant)->bool:
 return (value is float or value is int) and is_finite(float(value)) and value>=0
static func valid_carry_snapshot(data:Variant)->bool:
 if not preload("res://scripts/crew_sprite_player.gd").valid_snapshot(data) or data.get("carry_binding","")!=BINDING:return false
 for key in ["carry_start","carry_stow","carry_cache"]:
  if not data.get(key) is Dictionary:return false
 var gear:String=str(data.get("equipment",""))
 if gear not in ["","diving-helmet"]:return false
 var entry:Dictionary=data.carry_start;var plan:Dictionary=data.carry_stow;var cache:Dictionary=data.carry_cache
 if not cache.is_empty():
  if cache.size()!=4 or cache.get("gear")!=gear or not cache.get("index") is int or cache.index<0 or cache.index>32 or not finite_nonnegative(cache.get("time")):return false
  if not cache.get("key") is String:return false
  var allowed:=false
  for direction in DIRECTIONS:
   if cache.key in ["carry-"+direction,"carry-start-"+direction]:allowed=true
  if not allowed:return false
 if not entry.is_empty():
  if entry.size()!=3 or entry.get("gear")!=gear or entry.get("direction") not in DIRECTIONS or not finite_nonnegative(entry.get("started")):return false
  if data.key!="carry-"+entry.direction or data.get("motion",{}).get("state","")!="carry" or data.motion.get("direction","")!=entry.direction or not str(data.motion.get("clip","")).is_empty():return false
 if not plan.is_empty():
  if not entry.is_empty() or not data.get("motion",{}).is_empty() or cache.is_empty():return false
  if plan.size()!=6 or plan.get("gear")!=gear or plan.get("arrival_direction") not in DIRECTIONS or not plan.get("rows") is Array or plan.rows.is_empty() or plan.rows.size()>64:return false
  for key in ["started","unload_started","until"]:
   if not finite_nonnegative(plan.get(key)):return false
  if plan.unload_started<=plan.started or absf(plan.until-plan.unload_started-2)>.00001:return false
  var total:=0.0
  for row in plan.rows:
   if not row is Dictionary or row.size()!=3 or not row.get("key") is String or row.key.length()>64 or not row.get("index") is int or row.index<0 or row.index>32:return false
   if not finite_nonnegative(row.get("seconds")) or row.seconds<=0 or row.seconds>2:return false
   total+=float(row.seconds)
  if absf(total-(plan.until-plan.started))>.00001:return false
 return true
func admits_loaded_snapshot(data:Dictionary)->bool:
 if not valid_carry_snapshot(data):return false
 var gear:String=str(data.get("equipment",""));var rows:Dictionary=rows_for(gear)
 if not data.key.is_empty() and not rows.has(data.key):return false
 var cache:Dictionary=data.carry_cache
 if not cache.is_empty() and (not rows.has(cache.key) or cache.index>=rows[cache.key].size()):return false
 var entry:Dictionary=data.carry_start
 if not entry.is_empty():
  var key:String="carry-start-"+entry.direction
  if not rows.has(key):return false
  if not cache.is_empty():
   if cache.key!=key or cache.time<entry.started or cache.time-entry.started>=cycle_seconds(key,gear):return false
   if frame_at_elapsed(key,cache.time-entry.started,gear)!=rows[cache.key][cache.index]:return false
 var plan:Dictionary=data.carry_stow
 if not plan.is_empty():
  var probe=preload("res://character/bill-carry-cardinal-runtime-v2/stow_player.gd").new()
  probe.frames=frames;probe.timing=timing;probe.equipment_frames=equipment_frames;probe.equipment_timing=equipment_timing
  probe.last_carry=rows[cache.key][cache.index];probe.last_carry_key=cache.key;probe.last_carry_gear=gear;probe.last_carry_time=cache.time
  if not probe.begin_stow(float(plan.started),gear,plan.arrival_direction) or probe.stow_plan!=plan:return false
 return true
func restore_snapshot(data:Dictionary)->void:
 if not admits_loaded_snapshot(data):return
 super.restore_snapshot(data);start_motion=data.carry_start.duplicate(true);stow_plan=data.carry_stow.duplicate(true);last_carry=null;last_carry_key="";last_carry_gear="";last_carry_time=-1
 var cache:Dictionary=data.carry_cache
 if not cache.is_empty():
  last_carry=rows_for(cache.gear)[cache.key][cache.index];last_carry_key=cache.key;last_carry_gear=cache.gear;last_carry_time=float(cache.time)
