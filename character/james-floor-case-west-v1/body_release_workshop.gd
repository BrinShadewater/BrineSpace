extends "res://character/james-floor-case-west-v1/release_workshop_v6.gd"
func bind_frame(texture:Texture2D,player,gear:String,source_anchor:Vector2)->void:
	var index:int=player.bank_for(gear).get("unload-west",[]).find(texture)
	var data:Dictionary=FLOOR.payload(bound_room)
	# Slots3..5 retain embedded case; terminal6 is exact registered idle body only.
	embedded_case=index>=3 and index<=5 and not data.is_empty() and Vector2(data.anchor).distance_to(source_anchor)<.001
	sync_case()
