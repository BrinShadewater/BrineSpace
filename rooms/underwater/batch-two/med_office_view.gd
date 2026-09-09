extends "res://rooms/underwater/batch-two/med_center_view.gd"
## Consultation and records. The desk monitor faces away; do not paint on its back.
var medical_hull: Texture2D
const OfficeDressing = preload("res://rooms/whole-room/room_dressing.gd")
var office_dressing: RefCounted
func rebuild() -> void:
	super.rebuild()
	if office_dressing!=null: office_dressing.place()
func draw_registered_prop(prop: Dictionary) -> void:
	if office_dressing!=null and office_dressing.draw(prop): return
	super.draw_registered_prop(prop)
func draw_room_floor(center: Vector2) -> void:
	super.draw_room_floor(center)
	if office_dressing!=null: office_dressing.floor()
func _ready() -> void:
	super._ready()
	center_dressing=null
	medical_hull=life_texture
	var source:=Image.new()
	assert(source.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/material-polish-medical-v3/office-equipment.png"))==OK)
	life_texture=ImageTexture.create_from_image(source)
	life_items=[
		{"id":"office_desk","rect":Rect2(-159,-142,98,70),"pivot":Vector2(330,493),"width":266.0,"outline":[Vector2(199,321),Vector2(211,309),Vector2(267,309),Vector2(267,270),Vector2(280,260),Vector2(283,222),Vector2(292,212),Vector2(339,212),Vector2(350,222),Vector2(350,260),Vector2(364,268),Vector2(364,297),Vector2(384,298),Vector2(386,309),Vector2(449,309),Vector2(460,322),Vector2(460,480),Vector2(448,493),Vector2(211,493),Vector2(199,481)]},
		{"id":"office_records","rect":Rect2(79,-141,66,64),"pivot":Vector2(941,486),"width":194.0,"outline":[Vector2(847,152),Vector2(856,143),Vector2(1024,143),Vector2(1035,154),Vector2(1035,473),Vector2(1024,486),Vector2(856,486),Vector2(845,475)]},
		{"id":"office_exam","rect":Rect2(-157,30,90,82),"pivot":Vector2(290,1038),"width":242.0,"outline":[Vector2(177,729),Vector2(254,729),Vector2(267,751),Vector2(279,741),Vector2(279,700),Vector2(291,688),Vector2(387,688),Vector2(400,701),Vector2(410,737),Vector2(411,1025),Vector2(399,1038),Vector2(282,1038),Vector2(270,1026),Vector2(270,917),Vector2(253,925),Vector2(180,925),Vector2(170,913),Vector2(170,785),Vector2(177,781)],"pieces":[[Vector2(177,729),Vector2(254,729),Vector2(264,748),Vector2(264,911),Vector2(253,925),Vector2(180,925),Vector2(170,913),Vector2(170,785),Vector2(177,781)],[Vector2(280,701),Vector2(291,688),Vector2(387,688),Vector2(400,701),Vector2(410,737),Vector2(411,1025),Vector2(399,1038),Vector2(282,1038),Vector2(270,1026),Vector2(270,755),Vector2(279,741)]]},
		{"id":"office_consultation","rect":Rect2(70,46,88,72),"pivot":Vector2(928,1038),"width":238.0,"outline":[Vector2(827,764),Vector2(838,754),Vector2(900,754),Vector2(912,765),Vector2(916,805),Vector2(933,805),Vector2(947,763),Vector2(959,754),Vector2(1021,754),Vector2(1033,766),Vector2(1034,805),Vector2(1046,813),Vector2(1047,913),Vector2(1035,926),Vector2(1017,926),Vector2(1017,1026),Vector2(1003,1038),Vector2(853,1038),Vector2(841,1027),Vector2(841,926),Vector2(823,926),Vector2(811,913),Vector2(811,814),Vector2(826,805)],"pieces":[[Vector2(827,764),Vector2(838,754),Vector2(900,754),Vector2(912,765),Vector2(916,805),Vector2(927,814),Vector2(927,913),Vector2(916,926),Vector2(823,926),Vector2(811,913),Vector2(811,814),Vector2(826,805)],[Vector2(947,763),Vector2(959,754),Vector2(1021,754),Vector2(1033,766),Vector2(1034,805),Vector2(1046,813),Vector2(1047,913),Vector2(1035,926),Vector2(947,926),Vector2(935,913),Vector2(935,814),Vector2(946,805)],[Vector2(843,926),Vector2(854,916),Vector2(1005,916),Vector2(1017,927),Vector2(1017,1026),Vector2(1003,1038),Vector2(853,1038),Vector2(841,1027)]]}
	]
	office_dressing=OfficeDressing.new(self,"res://rooms/underwater/batch-two/med-office-composition-v2.json")
	rebuild()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var furniture:=life_texture
	life_texture=medical_hull
	super.draw_wall(rect,horizontal)
	life_texture=furniture

func draw_cap(rect: Rect2) -> void:
	var furniture:=life_texture
	life_texture=medical_hull
	super.draw_cap(rect)
	life_texture=furniture

func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="office_exam"

func effect_region(prop: Dictionary) -> Rect2:
	return Rect2(186,752,59,34) if prop.id=="office_exam" else Rect2()

func effect_marks(prop: Dictionary,time: float) -> Array:
	if not is_animated_prop(prop): return []
	var marks: Array=[]
	for row in range(3): marks.append([Vector2(190,758+row*10),Vector2(220+sin(time*1.2+row)*16,758+row*10)])
	return marks

func layout_caption() -> String:
	return "MEDICAL OFFICE / consultation and records / %d degrees"%(quarter*90)
