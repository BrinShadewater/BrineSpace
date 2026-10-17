extends RefCounted
const SAVE=preload("res://scripts/run_save.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
static func problem(data:Dictionary)->String:
 if not data.get("state") is Dictionary:return "Bill floor-case state"
 if not FLOOR.valid_rooms(data.get("state",{}).get("placed_rooms")):return "Bill floor-case state"
 return SAVE.problem(data)
static func write(game,path:String)->Error:
 if not problem(SAVE.capture(game)).is_empty():return ERR_INVALID_DATA
 return SAVE.write(game,path)
static func read(path:String)->Dictionary:
 var data:Dictionary=SAVE.read(path)
 return data if not data.is_empty() and problem(data).is_empty() else {}
static func restore_staged(game,data:Dictionary)->bool:
 if not problem(data).is_empty():return false
 return await SAVE.restore_staged(game,data)
