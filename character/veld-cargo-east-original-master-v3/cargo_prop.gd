extends RefCounted
## Staged visual equipment lifecycle. Resources/credit remain owned by gameplay.
var present := false
var foot := Vector2.ZERO
var action := ""
var event_done := false
var contract: Dictionary = {}
func configure(data: Dictionary) -> void:
 contract=data.duplicate(true)
func begin(clip: String) -> void:
 action=clip
 event_done=false
func advance(elapsed: float, actor_foot: Vector2) -> void:
 if event_done: return
 var event_ms: float=-1.0
 if action=="unload-east": event_ms=float(contract.unloadDepositMs)
 elif action=="pickup-east": event_ms=float(contract.pickupTakeMs)
 if event_ms<0.0 or elapsed*1000.0<event_ms: return
 event_done=true
 if action=="unload-east":
  present=true
  foot=actor_foot
 else: present=false
func retire_on_delivery() -> void:
 present=false
func snapshot() -> Dictionary:
 return {"present":present,"foot":[foot.x,foot.y],"action":action,"eventDone":event_done}
func restore(data: Dictionary) -> bool:
 if not data.get("present") is bool or not data.get("eventDone") is bool: return false
 if not data.get("foot") is Array or data.foot.size()!=2: return false
 if not data.foot[0] is float and not data.foot[0] is int: return false
 if not data.foot[1] is float and not data.foot[1] is int: return false
 var restored_foot:=Vector2(float(data.foot[0]),float(data.foot[1]))
 if not restored_foot.is_finite(): return false
 var restored_action: String=str(data.get("action",""))
 if not restored_action in ["","carry-east","unload-east","idle-east","pickup-east"]: return false
 present=data.present;foot=restored_foot;action=restored_action;event_done=data.eventDone
 return true
