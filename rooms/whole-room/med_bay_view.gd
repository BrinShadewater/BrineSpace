extends "res://rooms/whole-room/life_support_view.gd"
## Medical's south-only socket, smaller treatment assemblies, registered screens.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func is_animated_prop(prop: Dictionary) -> bool: return not prop.registration.get("dressing",false)
func _ready() -> void:
	super._ready()
	var img := Image.new()
	if img.load("res://assets/material-polish-medical-v1/treatment-equipment.png") != OK: push_error("Failed to load image (rooms/whole-room/med_bay_view.gd)")
	life_texture = ImageTexture.create_from_image(img)
	life_items = []
	for i in range(2):
		var dy := 457.0*i
		var outline: Array = []
		for p in [Vector2(235,148),Vector2(382,148),Vector2(384,218),Vector2(390,231),Vector2(393,249),Vector2(395,249),Vector2(395,227),Vector2(402,218),Vector2(447,218),Vector2(453,230),Vector2(453,363),Vector2(393,366),Vector2(393,481),Vector2(384,543),Vector2(229,543),Vector2(216,477),Vector2(218,250),Vector2(233,226)]: outline.append(p+Vector2(0,dy))
		# Follow the inset bed base below the projecting rails; exclude source floor.
		outline.insert(outline.find(Vector2(384,543+dy)),Vector2(384,494+dy))
		outline.insert(outline.find(Vector2(229,543+dy))+1,Vector2(229,494+dy))
		# Separate stand, bag and tube; their negative spaces reveal the live floor.
		var iv_parts: Array = []
		for shape in [
			[Vector2(177,204),Vector2(191,181),Vector2(198,184),Vector2(197,192),Vector2(188,199),Vector2(187,311),Vector2(178,318),Vector2(177,213),Vector2(160,220),Vector2(154,215),Vector2(156,207),Vector2(176,196),Vector2(182,198)],
			[Vector2(155,224),Vector2(163,218),Vector2(173,224),Vector2(173,256),Vector2(166,264),Vector2(156,257)],
			[Vector2(160,261),Vector2(166,262),Vector2(164,278),Vector2(168,292),Vector2(176,302),Vector2(174,306),Vector2(164,294),Vector2(160,280)],
			[Vector2(157,306),Vector2(162,303),Vector2(180,314),Vector2(204,303),Vector2(211,307),Vector2(211,316),Vector2(190,326),Vector2(208,335),Vector2(209,345),Vector2(202,349),Vector2(181,334),Vector2(160,349),Vector2(152,345),Vector2(151,336),Vector2(172,323),Vector2(157,316)]
		]:
			var iv: Array = []
			for p in shape: iv.append(p+Vector2(0,dy))
			iv_parts.append(iv)
		life_items.append({"id":"med_bed_"+str(i),"rect":Rect2(-169 if i==0 else -60,-98,86,56),"pivot":Vector2(301,548+dy),"width":305.0,"outline":outline,"extras":iv_parts,"screen":Vector2(407,242+dy)})
	life_items.append({"id":"med_console","rect":Rect2(84,-102,80,50),"pivot":Vector2(940,489),"width":309.0,"outline":[Vector2(844,153),Vector2(1031,153),Vector2(1033,170),Vector2(1078,170),Vector2(1085,230),Vector2(1096,270),Vector2(1096,435),Vector2(1042,446),Vector2(1010,433),Vector2(1006,404),Vector2(867,404),Vector2(862,433),Vector2(848,441),Vector2(802,441),Vector2(787,426),Vector2(789,273),Vector2(799,258),Vector2(799,186),Vector2(818,170),Vector2(842,170)],"extras":[[Vector2(926,375),Vector2(947,377),Vector2(961,387),Vector2(968,402),Vector2(967,418),Vector2(953,431),Vector2(956,443),Vector2(968,449),Vector2(967,458),Vector2(960,460),Vector2(942,451),Vector2(940,460),Vector2(966,470),Vector2(968,479),Vector2(961,484),Vector2(933,468),Vector2(906,485),Vector2(896,480),Vector2(896,473),Vector2(918,458),Vector2(918,447),Vector2(906,454),Vector2(896,450),Vector2(894,443),Vector2(902,436),Vector2(913,431),Vector2(899,422),Vector2(895,409),Vector2(896,393),Vector2(908,381)]]})
	# Follow the console's rounded rear shoulder, not its background bounding box.
	life_items[2].outline[3]=Vector2(1064,170)
	life_items[2].outline.insert(4,Vector2(1076,179))
	life_items[2].outline.insert(5,Vector2(1080,191))
	life_items.append({"id":"med_supply","rect":Rect2(106,105,60,42),"pivot":Vector2(941,1010),"width":270.0,"outline":[Vector2(831,657),Vector2(1064,657),Vector2(1078,675),Vector2(1077,994),Vector2(1061,1011),Vector2(819,1011),Vector2(807,997),Vector2(809,735),Vector2(821,725)]})
	dressing=Dressing.new(self,"res://rooms/whole-room/med-bay-composition-v2.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	for prop in props:
		if prop.id=="med_bed_1" and quarter in [1,3]:
			var at:=Vector2(70,24) if quarter==1 else Vector2(-70,7)
			prop.rect.position=at-prop.rect.size*0.5
			prop.sort_y=prop.rect.end.y
	layout[0].kind = 3
	edges = Geometry.edges(layout)
	for edge in edges: edge.open = edge.port
	if dressing!=null: dressing.place()

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	var bounds := super.prop_visual_bounds(prop)
	for outline in prop.registration.get("extras",[]):
		for p in outline: bounds = bounds.expand(life_point(prop,p))
	return bounds

func draw_room_floor(center: Vector2) -> void:
	# Large composite panels are two 48-unit modules, with quieter seams.
	RoomFloor.draw_profile_floor(self,painter,center,Color("a9b4b2"),Color(0.20,0.32,0.32,0.13),2,"sealed")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"sealed")
	if dressing!=null: dressing.floor()
	preload("res://rooms/whole-room/room_services.gd").identity_details(painter,props,"medical",operating)

func draw_registered_prop(prop: Dictionary) -> void:
	draw_prop_base(prop)
	draw_prop_animation(prop)

func draw_prop_base(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var outlines: Array = [prop.registration.outline]
	outlines.append_array(prop.registration.get("extras",[]))
	for outline in outlines:
		var vertices := PackedVector2Array()
		var uv := PackedVector2Array()
		for p in outline:
			vertices.append(life_point(prop,p))
			uv.append(p/Vector2(life_texture.get_size()))
		draw_cached_polygon(vertices,uv,life_texture)

func draw_prop_animation(prop: Dictionary) -> void:
	if prop.registration.get("dressing",false): return
	if not operating: return
	if str(prop.id).begins_with("med_bed"):
		var start: Vector2 = prop.registration.screen
		# Empty beds report equipment readiness, never invented patient vitals.
		for row in range(3):
			var a := start+Vector2(0,row*5)
			var strength := 0.45+0.45*(0.5+0.5*sin(machine_clock*2-row*1.8))
			painter.draw_line(life_point(prop,a),life_point(prop,a+Vector2(20,0)),Color(0.70,0.89,0.85,strength),0.9,true)
	elif prop.id=="med_console":
		for row in range(3):
			var start := life_point(prop,Vector2(870,210+row*15))
			painter.draw_line(start,life_point(prop,Vector2(915+20*sin(machine_clock*1.7+row),210+row*15)),Color("a7d9d4"),1,true)
	elif prop.id=="med_supply":
		var width := 3.0+10.0*fposmod(machine_clock*0.7,1.0)
		painter.draw_line(life_point(prop,Vector2(1024,977)),life_point(prop,Vector2(1024+width,977)),Color("b9e8dc"),1.1,true)

func layout_caption() -> String:
	return "MED BAY / smaller beds / south-facing equipment / %d degrees"%(quarter*90)
