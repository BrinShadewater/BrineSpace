extends "res://rooms/whole-room/life_support_view.gd"
## Blueprints remain empty. Discovered wards supply finite recovery state explicitly.
var recovery: Dictionary = {}:
	set(value):
		var changed: bool = recovery.get("pods",[]).size()!=value.get("pods",[]).size()
		recovery=value
		if changed: layout.clear() # One/two-pod wards cannot reuse the empty blueprint's furniture cache.
var wake_frames: Array[Texture2D] = []
const CryoDressing = preload("res://rooms/whole-room/room_dressing.gd")
var cryo_dressing: RefCounted
func is_animated_prop(prop: Dictionary) -> bool: return not prop.registration.get("dressing",false)
func _ready() -> void:
	super._ready()
	for i in range(6):
		var frame := Image.new()
		assert(frame.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/material-polish-cryo-recovery-v1/bill/wake-%d.png" % i))==OK)
		wake_frames.append(ImageTexture.create_from_image(frame))
	var image := Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/material-polish-cryo-v1/cryo-equipment.png"))==OK)
	life_texture=ImageTexture.create_from_image(image)
	life_items=[]
	for i in range(2):
		var dx := 546.0*i
		var outline: Array=[]
		for p in [Vector2(281,193),Vector2(416,193),Vector2(441,206),Vector2(451,235),Vector2(456,241),Vector2(456,289),Vector2(447,300),Vector2(447,533),Vector2(434,548),Vector2(262,548),Vector2(251,535),Vector2(252,393),Vector2(244,389),Vector2(244,333),Vector2(252,330),Vector2(252,313),Vector2(244,308),Vector2(244,245),Vector2(252,239),Vector2(259,213)]: outline.append(p+Vector2(dx,0))
		life_items.append({"id":"cryo_pod_"+str(i),"rect":Rect2(-143 if i==0 else 81,-147,62,90),"pivot":Vector2(350+dx,548),"width":216.0,"outline":outline,"gauge":Vector2(350+dx,479)})
	life_items.append({"id":"cryo_compressor","rect":Rect2(-160,99,96,57),"pivot":Vector2(344,1018),"width":340.0,"outline":[Vector2(239,727),Vector2(496,727),Vector2(508,740),Vector2(508,1001),Vector2(493,1018),Vector2(250,1018),Vector2(236,1001),Vector2(235,966),Vector2(189,966),Vector2(176,948),Vector2(176,801),Vector2(187,784),Vector2(195,784),Vector2(195,762),Vector2(207,748),Vector2(235,748)]})
	life_items.append({"id":"cryo_console","rect":Rect2(70,99,84,57),"pivot":Vector2(895,1015),"width":245.0,"outline":[Vector2(787,783),Vector2(910,783),Vector2(916,789),Vector2(1001,789),Vector2(1010,799),Vector2(1010,906),Vector2(1016,911),Vector2(1016,940),Vector2(1008,944),Vector2(1008,1005),Vector2(993,1015),Vector2(785,1015),Vector2(773,1004),Vector2(773,802)]})
	cryo_dressing=CryoDressing.new(self,"res://rooms/underwater/batch-two/cryo-composition-v2.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	if not recovery.is_empty() and recovery.pods.size()==1:
		props = props.filter(func(p): return p.id!="cryo_pod_1")
	layout[0].kind=1 # Database north/south straight, not inherited cross.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if not recovery.is_empty(): props=props.filter(func(p): return not p.registration.get("dressing",false))
	elif cryo_dressing!=null: cryo_dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("677975") if not recovery.is_empty() and not recovery.cleared else Color("a9b4b2"),Color(0.20,0.32,0.32,0.13),2,"sealed")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"sealed")
	if recovery.is_empty() and cryo_dressing!=null: cryo_dressing.floor()
	if not recovery.is_empty() and not recovery.cleared:
		# Localized failed hull seams; the maintained medical palette stays legible.
		for x in [-168,168]:
			painter.draw_polyline(PackedVector2Array([Vector2(x,-130),Vector2(x-5,-80),Vector2(x+3,-56),Vector2(x,-20)]),Color("66584c"),3)
		painter.draw_string(ThemeDB.fallback_font,Vector2(-140,175),"SEALED // REPAIRABLE",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("bcb59c"))

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if str(prop.id).begins_with("cryo_pod"):
		var hub: Vector2=prop.registration.gauge
		marks.append([hub,hub+Vector2.from_angle(-1.6+sin(time*1.3)*0.7)*9])
	elif prop.id=="cryo_compressor":
		for hub in [Vector2(410,893),Vector2(460,893),Vector2(410,936),Vector2(460,936)]:
			for blade in range(3):
				var axis:=Vector2.from_angle(time*3+blade*TAU/3)
				marks.append([hub+axis*3,hub+axis*12])
	elif prop.id=="cryo_console":
		for row in range(3): marks.append([Vector2(810,816+row*15),Vector2(846+sin(time*1.7+row)*20,816+row*15)])
	return marks

func draw_registered_prop(prop: Dictionary) -> void:
	if cryo_dressing!=null and cryo_dressing.draw(prop): return
	if not recovery.is_empty() and str(prop.id).begins_with("cryo_pod_"):
		var index := int(str(prop.id).trim_prefix("cryo_pod_"))
		if index >= recovery.pods.size(): return
		var pod: Dictionary = recovery.pods[index]
		if pod.has("architect_id"):
			preload("res://scripts/architect_cryo_art.gd").draw(painter,prop.rect,pod,Color.WHITE if recovery.cleared else Color(0.65,0.70,0.69))
			return
		if not pod.recovered:
			var frame_index := mini(5,int(pod.wake / preload("res://scripts/cryo_recovery.gd").WAKE_SECONDS * 6.0))
			var scale: float = prop.rect.size.x / 290.0
			var base := Vector2(prop.rect.get_center().x,prop.rect.end.y)
			painter.draw_texture_rect(wake_frames[frame_index],Rect2(base-Vector2(210,560)*scale,Vector2(418,627)*scale),false,Color.WHITE if recovery.cleared else Color(0.65,0.70,0.69))
			return
	var vertices:=PackedVector2Array()
	var uv:=PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	if not operating: return
	for mark in effect_marks(prop,machine_clock): painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("97c4bd"),1.0,true)

func layout_caption() -> String:
	return "CRYO / empty pods / south-facing equipment / %d degrees"%(quarter*90)
