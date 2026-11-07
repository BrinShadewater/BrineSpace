extends "res://rooms/new-room-expansion/room_view.gd"
## Seawater plant: vessels, teal membrane skid, pump, console and service cartridges.
func _init() -> void:
	room_id = "desalination_unit"

func rebuild() -> void:
	super.rebuild()
	# Canonical west/east/south tee; the sealed north wall carries the ocean intake.
	layout[0].kind=0
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port

func draw_room_world(include_floor := true) -> void:
	super.draw_room_world(include_floor)
	if shell_pass==2: return
	# This new room retains its custom riser face rather than a painted-shell
	# catalog entry. Reuse the production cap strips, mitred corners and frames
	# so the older base shell does not leave the top of the hull unfinished.
	var catalog=preload("res://rooms/whole-room/riser_catalog.gd")
	var material:String=catalog.material(room_id)
	var caps=preload("res://rooms/whole-room/painted_shell.gd").new()
	caps.room=self
	caps.room_id=room_id
	caps.wall=catalog.texture(material)
	caps.registrations={room_id:catalog.catalog()[material]}
	var db=preload("res://scripts/room_database.gd")
	for side in db.get_layout(db.get_room(room_id).layout).doors:
		caps.ports.append(posmod(["north","east","south","west"].find(side)+quarter,4))
	caps.tops(painter)
	if get_meta("raised_north_visible",false):
		# PaintedShell.north completes this lintel after tops() reserves a north
		# doorway. Keep that continuous crown above the custom riser face too.
		caps.draw_cap_strip(painter,Rect2(-184,-271,368,16))

func equipment(id: String) -> Dictionary:
	for prop in props:
		if str(prop.id)==id: return prop
	return {}

func draw_floor_overlays(_center: Vector2) -> void:
	draw_intake_arrow()
	var vessels:=equipment("library/sp-desalination-vessels-1")
	var membrane:=equipment("library/sp-desalination-membrane-1")
	var cartridges:=equipment("library/sp-desalination-cartridges-1")
	# Flush service channel joins the treatment machinery, under props and crew.
	# Resolve from the effective layout so Studio moves do not leave orphan pipework.
	if not vessels.is_empty() and not membrane.is_empty():
		var a:Rect2=vessels.rect
		var b:Rect2=membrane.rect
		var inlet:=Vector2(a.end.x-5,a.position.y+38)
		var outlet:=Vector2(b.position.x+6,b.position.y+38)
		var elbow:=Vector2((inlet.x+outlet.x)*0.5,inlet.y)
		var path:=PackedVector2Array([inlet,elbow,Vector2(elbow.x,outlet.y),outlet])
		painter.draw_polyline(path,Color("202d2c"),8.0)
		painter.draw_polyline(path,Color("567b77"),4.0)
		painter.draw_polyline(path,Color("7b9290"),1.0)
		# Recessed drain at the vessels' service face; a floor surface, not an obstacle.
		var drain:=Rect2(a.position.x+10,a.end.y+7,48,7)
		painter.draw_rect(drain,Color("1b2625"))
		painter.draw_rect(drain,Color("697776"),false,1.0)
		for x in range(6):
			var at:=drain.position+Vector2(5+x*7,1)
			painter.draw_line(at,at+Vector2(0,5),Color("475652"),2.0)
	if not cartridges.is_empty():
		# A maintained cartridge-changing bay: quiet corner paint and a small stencil.
		var zone:Rect2=cartridges.rect.grow(5)
		var ink:=Color("728b85")
		for corner in [zone.position,Vector2(zone.end.x,zone.position.y),zone.end,Vector2(zone.position.x,zone.end.y)]:
			var inward:Vector2=(zone.get_center()-corner).sign()
			painter.draw_line(corner,corner+Vector2(inward.x*10,0),ink,1.0)
			painter.draw_line(corner,corner+Vector2(0,inward.y*10),ink,1.0)
		painter.draw_string(preload("res://scripts/ui_fonts.gd").interface_bold(),Vector2(zone.position.x+5,zone.end.y+12),"FILTERS",HORIZONTAL_ALIGNMENT_LEFT,-1,9,Color("81928a"))

static var intake_stencil_pieces:Array=[]

static func intake_stencil() -> Array:
	if not intake_stencil_pieces.is_empty(): return intake_stencil_pieces
	var pieces:Array=[PackedVector2Array([Vector2(-3,14),Vector2(-3,-12),Vector2(-11,-12),Vector2(0,-32),Vector2(11,-12),Vector2(3,-12),Vector2(3,14)])]
	# Stencil bridges and a few edge nicks reveal the real floor beneath the ink.
	# Every cut reaches an outside edge, so no filled inner rings can erase holes.
	for cut in [Rect2(-15,-18,30,1.2),Rect2(-5,2,10,1.2),Rect2(2,7,3,2),Rect2(-13,-15.5,5,1.3)]:
		var cutter:=PackedVector2Array([cut.position,Vector2(cut.end.x,cut.position.y),cut.end,Vector2(cut.position.x,cut.end.y)])
		var next:Array=[]
		for piece in pieces: next.append_array(Geometry2D.clip_polygons(piece,cutter))
		pieces=next
	intake_stencil_pieces=pieces
	return intake_stencil_pieces

func draw_intake_arrow() -> void:
	# One thin layer of matte paint, without a raised marker's offset shadow.
	var ink:=Color(0.68,0.73,0.65,0.80)
	for piece in intake_stencil():
		var rotated:=PackedVector2Array()
		for point in piece: rotated.append(Geometry.turn(point,quarter))
		painter.draw_colored_polygon(rotated,ink)
	# Larger, lightly compressed lettering sits on the same floor plane. Alpha
	# keeps the deck grain/seams visible; small fixed variations suggest applied ink.
	var font=preload("res://scripts/ui_fonts.gd").interface_bold()
	var letters:="INTAKE"
	var width:=0.0
	for letter in letters: width+=font.get_string_size(letter,HORIZONTAL_ALIGNMENT_LEFT,-1,22).x
	var x:float=-width*0.5
	var baseline:float=(-28.0 if quarter==2 else 38.0)/0.80
	painter.draw_set_transform(view_origin,0,Vector2(view_scale,view_scale*0.80))
	for i in range(letters.length()):
		var paint:=ink
		paint.a=[0.88,0.84,0.86,0.87,0.83,0.88][i]
		painter.draw_string(font,Vector2(x,baseline),letters[i],HORIZONTAL_ALIGNMENT_LEFT,-1,22,paint)
		x+=font.get_string_size(letters[i],HORIZONTAL_ALIGNMENT_LEFT,-1,22).x
	painter.draw_set_transform(view_origin,0,Vector2.ONE*view_scale)
