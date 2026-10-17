extends "res://character/bill-carry-start-east-v3/carry_start_preview_player.gd"
## Candidate playback persistence; normal source selection does not load this script.
const BINDING="bill-east-turn3-start3-gait2"
func snapshot()->Dictionary:
 var data=super.snapshot();data.carry_binding=BINDING;data.carry_start=start_motion.duplicate(true);return data
static func valid_carry_snapshot(data:Variant)->bool:
 if not preload("res://scripts/crew_sprite_player.gd").valid_snapshot(data):return false
 if data.get("carry_binding","")!=BINDING or not data.get("carry_start") is Dictionary:return false
 var entry:Dictionary=data.carry_start
 if entry.is_empty():return true
 if entry.size()!=2 or entry.get("gear") not in ["","diving-helmet"]:return false
 if not (entry.get("started") is float or entry.get("started") is int) or not is_finite(float(entry.started)) or entry.started<0:return false
 return data.key=="carry-east" and entry.gear==data.get("equipment","") and data.get("motion",{}).get("state","")=="carry" and data.get("motion",{}).get("direction","")=="east"
func restore_snapshot(data:Dictionary)->void:
 if not valid_carry_snapshot(data):return
 if not data.key.is_empty() and not frames.has(data.key):return
 var gear:String=str(data.get("equipment",""))
 if not gear.is_empty() and not equipment_frames.get(gear,{}).has(data.key):return
 super.restore_snapshot(data);start_motion=data.carry_start.duplicate(true)
