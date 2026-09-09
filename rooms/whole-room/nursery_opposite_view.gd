extends "res://rooms/whole-room/nursery_whole_view.gd"
## Experimental q2 registration. Rich source pixels, not bitmap rotation.
## Not promoted to the station or cards; artwork review remains separate.
var opposite_texture: ImageTexture
var pipe_outlines := {
	"reservoir": [[Vector2(1057,144),Vector2(1083,144),Vector2(1099,156),Vector2(1099,228),Vector2(1124,230),Vector2(1124,333),Vector2(1109,351),Vector2(1057,351),Vector2(1057,335),Vector2(1100,335),Vector2(1109,326),Vector2(1109,251),Vector2(1084,251),Vector2(1084,163),Vector2(1057,163)]],
	"filter": [[Vector2(155,229),Vector2(130,229),Vector2(113,243),Vector2(112,323),Vector2(125,340),Vector2(153,340),Vector2(153,325),Vector2(132,325),Vector2(128,316),Vector2(128,254),Vector2(138,244),Vector2(155,244)]],
	"rack": [[Vector2(1070,796),Vector2(1095,796),Vector2(1120,814),Vector2(1122,955),Vector2(1109,974),Vector2(1070,974),Vector2(1070,958),Vector2(1099,958),Vector2(1105,951),Vector2(1105,826),Vector2(1089,813),Vector2(1070,813)]]
}
var source_items := {
	"rack": {"outline":[Vector2(718,687),Vector2(742,687),Vector2(742,727),Vector2(1051,727),Vector2(1051,687),Vector2(1074,687),Vector2(1074,990),Vector2(718,990)],"pivot":Vector2(896,990),"width":356.0},
	"bench": {"outline":[Vector2(141,751),Vector2(165,751),Vector2(165,729),Vector2(211,729),Vector2(211,751),Vector2(450,751),Vector2(465,764),Vector2(465,987),Vector2(141,987)],"pivot":Vector2(303,987),"width":324.0},
	"reservoir": {"outline":[Vector2(934,78),Vector2(963,61),Vector2(1018,61),Vector2(1044,76),Vector2(1059,94),Vector2(1059,325),Vector2(1076,345),Vector2(1076,381),Vector2(904,381),Vector2(904,344),Vector2(916,325),Vector2(916,94)],"pivot":Vector2(990,381),"width":172.0},
	"filter": {"outline":[Vector2(153,159),Vector2(180,156),Vector2(180,149),Vector2(232,149),Vector2(233,157),Vector2(264,157),Vector2(265,149),Vector2(310,149),Vector2(311,157),Vector2(343,157),Vector2(344,149),Vector2(393,149),Vector2(394,157),Vector2(443,159),Vector2(452,388),Vector2(145,388)],"pivot":Vector2(298.5,388),"width":307.0}
}

func _ready() -> void:
	var img := Image.new()
	preload("res://scripts/safe_image.gd").load_png(img, "res://rooms/whole-room/nursery-opposite-candidate.png")
	opposite_texture = ImageTexture.create_from_image(img)
	super._ready()

func rebuild() -> void:
	super.rebuild()
	for room in layout:
		room.rotation = 2
	edges = Geometry.edges(layout)
	for edge in edges:
		if not edge.shared: edge.open = edge.port
	for prop in props:
		var original: Rect2 = prop.rect
		var target_center: Vector2 = prop.center + Geometry.turn(original.get_center()-prop.center,2)
		prop.rect = Rect2(target_center-original.size*0.5,original.size)
		prop.sort_y = prop.rect.end.y
	actor = Vector2.ZERO

func draw_room_floor(center: Vector2) -> void:
	# Reuse quiet original floor pixels; no independently generated floor landmarks.
	for y in range(8):
		for x in range(8):
			painter.draw_texture_rect_region(texture,Rect2(center+Vector2(-192+x*48,-192+y*48),Vector2(48,48)),Rect2(571,552,120,120))
	# Panel seams are floor geometry and stay under crew and all machinery.
	for axis in range(2):
		for seam in [-144.0,-96.0,-48.0,0.0,48.0,96.0,144.0]:
			var a := Vector2(seam,-184) if axis == 0 else Vector2(-184,seam)
			var b := Vector2(seam,184) if axis == 0 else Vector2(184,seam)
			a = center+Geometry.turn(a,2)
			b = center+Geometry.turn(b,2)
			painter.draw_line(a,b,Color(0.08,0.10,0.13,0.40),0.7)
			painter.draw_line(a+Vector2(0.6,0.6),b+Vector2(0.6,0.6),Color(0.4,0.43,0.47,0.12),0.5)
	for p in [Vector2(340,488),Vector2(933,424),Vector2(277,1041),Vector2(957,1037)]:
		var at := center+Geometry.turn(pixel_to_world(p),2)
		painter.draw_texture_rect_region(texture,Rect2(at-Vector2(35,5),Vector2(70,10)),Rect2(249,474,181,26))

func source_point(prop: Dictionary, p: Vector2) -> Vector2:
	var source: Dictionary = source_items[prop.id]
	var scale_factor: float = prop.rect.size.x / source.width
	return Vector2(prop.rect.get_center().x,prop.rect.end.y)+(p-source.pivot)*scale_factor

func draw_prop_polygon(prop: Dictionary, outline: Array) -> void:
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for p in outline:
		vertices.append(source_point(prop,p))
		uv.append(p/Vector2(1254,1254))
	painter.draw_polygon(vertices,PackedColorArray([Color.WHITE]),uv,opposite_texture)

func draw_registered_prop(prop: Dictionary) -> void:
	for outline in pipe_outlines.get(prop.id,[]):
		draw_prop_polygon(prop,outline)
	draw_prop_polygon(prop,source_items[prop.id].outline)
	if prop.id == "reservoir" and operating:
		for i in range(8):
			var p := Vector2(942+(i*29)%85,310-fposmod(machine_clock*37+i*23,130))
			painter.draw_circle(source_point(prop,p),0.8,Color(0.65,0.88,0.9,0.48))

func _draw() -> void:
	super._draw()
	painter.draw_string(ThemeDB.fallback_font,Vector2(28,82),"Q2 REGISTRATION STUDY / art review pending",HORIZONTAL_ALIGNMENT_LEFT,-1,14,Color("edaf66"))
