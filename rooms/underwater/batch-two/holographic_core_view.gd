extends "res://rooms/underwater/batch-two/data_archive_view.gd"
## Computing architecture; the local projection is not BRINE's aquatic chamber.
var computing_hull: Texture2D
func _ready() -> void:
	super._ready()
	computing_hull=life_texture
	var source:=Image.new()
	assert(source.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/batch-two/holographic_core-source-v1.png"))==OK)
	life_texture=ImageTexture.create_from_image(source)
	life_items=[
{"id":"holo_projector","rect":Rect2(-172,-139,98,66),"pivot":Vector2(308,487),"width":356.0,"outline":[Vector2(155,167),Vector2(169,156),Vector2(256,159),Vector2(275,143),Vector2(342,143),Vector2(361,157),Vector2(447,157),Vector2(461,170),Vector2(462,219),Vector2(478,239),Vector2(486,346),Vector2(474,363),Vector2(474,432),Vector2(429,487),Vector2(185,487),Vector2(141,444),Vector2(132,417),Vector2(130,351),Vector2(139,333),Vector2(137,242),Vector2(154,218)]},
		{"id":"holo_compute","rect":Rect2(70,-139,84,62),"pivot":Vector2(940,472),"width":316.0,"outline":[Vector2(791,141),Vector2(799,133),Vector2(1080,133),Vector2(1088,142),Vector2(1088,162),Vector2(1096,176),Vector2(1096,457),Vector2(1084,472),Vector2(795,472),Vector2(782,456),Vector2(783,175),Vector2(791,161)]},
		{"id":"holo_calibrator","rect":Rect2(-165,45,70,50),"pivot":Vector2(310,1008),"width":260.0,"outline":[Vector2(184,829),Vector2(201,809),Vector2(232,808),Vector2(233,768),Vector2(255,765),Vector2(258,782),Vector2(267,782),Vector2(267,794),Vector2(276,794),Vector2(276,799),Vector2(297,799),Vector2(298,771),Vector2(322,788),Vector2(323,799),Vector2(340,799),Vector2(341,787),Vector2(348,775),Vector2(379,775),Vector2(382,790),Vector2(393,791),Vector2(410,791),Vector2(414,808),Vector2(435,826),Vector2(439,986),Vector2(425,1008),Vector2(195,1008),Vector2(181,991)]},
		{"id":"holo_terminal","rect":Rect2(66,50,96,52),"pivot":Vector2(922,1012),"width":308.0,"outline":[Vector2(785,789),Vector2(800,780),Vector2(1048,780),Vector2(1059,793),Vector2(1059,807),Vector2(1073,822),Vector2(1076,993),Vector2(1062,1012),Vector2(783,1012),Vector2(768,994),Vector2(769,823),Vector2(782,806)]}
	]
	dressing=Dressing.new(self,"res://rooms/underwater/batch-two/holo-composition-v3.json")
	rebuild()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var equipment:=life_texture
	life_texture=computing_hull
	super.draw_wall(rect,horizontal)
	life_texture=equipment

func draw_cap(rect: Rect2) -> void:
	var equipment:=life_texture
	life_texture=computing_hull
	super.draw_cap(rect)
	life_texture=equipment

func display_regions(prop: Dictionary) -> Array:
	match prop.id:
		"holo_projector": return [Rect2(289,459,39,9),Rect2(279,338,66,9),Rect2(278,148,65,9)]
		"holo_compute": return [Rect2(810,240,44,156),Rect2(881,240,45,156),Rect2(952,240,43,156),Rect2(1023,240,44,156)]
		"holo_calibrator": return [Rect2(239,769,12,11),Rect2(357,779,15,12)]
		"holo_terminal": return [Rect2(877,808,99,59),Rect2(1001,812,20,18)]
	return []

func effect_region(prop: Dictionary) -> Rect2:
	match prop.id:
		"holo_projector": return Rect2(279,185,60,66)
		"holo_compute": return Rect2(813,245,250,145)
		"holo_calibrator": return Rect2(300,797,20,21)
		"holo_terminal": return Rect2(881,812,91,51)
	return Rect2()

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	match prop.id:
		"holo_projector":
			# Two slow wireframe rings imply projected volume over the emitter.
			for ring in range(2):
				var center:=Vector2(308,204+ring*30)
				for i in range(8):
					var a:=TAU*i/8.0+time*0.45
					var b:=TAU*(i+1)/8.0+time*0.45
					marks.append([center+Vector2(cos(a)*24,sin(a)*11),center+Vector2(cos(b)*24,sin(b)*11)])
			for i in range(4):
				var a:=TAU*i/4.0+time*0.45
				var p:=Vector2(308+cos(a)*24,204+sin(a)*11)
				marks.append([p,p+Vector2(0,30)])
		"holo_compute":
			for column in range(4):
				for row in range(4):
					var p:=Vector2(816+71*column,252+row*37)
					marks.append([p,p+Vector2(12+sin(time*1.4+row+column)*7,0)])
		"holo_calibrator":
			var y:=807+sin(time*1.3)*6
			marks.append([Vector2(302,y),Vector2(318,y)])
		"holo_terminal":
			for row in range(4):
				var p:=Vector2(885,819+row*11)
				marks.append([p,p+Vector2(43+sin(time*1.2+row)*28,0)])
	return marks

func layout_caption() -> String:
	return "HOLOGRAPHIC CORE / local projection lattice / %d degrees"%(quarter*90)

func projector_lens_quads() -> Array:
	# Replace only the luminous ring, retaining the recessed lens and housing.
	var quads: Array=[]
	for i in range(32):
		var a:=TAU*i/32.0
		var b:=TAU*(i+1)/32.0
		quads.append([Vector2(308,252)+Vector2(cos(a)*39,sin(a)*30),Vector2(308,252)+Vector2(cos(b)*39,sin(b)*30),Vector2(308,252)+Vector2(cos(b)*32,sin(b)*23),Vector2(308,252)+Vector2(cos(a)*32,sin(a)*23)])
	return quads

func projector_status_lens_quads() -> Array:
	# Source-local lens interiors only; preserve the angled bezels and metal seams.
	return [
		[Vector2(172,162),Vector2(182,161),Vector2(190,167),Vector2(179,168)],
		[Vector2(427,164),Vector2(440,160),Vector2(444,165),Vector2(428,170)],
		[Vector2(184,356),Vector2(194,363),Vector2(189,372),Vector2(178,363)],
		[Vector2(424,364),Vector2(433,357),Vector2(439,364),Vector2(428,372)]
	]

func draw_projector_status_lenses(prop: Dictionary) -> void:
	for quad in projector_status_lens_quads():
		var vertices:=PackedVector2Array()
		var uv:=PackedVector2Array()
		for point in quad:
			vertices.append(life_point(prop,point))
			uv.append(point/Vector2(life_texture.get_size()))
		var value:=0.85 if operating else 0.24
		painter.draw_polygon(vertices,PackedColorArray([Color(value,value,value)]),uv,life_texture)

func draw_terminal_glass(prop: Dictionary,region: Rect2) -> void:
	# Physical glass stays when data/power stops; live traces are drawn afterward.
	var inner:=region.grow(-2)
	var start:=life_point(prop,inner.position)
	painter.draw_rect(Rect2(start,life_point(prop,inner.end)-start),Color("15242e"))
	var reflection:=PackedVector2Array()
	for fraction in [Vector2(0,0),Vector2(0.70,0),Vector2(0.26,1),Vector2(0,1)]:
		reflection.append(life_point(prop,inner.position+inner.size*fraction))
	painter.draw_colored_polygon(reflection,Color("1d303c"))

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices:=PackedVector2Array()
	var uv:=PackedVector2Array()
	for point in prop.registration.outline:
		vertices.append(life_point(prop,point))
		uv.append(point/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	for region in display_regions(prop):
		var start:=life_point(prop,region.position)
		var target:=Rect2(start,life_point(prop,region.end)-start)
		if prop.id=="holo_compute":
			# These are hardware bays, not featureless screens. Preserve their
			# source detail beneath a dim material treatment; activity stays separate.
			painter.draw_texture_rect_region(life_texture,target,region,Color(0.72,0.52,0.48))
		else:
			painter.draw_rect(target,Color("111b23"))
			if prop.id=="holo_terminal": draw_terminal_glass(prop,region)
	if prop.id=="holo_projector":
		draw_projector_status_lenses(prop)
		# Draw individual quads: an annulus is not one simple solid polygon.
		for quad in projector_lens_quads():
			var band:=PackedVector2Array()
			for point in quad: band.append(life_point(prop,point))
			painter.draw_colored_polygon(band,Color("1b2b34"))
	if not operating: return
	for mark in effect_marks(prop,machine_clock): painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("6cbbc4"),0.9,true)
