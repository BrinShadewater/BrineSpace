extends "res://rooms/underwater/batch-two/biodome_view.gd"
## Biological processing, distinct from cultivated plants in the Biodome.
func _ready() -> void:
	super._ready()
	# Bio Lab replaces the parent's host registrations below. Its floor cannot
	# retain Biodome-only routes/supports that reference those removed hosts.
	dressing=null
	var source:=Image.new()
	if source.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/material-polish-bio-v2/bio-equipment.png")) != OK: push_error("Failed to load image (rooms/underwater/batch-two/bio_lab_view.gd)")
	life_texture=ImageTexture.create_from_image(source)
	life_items=[
		{"id":"bio_reactors","rect":Rect2(-160,-125,100,78),"pivot":Vector2(354,459),"width":294.0,"outline":[Vector2(208,337),Vector2(215,221),Vector2(226,204),Vector2(232,204),Vector2(232,185),Vector2(246,166),Vector2(273,157),Vector2(297,159),Vector2(321,174),Vector2(333,176),Vector2(333,159),Vector2(374,159),Vector2(378,178),Vector2(389,177),Vector2(405,165),Vector2(430,157),Vector2(455,161),Vector2(475,176),Vector2(478,202),Vector2(490,205),Vector2(498,223),Vector2(501,437),Vector2(488,459),Vector2(223,459),Vector2(208,444)]},
		{"id":"bio_culture","rect":Rect2(56,-151,110,78),"pivot":Vector2(887,470),"width":346.0,"outline":[Vector2(716,199),Vector2(728,186),Vector2(901,186),Vector2(904,179),Vector2(917,170),Vector2(1033,170),Vector2(1044,181),Vector2(1058,198),Vector2(1060,454),Vector2(1047,470),Vector2(728,470),Vector2(715,457)]},
		{"id":"bio_centrifuge","rect":Rect2(-160,49,78,60),"pivot":Vector2(335,1049),"width":259.0,"outline":[Vector2(208,765),Vector2(220,742),Vector2(235,740),Vector2(240,723),Vector2(258,718),Vector2(435,718),Vector2(455,731),Vector2(465,756),Vector2(464,1027),Vector2(449,1049),Vector2(220,1049),Vector2(207,1033)]},
		{"id":"bio_cold_storage","rect":Rect2(94,101,68,54),"pivot":Vector2(906,1054),"width":282.0,"outline":[Vector2(773,696),Vector2(786,676),Vector2(800,674),Vector2(1018,674),Vector2(1033,688),Vector2(1042,711),Vector2(1047,1033),Vector2(1035,1054),Vector2(779,1054),Vector2(765,1039),Vector2(766,850),Vector2(773,845)]}
	]
	dressing=Dressing.new(self,"res://rooms/underwater/batch-two/bio-composition-v2.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=0 # West/east/south tee from RoomDatabase.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("29352c"))
	var span:=rect.size.x if horizontal else rect.size.y
	var cursor:=0.0
	while cursor<span:
		var length:=minf(48,span-cursor)
		var target:=Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(248,43,130,38) if horizontal else Rect2(57,132,27,90))
		cursor+=length
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("d9ded6"),0.7)

func draw_cap(rect: Rect2) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("29352c"))
	painter.draw_texture_rect_region(life_texture,top,Rect2(57,44,28,36))

func display_regions(prop: Dictionary) -> Array:
	match prop.id:
		"bio_reactors": return [Rect2(344,272,21,28),Rect2(344,312,21,15),Rect2(345,342,19,17)]
		"bio_culture": return [Rect2(741,333,53,25)]
		"bio_centrifuge": return [Rect2(338,900,40,18)]
		"bio_cold_storage": return [Rect2(1003,795,14,17)]
	return []

func effect_region(prop: Dictionary) -> Rect2:
	match prop.id:
		"bio_reactors": return Rect2(244,274,220,55)
		"bio_culture": return Rect2(744,336,46,19)
		"bio_centrifuge": return Rect2(341,903,34,12)
		"bio_cold_storage": return Rect2(1005,798,10,12)
	return Rect2()

func effect_surfaces(prop: Dictionary) -> Array:
	# Twin vessels share a host, not a fluid surface. Exclude the dry controller.
	if prop.id=="bio_reactors": return [Rect2(244,274,61,55),Rect2(395,274,62,55)]
	return [effect_region(prop)]

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	match prop.id:
		"bio_reactors":
			for x in [251,274,296,402,425,449]:
				var y:=321-fposmod(time*18+x*0.17,41)
				marks.append([Vector2(x,y),Vector2(x,y+4)])
		"bio_culture":
			var x:=750+fposmod(time*16,34)
			marks.append([Vector2(x,340),Vector2(x,351)])
		"bio_centrifuge":
			marks.append([Vector2(344,908),Vector2(356+sin(time*2)*10,908)])
		"bio_cold_storage":
			var y:=801+sin(time*1.5)*2
			marks.append([Vector2(1007,y),Vector2(1013,y)])
	return marks

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices:=PackedVector2Array()
	var uv:=PackedVector2Array()
	for point in prop.registration.outline:
		vertices.append(life_point(prop,point))
		uv.append(point/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	for region in display_regions(prop):
		painter.draw_rect(Rect2(life_point(prop,region.position),region.size*(prop.rect.size.x/prop.registration.width)),Color("26342e"))
	if not operating: return
	for mark in effect_marks(prop,machine_clock): painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("b7d2b4"),0.85,true)

func layout_caption() -> String:
	return "BIO LAB / south-facing biological processing / %d degrees"%(quarter*90)
