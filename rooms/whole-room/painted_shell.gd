extends RefCounted
## Production painted shell. Geometry and placement remain owned by the room view.
const Store=preload("res://scripts/room_layout_store.gd")
const Geometry=preload("res://tools/modular_room_geometry.gd")
const Doors=preload("res://rooms/doors/painted_door.gd")
static var records:Dictionary={}
static var textures:Dictionary={}
var room_id:String
var room
var wall:Texture2D
var registrations:Dictionary={}
var integrated:Dictionary={}
var north_special:Dictionary={}
var ports:Array=[]
static func catalog() -> Dictionary:
	if records.is_empty():records=JSON.parse_string(FileAccess.get_file_as_string("res://assets/architecture-rollout-2026-09-26/walls.json"))
	return records
static func png(path:String) -> Texture2D:
	if not textures.has(path):
		var im:=Image.new()
		if im.load_png_from_buffer(FileAccess.get_file_as_bytes(path))!=OK:return null
		textures[path]=ImageTexture.create_from_image(im)
	return textures[path]
static func id_for(view) -> String:return Store.room_id_for(view,Store.asset_for(view))
static func enabled(view) -> bool:
	return view!=null and view.layout.size()==1 and catalog().has(id_for(view)) and id_for(view) not in ["corridor","corner","tee_corridor"]
static func context(view,id:String=""):
	var ctx=new();ctx.room=view;ctx.room_id=id_for(view) if id.is_empty() else id
	if not catalog().has(ctx.room_id):return null
	var record:Dictionary=catalog()[ctx.room_id]
	var base:Dictionary=record.base
	ctx.integrated=record.integrated
	if view!=null and view.quarter==0:ctx.north_special=record.get("north_special",{})
	# Honour an owner's explicit material selection without changing their saved data.
	var chosen:String=Store.surface_positions(view).get("wall/riser","") if view!=null else ""
	var old=load("res://rooms/whole-room/riser_catalog.gd")
	if not chosen.is_empty() and old.catalog().has(chosen):
		base=old.catalog()[chosen];ctx.integrated={}
		ctx.north_special={}
	ctx.registrations={ctx.room_id:base};ctx.wall=png(base.source)
	if view!=null:
		var db=load("res://scripts/room_database.gd")
		var definition:Dictionary=db.get_room(ctx.room_id)
		for direction in db.get_layout(definition.layout).doors:
			ctx.ports.append(posmod(["north","east","south","west"].find(direction)+int(view.quarter),4))
		for edge in view.edges:
			var side:int=0 if edge.horizontal and edge.center.y<0 else 2 if edge.horizontal else 1 if edge.center.x>0 else 3
			if edge.open and not ctx.ports.has(side):ctx.ports.append(side)
	return ctx
func north(canvas:CanvasItem,adjoining_left:bool=false,adjoining_right:bool=false,static_leaf:bool=true) -> void:
	var ocean:bool=room_id=="airlock" and room!=null and room.quarter==0
	var windows:bool=room!=null and room.get_meta("raised_north_visible",false) and room_id!="brine_core"
	var base:Array=registrations[room_id].face
	var special:bool=not north_special.is_empty()
	if special:base=north_special.face
	for span in [[0.0,.385,-184.0,138.0],[.385,.23,-46.0,92.0],[.615,.385,46.0,138.0]]:
		var sample:Array=base
		var tex:Texture2D=wall
		if special:tex=png(north_special.source)
		if not special and not windows and not integrated.is_empty() and not (span[2]==-46.0 and (ports.has(0) or room_id=="airlock")):
			sample=integrated.face;tex=png(integrated.source)
		if ocean and span[2]==-46.0:
			for x in [-46.0,28.0]:
				canvas.draw_texture_rect_region(tex,Rect2(x,-255,18,79),Rect2(sample[0]+sample[2]*.4,sample[1],sample[2]*.045,sample[3]))
		else:
			canvas.draw_texture_rect_region(tex,Rect2(span[2],-255,span[3],79),Rect2(sample[0]+sample[2]*span[0],sample[1],sample[2]*span[1],sample[3]))
	if windows:
		var inserts=preload("res://rooms/whole-room/ocean_windows.gd")
		if special:
			inserts.draw_room(canvas,room_id,north_special.get("window_reserves",[]),false)
		elif inserts.room_allowed(true,room_id,ports,ocean):
			# Use the authored panel reserves, preserving the central doorway bay.
			inserts.draw_room(canvas,room_id,registrations[room_id].get("window_reserves",[]))
	# Raised assembly owns the top corners/returns even when a card draws north after the shell.
	if ocean:
		draw_cap_strip(canvas,Rect2(-184,-271,368,16))
	else:draw_cap_strip(canvas,Rect2(-184,-271,368,16))
	for x in [-200,184]:
		if (x<0 and adjoining_left) or (x>0 and adjoining_right):continue
		draw_cap_strip(canvas,Rect2(x,-255,16,68),true,x>0)
		draw_cap_corner(canvas,Vector2(x,-271),x>0,false)
	if room_id=="airlock" and room!=null and room.quarter==0:
		preload("res://rooms/doors/ocean_hatch.gd").raised(canvas,0,static_leaf)
	elif ports.has(0) or room_id=="brine_core":Doors.for_variant(room_id).raised_at(canvas,0,0,-255,79)
	if special and room_id=="survey_probe_bay":
		# The fixed launcher straddles the hull; let its housing overlap its matching backplate.
		preload("res://scripts/probe_launcher_mechanics.gd").draw(canvas,float(room.survey_clock),0)
		preload("res://scripts/probe_launcher_mechanics.gd").tunnel(canvas,float(room.survey_clock),str(room.survey_status))
static func draw_ocean_window(canvas:CanvasItem,path:String,center:Vector2,limit:Vector2) -> void:
	var texture:Texture2D=png(path)
	var factor:=minf(limit.x/texture.get_width(),limit.y/texture.get_height())
	var size:=Vector2(texture.get_size())*factor
	canvas.draw_texture_rect(texture,Rect2(center-size*.5,size),false)

func tops(canvas:CanvasItem) -> void:
	var raised:bool=room.get_meta("raised_north_visible",false)
	var present:Array=[]
	for edge in room.edges:present.append(0 if edge.horizontal and edge.center.y<0 else 2 if edge.horizontal else 1 if edge.center.x>0 else 3)
	var top:float=-271 if raised else -203
	for side in present:
		var vertical:bool=side in [1,3]
		var start:float=top+16 if vertical else -184.0
		var finish:float=181 if vertical else 184
		var spans:Array=[[start,finish]]
		if ports.has(side):spans=[[start,-46.0],[46.0,finish]]
		# Exterior hatches are hull openings, not station ports; reserve them in every rotation.
		if room_id=="airlock" and side==room.quarter:spans=[[start,-28.0],[28.0,finish]]
		for span in spans:
			var rect:=Rect2(span[0],top if side==0 else 181,span[1]-span[0],16)
			if vertical:rect=Rect2(184 if side==1 else -200,span[0],16,span[1]-span[0])
			draw_cap_strip(canvas,rect,vertical,side in [1,2])
	for edge in room.edges:
		var side:int=0 if edge.horizontal and edge.center.y<0 else 2 if edge.horizontal else 1 if edge.center.x>0 else 3
		if not ports.has(side) or (raised and side==0):continue
		var copy:Dictionary=edge.duplicate();copy.open=true
		for jamb in Geometry.jamb_rects(copy):
			var rect:Rect2=jamb;rect.position.y-=3
			draw_cap_strip(canvas,rect,not edge.horizontal,side in [1,2])
		# A closed outer station port still shows its registered leaf and fixed frame.
		if not edge.open:Doors.for_variant(room_id).low_closed(canvas,edge.center+Vector2(0,-3),not edge.horizontal,room_id)
	for x in [-200,184]:
		for y in [top,181]:
			if (1 if x>0 else 3) in present and (2 if y==181 else 0) in present:draw_cap_corner(canvas,Vector2(x,y),x>0,y==181)
func draw_cap_strip(target: CanvasItem, rect: Rect2, vertical := false, flip_depth := false) -> void:
	var cap: Array=registrations[room_id].cap
	var source:=Rect2(cap[0],cap[1],cap[2],cap[3])
	var length:=rect.size.y if vertical else rect.size.x
	var thickness:=rect.size.x if vertical else rect.size.y
	# Keep the source's pixel density and bevel thickness; crop length, never
	# stretch a tiny square tile into a long structural beam.
	var source_length:=minf(source.size.x,length*source.size.y/thickness)
	source.position.x+=(source.size.x-source_length)*0.5
	source.size.x=source_length
	if vertical or flip_depth:
		var points:=PackedVector2Array([rect.position,Vector2(rect.position.x,rect.end.y),rect.end,Vector2(rect.end.x,rect.position.y)])
		if not vertical: points=PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)])
		var near_y:=source.end.y if flip_depth else source.position.y
		var far_y:=source.position.y if flip_depth else source.end.y
		var uv:=PackedVector2Array([Vector2(source.position.x,near_y),Vector2(source.end.x,near_y),Vector2(source.end.x,far_y),Vector2(source.position.x,far_y)])
		for i in range(4): uv[i]/=Vector2(wall.get_size())
		target.draw_polygon(points,PackedColorArray([Color.WHITE]),uv,wall)
	else:
		target.draw_texture_rect_region(wall,rect,source)

func draw_cap_corner(target: CanvasItem, at: Vector2, east: bool, south: bool) -> void:
	var cap: Array=registrations[room_id].cap
	var depth: float=cap[3]
	# Quiet metal between structural fasteners, at exactly the straight cap scale.
	var source:=Rect2(cap[0]+cap[2]*0.2,cap[1],depth,depth)
	var local:=PackedVector2Array([Vector2(0,0),Vector2(16,0),Vector2(16,16),Vector2(0,16)])
	var points:=PackedVector2Array()
	for p in local:
		points.append(at+Vector2(16-p.x if east else p.x,16-p.y if south else p.y))
	var uv:=PackedVector2Array([source.position,Vector2(source.end.x,source.position.y),source.end,Vector2(source.position.x,source.end.y)])
	for i in range(4): uv[i]/=Vector2(wall.get_size())
	# The diagonal joins horizontal and vertical material planes; both bevels
	# meet at the inner vertex and the outside silhouette remains fully covered.
	target.draw_polygon(PackedVector2Array([points[0],points[1],points[2]]),PackedColorArray([Color.WHITE]),PackedVector2Array([uv[0],uv[1],uv[2]]),wall)
	target.draw_polygon(PackedVector2Array([points[0],points[2],points[3]]),PackedColorArray([Color.WHITE]),PackedVector2Array([uv[0],uv[2],uv[1]]),wall)

