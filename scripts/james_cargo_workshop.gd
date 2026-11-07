extends "res://rooms/underwater/salvage-workshop-v1/workshop_view.gd"
var room_id := "salvage_workshop"
const FLOOR=preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd")
const CASE_ID="james-floor-case"
const CASE_PIXEL_SCALE=65.28/148.0
var bound_room:Dictionary={}
var case_texture:Texture2D
var case_enabled:=false
var case_anchor:=Vector2.ZERO
var embedded_case:=false
func _ready()->void:
	super._ready()
	var image:=Image.new()
	if preload("res://scripts/safe_image.gd").load_png(image,FLOOR.ART_PATH)==OK:case_texture=ImageTexture.create_from_image(image)
func bind_room(room:Dictionary)->void:
	bound_room=room;embedded_case=false;sync_case()
func sync_case()->void:
	var value:Dictionary=FLOOR.payload(bound_room)
	case_anchor=Vector2(value.anchor) if not value.is_empty() else Vector2.ZERO
	case_enabled=not value.is_empty() and not embedded_case
func bind_frame(texture:Texture2D,player,gear:String,source_anchor:Vector2)->void:
	var index:int=player.bank_for(gear).get("unload-west",[]).find(texture)
	var value:Dictionary=FLOOR.payload(bound_room)
	embedded_case=index>=3 and index<=4 and not value.is_empty() and Vector2(value.anchor).distance_to(source_anchor)<.001
	sync_case()
func configure_embedded(q:int,open_sides:Array,running:bool,time_seconds:float,omitted_sides:Array=[])->void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides);sync_case()
func case_rect()->Rect2:return Rect2(case_anchor-Vector2(128,224)*CASE_PIXEL_SCALE,Vector2(256,256)*CASE_PIXEL_SCALE)
func _sorted_content_queue(live:Array)->Array:
	var queue:Array=super._sorted_content_queue(live)
	if case_enabled:
		var prop:Dictionary={"id":CASE_ID,"rect":case_rect(),"sort_y":case_anchor.y-2*CASE_PIXEL_SCALE,"registration":{},"library_asset":true,"custom_library_draw":true}
		var item:Dictionary={"kind":"prop","sort_y":prop.sort_y,"prop":prop}
		var at:int=queue.size()
		for index in queue.size():
			if float(queue[index].sort_y)>float(item.sort_y):at=index;break
		queue.insert(at,item)
	return queue
func prop_visual_bounds(prop:Dictionary)->Rect2:
	if prop.id==CASE_ID:return prop.rect
	return super.prop_visual_bounds(prop)
func draw_registered_prop(prop:Dictionary)->void:
	if prop.id==CASE_ID:painter.draw_texture_rect(case_texture,prop.rect,false);return
	super.draw_registered_prop(prop)

# Snapshot only visible case state; actor-containing rooms keep full preparation.
func retained_floor_case_key()->Dictionary:
	return FLOOR.payload(bound_room).duplicate(true)
