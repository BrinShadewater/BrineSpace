extends "res://rooms/underwater/batch-two/xeno_lab_view.gd"
## Retains the Science host; anomalous machinery does not replace socket geometry.
var science_hull: Texture2D
func _ready() -> void:
	super._ready()
	science_hull=life_texture
	var image:=Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, "res://rooms/underwater/batch-two/anomaly_lab-source-v1.png")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"anomaly_platform","rect":Rect2(-54,-135,108,86),"pivot":Vector2(338,507),"width":368.0,"outline":[Vector2(188,179),Vector2(235,179),Vector2(248,186),Vector2(394,186),Vector2(407,179),Vector2(486,179),Vector2(520,211),Vector2(520,266),Vector2(507,280),Vector2(507,384),Vector2(520,403),Vector2(520,474),Vector2(490,506),Vector2(422,507),Vector2(409,496),Vector2(268,496),Vector2(251,507),Vector2(185,507),Vector2(154,476),Vector2(154,407),Vector2(164,390),Vector2(164,270),Vector2(161,257),Vector2(161,211)]},
		{"id":"anomaly_diagnostics","rect":Rect2(65,-10,100,72),"pivot":Vector2(933,478),"width":328.0,"outline":[Vector2(772,262),Vector2(780,253),Vector2(780,215),Vector2(794,200),Vector2(853,200),Vector2(853,187),Vector2(865,173),Vector2(885,169),Vector2(901,173),Vector2(913,187),Vector2(913,200),Vector2(1071,200),Vector2(1087,213),Vector2(1096,236),Vector2(1096,464),Vector2(1085,478),Vector2(779,478),Vector2(770,464)]},
		{"id":"anomaly_capacitors","rect":Rect2(-159,70,98,66),"pivot":Vector2(326,1035),"width":306.0,"outline":[Vector2(188,789),Vector2(448,789),Vector2(464,804),Vector2(464,821),Vector2(474,835),Vector2(478,1020),Vector2(465,1035),Vector2(185,1035),Vector2(173,1020),Vector2(173,849),Vector2(181,832),Vector2(181,800)]},
		{"id":"anomaly_receiver","rect":Rect2(62,96,100,62),"pivot":Vector2(931,1021),"width":304.0,"outline":[Vector2(801,850),Vector2(1060,850),Vector2(1075,862),Vector2(1082,881),Vector2(1083,1007),Vector2(1070,1021),Vector2(793,1021),Vector2(779,1006),Vector2(779,885),Vector2(787,866)]}
	]
	dressing=Dressing.new(self,"res://rooms/underwater/batch-two/anomaly-composition-v2.json")
	rebuild()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	# Science material comes from the verified Xeno host, not the dark candidate shell.
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("2a3a51"))
	var span:=rect.size.x if horizontal else rect.size.y
	var cursor:=0.0
	while cursor<span:
		var length:=minf(48,span-cursor)
		var target:=Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(science_hull,target,Rect2(257,45,120,31) if horizontal else Rect2(74,88,31,120))
		cursor+=length
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("d5dce1"),0.7)

func draw_cap(rect: Rect2) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("2a3a51"))
	painter.draw_texture_rect_region(science_hull,top,Rect2(75,45,34,32))

func display_regions(prop: Dictionary) -> Array:
	match prop.id:
		"anomaly_platform":
			return [Rect2(214,187,12,11),Rect2(263,189,12,11),Rect2(271,198,16,8),Rect2(308,200,12,9),Rect2(274,220,135,9),Rect2(189,229,10,9),Rect2(295,239,11,10),Rect2(361,239,28,10),Rect2(458,247,10,9),Rect2(247,293,10,42),Rect2(425,296,10,37),Rect2(465,295,9,72),Rect2(206,307,9,63),Rect2(308,385,12,9),Rect2(266,405,12,9),Rect2(505,408,9,9),Rect2(300,421,72,10),Rect2(231,428,11,9),Rect2(172,433,25,26),Rect2(481,438,23,21),Rect2(268,473,22,11),Rect2(390,474,24,10)]
		"anomaly_diagnostics":
			return [Rect2(1011,310,10,11),Rect2(1047,406,10,14),Rect2(976,407,31,10),Rect2(1024,407,10,13),Rect2(1036,408,10,11),Rect2(818,410,10,12),Rect2(816,438,10,10)]
		"anomaly_capacitors":
			return [Rect2(255,919,13,42),Rect2(317,918,15,39),Rect2(378,919,17,40),Rect2(257,967,10,9),Rect2(239,1006,9,11),Rect2(253,1006,9,11),Rect2(409,1007,16,10)]
		"anomaly_receiver":
			return [Rect2(831,875,39,39),Rect2(911,875,40,40),Rect2(991,875,40,40),Rect2(1021,938,19,12),Rect2(827,979,32,15),Rect2(1003,979,32,15)]
	return []

func aperture_polygons(prop: Dictionary) -> Array:
	var shapes: Array=[]
	var regions:=display_regions(prop)
	# Small source highlights identified by the strict offline coverage audit.
	match prop.id:
		"anomaly_platform": regions.append_array([Rect2(425,191,4,4),Rect2(297,201,4,3),Rect2(476,261,4,5),Rect2(475,379,4,4)])
		"anomaly_diagnostics": regions.append(Rect2(1013,292,4,4))
		"anomaly_capacitors": regions.append(Rect2(321,970,6,3))
		"anomaly_receiver": regions.append_array([Rect2(975,864,3,4),Rect2(831,905,6,6),Rect2(991,906,3,3)])
	for i in range(regions.size()):
		if prop.id=="anomaly_platform" and i==18:
			shapes.append(PackedVector2Array([Vector2(173,438),Vector2(178,433),Vector2(197,452),Vector2(192,459)]))
			continue
		if prop.id=="anomaly_platform" and i==19:
			shapes.append(PackedVector2Array([Vector2(481,451),Vector2(499,438),Vector2(504,444),Vector2(486,459)]))
			continue
		# Only the receiver's three optical faces are circular.
		shapes.append(display_polygon(regions[i],0 if prop.id=="anomaly_receiver" and i<3 else 1))
	return shapes

func effect_region(prop: Dictionary) -> Rect2:
	match prop.id:
		"anomaly_platform": return Rect2(276,270,124,112)
		"anomaly_diagnostics": return Rect2(802,345,109,17)
		"anomaly_capacitors": return Rect2(254,918,142,44)
		"anomaly_receiver": return Rect2(834,878,195,34)
	return Rect2()

func platform_strip_indices() -> Array:
	return [4,9,10,11,12,16,18,19,20,21]

func platform_lens_polygons(aperture: PackedVector2Array) -> Array:
	# Source-space inset follows angled corner lamps as well as straight strips.
	# Do not re-sample the donor: its painted violet activity survives modulation.
	return Geometry2D.offset_polygon(aperture,-1.5)

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	match prop.id:
		"anomaly_platform":
			var radius:=27+sin(time*1.4)*7
			var center:=Vector2(338,326)
			var corners:=[Vector2(-1,-1),Vector2(1,-1),Vector2(1,1),Vector2(-1,1)]
			for i in range(4): marks.append([center+corners[i]*radius,center+corners[(i+1)%4]*radius])
		"anomaly_diagnostics":
			marks.append([Vector2(810,353),Vector2(867+sin(time*1.8)*25,353)])
		"anomaly_capacitors":
			for x in [261,324,387]:
				var y:=926+fposmod(time*12+x*0.1,20)
				marks.append([Vector2(x,y),Vector2(x,y+8)])
		"anomaly_receiver":
			for i in range(3):
				var center:=Vector2(850+i*80,895)
				var direction:=Vector2.from_angle(time*1.1+i*0.7)
				marks.append([center+direction*2,center+direction*10])
	return marks

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices:=PackedVector2Array()
	var uv:=PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	var shapes:=aperture_polygons(prop)
	for index in range(shapes.size()):
		var points:=PackedVector2Array()
		for p in shapes[index]:
			points.append(life_point(prop,p))
		if prop.id=="anomaly_platform" and index in platform_strip_indices():
			painter.draw_colored_polygon(points,Color("141b24"))
			for shape in platform_lens_polygons(shapes[index]):
				var lens:=PackedVector2Array()
				for p in shape: lens.append(life_point(prop,p))
				painter.draw_colored_polygon(lens,Color("28323e"))
		elif prop.id=="anomaly_receiver" and index<3:
			# Optical glass has depth, but the donor's active points stay suppressed.
			painter.draw_colored_polygon(points,Color("151b25"))
			for inset in [3.0,6.0]:
				var glass:=PackedVector2Array()
				for p in display_polygon(display_regions(prop)[index].grow(-inset),0): glass.append(life_point(prop,p))
				painter.draw_colored_polygon(glass,Color("242b36") if inset==3.0 else Color("1b222d"))
		elif prop.id=="anomaly_capacitors" and index<3:
			# Recessed inactive glass, bounded by the existing suppression aperture.
			# The operating stroke remains a separate state-controlled overlay.
			painter.draw_colored_polygon(points,Color("101923"))
			var region: Rect2=display_regions(prop)[index]
			for inset in [2.0,4.0]:
				var glass:=PackedVector2Array()
				for p in display_polygon(region.grow(-inset),1): glass.append(life_point(prop,p))
				painter.draw_colored_polygon(glass,Color("253747") if inset==2.0 else Color("192735"))
		elif prop.id=="anomaly_receiver" and index==3:
			# The suppression region includes pale fascia, not one large dark lens.
			# Reconstruct that small trim patch, then its actual recessed fitting.
			painter.draw_colored_polygon(points,Color("b8b4b1"))
			for layer in [[Rect2(1022,941,16,7),Color("45464b")],[Rect2(1023,942,14,5),Color("111923")],[Rect2(1024,943,12,3),Color("25313e")]]:
				var detail:=PackedVector2Array()
				for p in display_polygon(layer[0],1): detail.append(life_point(prop,p))
				painter.draw_colored_polygon(detail,layer[1])
		elif prop.id in ["anomaly_diagnostics","anomaly_capacitors","anomaly_receiver"] and index<display_regions(prop).size():
			# Small inactive indicators keep a recessed lens and surrounding bezel.
			# Do not texture-modulate these: the donor's violet glow survives that.
			painter.draw_colored_polygon(points,Color("141b24"))
			var region: Rect2=display_regions(prop)[index].grow(-2.0)
			var segments:=3 if (prop.id=="anomaly_receiver" and index>=4) or (prop.id=="anomaly_diagnostics" and index==2) else 1
			for segment in range(segments):
				var slot:=region
				if segments>1:
					slot.position.x+=segment*region.size.x/segments+1.0
					slot.size.x=region.size.x/segments-2.0
				var lens:=PackedVector2Array()
				for p in display_polygon(slot,1): lens.append(life_point(prop,p))
				painter.draw_colored_polygon(lens,Color("28323e"))
		else:
			# Hardware modulation trial retained visible violet strips offline.
			# Keep suppression until aperture-specific housings are reconstructed.
			painter.draw_colored_polygon(points,Color("23252d"))
	if not operating: return
	for mark in effect_marks(prop,machine_clock): painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("9ebbc7") if prop.id=="anomaly_diagnostics" else Color("a08bb6"),0.95,true)

func layout_caption() -> String:
	return "ANOMALY LAB / contained instrumentation / %d degrees"%(quarter*90)
