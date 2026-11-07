extends "res://character/bill-floor-case-north-v1/world_workshop.gd"
## Preserve ownership, suppress duplicate drawing while source embeds the floor case.
var embedded_case:=false
func bind_frame(texture:Texture2D,player,gear:String,source_anchor:Vector2)->void:
 var index:int=player.rows_for(gear).get("unload-north",[]).find(texture)
 var data:Dictionary=FLOOR.payload(bound_room)
 embedded_case=index>=5 and not data.is_empty() and Vector2(data.anchor).distance_to(source_anchor)<.001
 sync_case()
func sync_case()->void:
 super.sync_case()
 if embedded_case:case_enabled=false
