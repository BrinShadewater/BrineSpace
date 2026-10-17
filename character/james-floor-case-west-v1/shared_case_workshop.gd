extends "res://character/james-floor-case-west-v1/body_release_workshop.gd"
func _ready()->void:
	super._ready()
	var image:=Image.new()
	preload("res://scripts/safe_image.gd").load_png(image,"res://character/james-floor-case-west-v1/floor-case-west-v7.png")
	case_texture=ImageTexture.create_from_image(image)
func bind_frame(texture:Texture2D,player,gear:String,source_anchor:Vector2)->void:
	var index:int=player.bank_for(gear).get("unload-west",[]).find(texture)
	var data:Dictionary=FLOOR.payload(bound_room)
	embedded_case=index>=3 and index<=4 and not data.is_empty() and Vector2(data.anchor).distance_to(source_anchor)<.001
	sync_case()
