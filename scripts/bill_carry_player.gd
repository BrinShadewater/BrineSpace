extends "res://character/bill-carry-cardinal-runtime-v3/stow_player.gd"
## Source versions stay bound for the entire resumed session; no mid-pose migration.
const NORTH2_BINDING="bill-cardinal-arrival3-eastg3s4-southg2s1-westg2s2-northg2s2-rise1"
const CURRENT_BINDING="bill-cardinal-arrival3-eastg3s4-southg3s2-westg2s2-northg2s2-rise1"
const MASTER_BINDING="bill-east-master-family-v1-cardinal-arrival3"
const SOURCE_BINDINGS=[BINDING,NORTH2_BINDING,CURRENT_BINDING,MASTER_BINDING]
const MASTER_BANKS=[
 "res://character/bill-east-idle-master-motion-v1/manifest.json",
 "res://character/bill-east-walk-master-full-v1/manifest.json",
 "res://character/bill-east-reach-adjacent-motion-v2/manifest.json",
 "res://character/bill-east-run-master-v2/manifest.json",
 "res://character/bill-east-carry-master-v1/manifest.json",
 "res://character/bill-east-torch-master-v1/manifest.json",
 "res://character/bill-east-torch-handoffs-master-v1/manifest.json",
 "res://character/bill-east-cargo-handoffs-master-v1/manifest.json",
 "res://character/bill-east-carry-entry-master-v1/manifest.json",
 "res://character/bill-carry-turn-east-seams-v1/manifest.json"]
const NORTH_BANKS=[
 ["res://character/bill-carry-north-gait-v2/bare-manifest.json","res://character/bill-carry-north-gait-v2/helmet-manifest.json"],
 ["res://character/bill-carry-start-north-v2/bare-manifest.json","res://character/bill-carry-start-north-v2/helmet-manifest.json"]]
const SOUTH_BANKS=[
 ["res://character/bill-carry-south-gait-v3/bare-manifest.json","res://character/bill-carry-south-gait-v3/helmet-manifest.json"],
 ["res://character/bill-carry-start-south-v2/bare-manifest.json","res://character/bill-carry-start-south-v2/helmet-manifest.json"]]
const SOURCE_KEYS=["carry-north","carry-start-north","carry-south","carry-start-south",
 "idle-east","walk-east","interact-east","run-east","carry-east","weld-east",
 "torch-draw-east","torch-stow-east","pickup-east","unload-east","carry-start-east",
 "carry-turn-east-south","carry-turn-south-east","carry-turn-north-east","carry-turn-east-north",
 "carry-turn-east-west","carry-turn-west-east","carry-turn-north-south"]
const BANK_FIELDS=["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides"]
var carry_banks:Dictionary={}
var active_binding:String=MASTER_BINDING
static func supported_binding(binding:String)->bool:
 return binding in SOURCE_BINDINGS
func carry_binding()->String:
 return active_binding
func remember_bank()->Dictionary:
 var bank:Dictionary={}
 for field in BANK_FIELDS:
  var source:Dictionary=get(field);var selected:Dictionary={}
  if field.begins_with("equipment_"):
   for gear in source:
    selected[gear]={}
    for key in SOURCE_KEYS:
     if source[gear].has(key):selected[gear][key]=source[gear][key]
  else:
   for key in SOURCE_KEYS:
    if source.has(key):selected[key]=source[key]
  bank[field]=selected.duplicate(true)
 return bank
func load_candidates()->bool:
 if not super.load_candidates():return false
 carry_banks[BINDING]=remember_bank()
 for pair in NORTH_BANKS:
  load_manifest(pair[0],true)
  if not load_equipment_manifest("diving-helmet",pair[1]):return false
 carry_banks[NORTH2_BINDING]=remember_bank()
 for pair in SOUTH_BANKS:
  load_manifest(pair[0],true)
  if not load_equipment_manifest("diving-helmet",pair[1]):return false
 carry_banks[CURRENT_BINDING]=remember_bank();active_binding=CURRENT_BINDING
 for path in MASTER_BANKS:
  # Per-facing stride overrides keep every other direction and legacy bank intact.
  load_manifest(path,true,false)
  var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
  for key in manifest.get("strideDistanceCells",{}):
   var facing_key:String=str(key) if str(key).ends_with("-east") else str(key)+"-east"
   strides[facing_key]=manifest.strideDistanceCells[key]
 carry_banks[MASTER_BINDING]=remember_bank();active_binding=MASTER_BINDING
 return true
func apply_bank(target,bank:Dictionary)->void:
 for field in BANK_FIELDS:
  var destination:Dictionary=target.get(field)
  if field.begins_with("equipment_"):
   for gear in destination:
    for key in SOURCE_KEYS:destination[gear].erase(key)
   for gear in bank[field]:
    if not destination.has(gear):destination[gear]={}
    destination[gear].merge(bank[field][gear].duplicate(true),true)
  else:
   for key in SOURCE_KEYS:destination.erase(key)
   destination.merge(bank[field].duplicate(true),true)
func complete_bank(binding:String)->bool:
 if not carry_banks.has(binding):return false
 var bank:Dictionary=carry_banks[binding]
 for field in BANK_FIELDS:
  if not bank.get(field) is Dictionary:return false
 for gear in ["","diving-helmet"]:
  var rows:Dictionary=bank.frames if gear.is_empty() else bank.equipment_frames.get(gear,{})
  var clock:Dictionary=bank.timing if gear.is_empty() else bank.equipment_timing.get(gear,{})
  for key in SOURCE_KEYS:
   if not rows.get(key) is Array or rows[key].is_empty() or not clock.get(key) is Dictionary:return false
   if not clock[key].get("durations") is Array or clock[key].durations.size()!=rows[key].size():return false
 return true
func select_binding(binding:String)->bool:
 if not supported_binding(binding) or not complete_bank(binding):return false
 apply_bank(self,carry_banks[binding]);active_binding=binding;return true
func admits_loaded_snapshot(data:Dictionary)->bool:
 var binding:String=str(data.get("carry_binding",""))
 if not supported_binding(binding) or not complete_bank(binding):return false
 # Validate a detached bank before changing the live source or pending program.
 var probe=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd").new()
 for field in BANK_FIELDS:probe.set(field,get(field).duplicate(true))
 apply_bank(probe,carry_banks[binding])
 var normalized:Dictionary=data.duplicate(true);normalized.carry_binding=BINDING
 return probe.admits_loaded_snapshot(normalized)
func restore_snapshot(data:Dictionary)->void:
 var restored:Dictionary=data.duplicate(true)
 if not restored.has("carry_binding"):
  restored.carry_binding=BINDING;restored.carry_start={};restored.carry_stow={};restored.carry_cache={}
 if not admits_loaded_snapshot(restored):return
 if not select_binding(restored.carry_binding):return
 super.restore_snapshot(restored)
func clear_carry()->void:
 start_motion.clear();stow_plan.clear();last_carry=null;last_carry_key="";last_carry_gear="";last_carry_time=-1
 if motion.get("state","")=="carry":motion.clear()
