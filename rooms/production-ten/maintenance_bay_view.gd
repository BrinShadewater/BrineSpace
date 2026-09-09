extends "res://rooms/whole-room/life_support_view.gd"
## Tooling and diagnostic activity are separate from static stored hull panels.
const FLOOR_CUTOUTS = {
	"maintenance_diagnostics":[[Vector2(997,710),Vector2(981,697),Vector2(861,697),Vector2(846,707),Vector2(846,720),Vector2(865,720),Vector2(976,720),Vector2(998.25,720)],[Vector2(998.25,720),Vector2(976,720),Vector2(976,730),Vector2(999.5,730)],[Vector2(846,730),Vector2(865,730),Vector2(865,720),Vector2(846,720)],[Vector2(804,1066),Vector2(832,1066),Vector2(845,1047),Vector2(995,1047),Vector2(1011,1068),Vector2(1036,1068),Vector2(1050,1046),Vector2(1051,967),Vector2(1066,955),Vector2(1067,826),Vector2(1057,793),Vector2(1043,779),Vector2(1018,777),Vector2(1015,741),Vector2(1000,734),Vector2(999.5,730),Vector2(976,730),Vector2(865,730),Vector2(846,730),Vector2(846,733),Vector2(829,744),Vector2(825,777),Vector2(802,777),Vector2(792,798),Vector2(792,1047)]]
}
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/production-ten/maintenance_bay-source-v1.png")) != OK: push_error("Failed to load image (rooms/production-ten/maintenance_bay_view.gd:11)")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"maintenance_repair","rect":Rect2(-167,-122,94,60),"pivot":Vector2(330,518),"width":384.0,"outline":[Vector2(138,221),Vector2(151,201),Vector2(169,201),Vector2(169,172),Vector2(224,172),Vector2(230,188),Vector2(310,186),Vector2(321,176),Vector2(351,173),Vector2(352,164),Vector2(448,141),Vector2(475,148),Vector2(481,171),Vector2(481,198),Vector2(504,199),Vector2(519,215),Vector2(521,500),Vector2(504,518),Vector2(151,518),Vector2(138,500)]},
		{"id":"maintenance_tools","rect":Rect2(71,-123,96,60),"pivot":Vector2(933,518),"width":394.0,"outline":[Vector2(758,134),Vector2(1107,134),Vector2(1110,256),Vector2(1127,266),Vector2(1130,499),Vector2(1115,518),Vector2(751,518),Vector2(736,502),Vector2(736,289),Vector2(744,267),Vector2(757,258)]},
		{"id":"maintenance_panels","rect":Rect2(-166,107,70,44),"pivot":Vector2(308,1108),"width":346.0,"outline":[Vector2(135,799),Vector2(152,777),Vector2(160,777),Vector2(161,699),Vector2(171,689),Vector2(184,694),Vector2(190,707),Vector2(380,706),Vector2(386,691),Vector2(405,691),Vector2(414,705),Vector2(415,734),Vector2(436,735),Vector2(439,712),Vector2(453,713),Vector2(461,731),Vector2(464,777),Vector2(475,788),Vector2(480,1089),Vector2(464,1108),Vector2(151,1108),Vector2(136,1092)]},
		{"id":"maintenance_diagnostics","rect":Rect2(65,90,64,42),"pivot":Vector2(929,1068),"width":276.0,"outline":[Vector2(792,798),Vector2(802,777),Vector2(825,777),Vector2(829,744),Vector2(846,733),Vector2(846,707),Vector2(861,697),Vector2(981,697),Vector2(997,710),Vector2(1000,734),Vector2(1015,741),Vector2(1018,777),Vector2(1043,779),Vector2(1057,793),Vector2(1067,826),Vector2(1066,955),Vector2(1051,967),Vector2(1050,1046),Vector2(1036,1068),Vector2(1011,1068),Vector2(995,1047),Vector2(845,1047),Vector2(832,1066),Vector2(804,1066),Vector2(792,1047)]}
	]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/maintenance-composition-v3.json")

	rebuild()

func rebuild() -> void:
	super.rebuild()
	if dressing!=null: dressing.place()
	layout[0].kind=0 # Canonical west/east/south tee.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_floor(painter,center,Color("424648"),Color(0.12,0.14,0.15,0.4),2)
	RoomFloor.draw_dressing(painter,center,edges,"steel")

	if dressing!=null: dressing.floor()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("252927"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(219,18,126,45) if horizontal else Rect2(16,110,40,140))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(17,20,46,42))

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="maintenance_repair":
		# Rotation cue contained on the clamped part; the fixed servicing arm stays still.
		var d := Vector2.from_angle(time*1.8)
		marks.append([Vector2(284,311)+d*18,Vector2(284,311)+d*31])
	elif prop.id=="maintenance_diagnostics":
		for row in range(3):
			marks.append([Vector2(866,783+row*18),Vector2(907+23*sin(time*2+row),783+row*18)])
	return marks

func is_animated_prop(prop: Dictionary) -> bool:
	return prop.id in ["maintenance_repair","maintenance_diagnostics"]

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	for outline in FLOOR_CUTOUTS.get(prop.id,[prop.registration.outline]):
		var vertices := PackedVector2Array()
		var uv := PackedVector2Array()
		for p in outline:
			vertices.append(life_point(prop,p))
			uv.append(p/Vector2(life_texture.get_size()))
		draw_cached_polygon(vertices,uv,life_texture)
	if dressing!=null: dressing.draw_supported(prop)
	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("e2bd82"),1.15,true)

