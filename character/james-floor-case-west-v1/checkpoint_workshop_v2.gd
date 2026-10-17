extends "res://character/james-floor-case-west-v1/workshop_preview.gd"
const FLOOR=preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd")
var bound_room:Dictionary={}
var embedded_case:=false
func bind_room(room:Dictionary)->void:
	bound_room=room;sync_case()
func sync_case()->void:
	var data:Dictionary=FLOOR.payload(bound_room)
	case_anchor=Vector2(data.anchor) if not data.is_empty() else Vector2.ZERO
	case_enabled=not data.is_empty() and not embedded_case
func configure_embedded(q:int,open_sides:Array,running:bool,time_seconds:float,omitted_sides:Array=[])->void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	sync_case()
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
