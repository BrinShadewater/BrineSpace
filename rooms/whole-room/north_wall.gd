extends RefCounted
## Screen-facing rear wall. Visual only; shared north edges retain the low shell.
static func draw_into(canvas: CanvasItem, room_id: String, cell := Vector2i.ZERO) -> void:
	if room_id=="airlock":
		preload("res://rooms/underwater/airlock-v4/fittings.gd").draw_wall(canvas,cell)
		return
	var warm := room_id in ["crew_hab","crew_lounge"]
	var clinical := room_id in ["med_bay","clone_lab","cryo_chamber","research_lab","xeno_lab"]
	var wet := room_id in ["hydroponics_bay","biodome","underwater_life_support","tidal_condenser"]
	var face := Color("b4ac96") if warm else Color("839994") if clinical or wet else Color("4d6068")
	canvas.draw_rect(Rect2(-192,-240,384,48),face)
	for x in range(-192,192,48):
		canvas.draw_line(Vector2(x,-236),Vector2(x,-194),face.darkened(.22),1)
	# Inset enamel panels, warm timber lining and a shadow under the crown.
	for x in range(-184,184,48):
		var panel:=Rect2(x,-235,40,34)
		canvas.draw_rect(panel,face.lightened(.045),false,.7)
		canvas.draw_line(panel.position+Vector2(1,1),Vector2(panel.end.x-1,panel.position.y+1),face.lightened(.13),.8)
		canvas.draw_line(Vector2(panel.end.x,panel.position.y),panel.end,face.darkened(.22),1)
	for y in range(-238,-196):
		canvas.draw_line(Vector2(-186,y),Vector2(186,y),Color(0,0,0,.10*float(y+238)/42.0),1)
	if warm:
		canvas.draw_rect(Rect2(-187,-203,374,6),Color("716751"))
		for x in range(-184,184,12):
			canvas.draw_line(Vector2(x,-202),Vector2(x+7,-202),Color("a99a79"),.6)
	canvas.draw_rect(Rect2(-196,-246,392,7),face.lightened(.2))
	canvas.draw_line(Vector2(-196,-239),Vector2(196,-239),face.darkened(.4),2)
	canvas.draw_rect(Rect2(-192,-197,384,5),face.darkened(.4))
	for x in [-190,187]:
		canvas.draw_rect(Rect2(x,-239,3,47),face.darkened(.25))
	for x in [-168,159]:
		# Small shielded wall lamps with a restrained pool of light.
		canvas.draw_colored_polygon(PackedVector2Array([Vector2(x,-229),Vector2(x+8,-229),Vector2(x+16,-203),Vector2(x-8,-203)]),Color(1,.86,.57,.075) if warm else Color(.63,.88,.91,.065))
		canvas.draw_rect(Rect2(x-2,-236,12,10),face.darkened(.45))
		canvas.draw_rect(Rect2(x,-233,8,4),Color("e3ce91") if warm else Color("afcfc8"))
		canvas.draw_line(Vector2(x-2,-236),Vector2(x+10,-236),face.lightened(.25),1)
	if warm:
		for x in [-128,-88]:
			canvas.draw_rect(Rect2(x,-231,28,25),Color("69513a"))
			canvas.draw_rect(Rect2(x+3,-228,22,19),Color("c5bd99"))
			canvas.draw_rect(Rect2(x+5,-217,18,6),Color("557764"))
			canvas.draw_circle(Vector2(x+17,-223),3,Color("d4b879"))
			canvas.draw_colored_polygon(PackedVector2Array([Vector2(x+5,-214),Vector2(x+10,-222),Vector2(x+16,-216),Vector2(x+23,-219),Vector2(x+23,-211),Vector2(x+5,-211)]),Color("426253"))
			canvas.draw_line(Vector2(x+2,-229),Vector2(x+25,-229),Color("ad9270"),1)
			canvas.draw_line(Vector2(x+4,-212),Vector2(x+24,-212),Color("8a9a73"),.7)
		canvas.draw_rect(Rect2(85,-229,52,24),Color("746d56"))
		for x in [91,107,123]:
			canvas.draw_rect(Rect2(x,-225,9,14),Color("d1c49f"))
	elif clinical:
		canvas.draw_rect(Rect2(-137,-233,55,29),Color("d4dfd5"))
		canvas.draw_line(Vector2(-110,-231),Vector2(-110,-205),face.darkened(.3),1)
		canvas.draw_line(Vector2(-116,-219),Vector2(-104,-219),Color("548e80"),3)
		canvas.draw_line(Vector2(-110,-225),Vector2(-110,-213),Color("548e80"),3)
		canvas.draw_rect(Rect2(90,-232,25,27),Color("d1d6c3"))
		for y in range(-226,-207,5):
			canvas.draw_line(Vector2(94,y),Vector2(110,y),Color("718c89"),1)
	else:
		canvas.draw_rect(Rect2(-147,-231,64,25),face.darkened(.4))
		for x in range(-141,-89,6):
			canvas.draw_line(Vector2(x,-227),Vector2(x,-211),face.lightened(.15),2)
		canvas.draw_line(Vector2(65,-219),Vector2(156,-219),Color("293b40"),6)
		canvas.draw_line(Vector2(65,-221),Vector2(156,-221),Color("87aaa0") if wet else Color("ac9770"),2)
		canvas.draw_rect(Rect2(93,-232,28,27),face.darkened(.25))
		canvas.draw_circle(Vector2(107,-219),7,Color("c2cbb6"))
		canvas.draw_line(Vector2(107,-219),Vector2(110,-223),Color("34494c"),1)

	# Center bay stays independent of the department fittings on either side.
	if room_id!="airlock" and posmod(cell.x*7+cell.y*11,3)!=1:
		_window(canvas)
	# Recessed mounting shadows, bevels and fasteners give fittings thickness.
	for fitting in ([Rect2(-128,-231,28,25),Rect2(-88,-231,28,25),Rect2(85,-229,52,24)] if warm else [Rect2(-137,-233,55,29),Rect2(90,-232,25,27)] if clinical else [Rect2(-147,-231,64,25),Rect2(93,-232,28,27)]):
		canvas.draw_line(fitting.position+Vector2(0,1),Vector2(fitting.end.x,fitting.position.y+1),Color(1,1,.9,.3),1)
		canvas.draw_line(Vector2(fitting.position.x,fitting.end.y+1),fitting.end+Vector2(2,1),Color(0,0,0,.35),2)
		for x in [fitting.position.x+2,fitting.end.x-2]:
			canvas.draw_circle(Vector2(x,fitting.position.y+3),.8,Color("d4cbbb"))
	if warm:
		for x in [91,107,123]:
			canvas.draw_circle(Vector2(x+4,-223),1,Color("a46a48"))
			for y in [-219,-216]:canvas.draw_line(Vector2(x+2,y),Vector2(x+7,y),Color("8d866c"),.6)
	elif clinical:
		for x in [-115,-106]:canvas.draw_line(Vector2(x,-212),Vector2(x,-207),Color("647e79"),1.5)
	else:
		for x in [73,143]:canvas.draw_rect(Rect2(x,-225,3,11),Color("adb3a0"))
		for angle in [-2.4,-1.6,-.8,0.0]:
			var direction:=Vector2(cos(angle),sin(angle))
			canvas.draw_line(Vector2(107,-219)+direction*4,Vector2(107,-219)+direction*6,Color("34494c"),.7)

static func _window(canvas: CanvasItem) -> void:
	var frame:=Rect2(-43,-235,86,35)
	canvas.draw_style_box(_frame(Color(0,0,0,.3),Color(0,0,0,.15),1),Rect2(-45,-234,90,37))
	canvas.draw_style_box(_frame(Color("657e80"),Color("253d45"),3),frame)
	canvas.draw_line(Vector2(-38,-234),Vector2(38,-234),Color("a3b6ae"),1)
	canvas.draw_line(Vector2(-42,-231),Vector2(-42,-205),Color("8fa5a1"),1)
	canvas.draw_rect(Rect2(-37,-230,74,25),Color("103a49"))
	for y in range(-228,-205,3):
		canvas.draw_line(Vector2(-36,y),Vector2(36,y),Color(.19,.48,.53,float(-205-y)/160.0),3)
	canvas.draw_colored_polygon(PackedVector2Array([Vector2(-36,-205),Vector2(-36,-211),Vector2(-23,-215),Vector2(-10,-209),Vector2(9,-214),Vector2(36,-210),Vector2(36,-205)]),Color("163f46"))
	for at in [Vector2(-23,-222),Vector2(18,-217),Vector2(25,-223)]:
		canvas.draw_colored_polygon(PackedVector2Array([at+Vector2(-3,0),at+Vector2(1,-1),at+Vector2(3,1),at+Vector2(5,-1),at+Vector2(5,2),at+Vector2(1,1)]),Color("608e91"))
	canvas.draw_line(Vector2(-30,-228),Vector2(-34,-216),Color(.7,.9,.9,.22),2)
	canvas.draw_line(Vector2(-25,-228),Vector2(-29,-216),Color(.7,.9,.9,.12),1)
	canvas.draw_rect(Rect2(-1,-231,2,27),Color("607c7f"))
	canvas.draw_rect(Rect2(-44,-204,88,3),Color("9caeaa"))
	for x in [-40,40]:
		for y in [-231,-207]:canvas.draw_circle(Vector2(x,y),1,Color("c3c9b6"))

static func _frame(fill: Color, edge: Color, border: int) -> StyleBoxFlat:
	var box:=StyleBoxFlat.new()
	box.bg_color=fill
	box.border_color=edge
	box.set_border_width_all(border)
	box.set_corner_radius_all(4)
	return box
