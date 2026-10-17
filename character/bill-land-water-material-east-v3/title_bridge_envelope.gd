extends RefCounted
## Staged title admission gate; no production save schema or source selection.
const CODEC=preload("res://character/bill-land-water-material-east-v3/checkpoint.gd")
static func valid(data:Dictionary)->bool:
 var wet:Variant=data.get("staged_bill_water_bridge")
 if not wet is Dictionary or wet.get("version")!=1:return false
 var state:Variant=data.get("state");var crew:Variant=data.get("crew")
 if not state is Dictionary or not crew is Dictionary:return false
 var bill:Variant=crew.get("bill");var playback:Variant=crew.get("playback",{}).get("bill")
 if not bill is Dictionary or not playback is Dictionary:return false
 if not CODEC.finite_number(wet.get("clock")) or not CODEC.finite_number(wet.get("started")):return false
 if wet.clock!=state.get("visual_time_seconds") or wet.clock<wet.started or wet.clock>=wet.started+.5:return false
 if wet.get("foot")!=bill.get("foot") or bill.get("dead",true) or not bill.get("active",false) or bill.get("direction")!="east" or bill.get("stage")!="":return false
 if not wet.get("gear") in ["","diving-helmet"] or (wet.gear=="diving-helmet")!=bill.get("helmet_equipped"):return false
 return wet.get("playback")==playback
