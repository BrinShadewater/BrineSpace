extends "res://rooms/whole-room/nursery_south_facing.gd"
## Nursery-only supported supplies; shared source-pixel renderer remains unchanged.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
var life_items: Array=[]

func _ready() -> void:
	super._ready()
	dressing=Dressing.new(self,"res://rooms/whole-room/nursery-composition-v3.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	# Keep source-pixel art and effects together; only this nursery leaf changes.
	var centers:={"rack":Vector2(-10,-100),"bench":Vector2(-106,120),"reservoir":Vector2(125,-61),"filter":Vector2(119,65)}
	for prop in props:
		var target: Vector2=prop.center+Geometry.turn(centers[prop.id],quarter)
		if prop.id=="filter" and quarter in [1,3]:
			target=prop.center+(Vector2(-120,110) if quarter==1 else Vector2(120,-100))
		if prop.id=="filter" and quarter==2: target=prop.center+Vector2(-119,-79)
		if prop.id=="rack" and quarter in [1,3]: target=prop.center+(Vector2(100,-28) if quarter==1 else Vector2(-100,35))
		if prop.id=="bench" and quarter==3: target=prop.center+Vector2(125,125)
		var shift: Vector2=target-prop.rect.get_center()
		prop.rect.position+=shift
		prop.art_offset+=shift
		prop.sort_y=prop.rect.end.y
	for item in life_items:
		var source: Rect2=item.rect
		var rect:=Rect2(Geometry.turn(source.get_center(),quarter)-source.size*0.5,source.size)
		props.append({"id":item.id,"rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":item})
	if dressing!=null: dressing.place()

func life_point(prop: Dictionary, point: Vector2) -> Vector2:
	var r: Dictionary=prop.registration
	return Vector2(prop.rect.get_center().x,prop.rect.end.y)+(point-r.pivot)*(prop.rect.size.x/r.width)

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	super.draw_registered_prop(prop)

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center)
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"steel")
	for prop in props:
		if prop.id not in ["reservoir","filter"]: continue
		var at:=Vector2(prop.rect.get_center().x,prop.rect.end.y+10)
		painter.draw_texture_rect_region(texture,Rect2(at-Vector2(30,4),Vector2(60,8)),Rect2(249,474,181,26))
	if dressing!=null: dressing.floor()
