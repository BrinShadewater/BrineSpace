extends RefCounted
## Equipment-anchored floor service channels; no raised collision geometry.
static func host(props: Array, id: String) -> Rect2:
	for prop in props:
		if prop.id==id: return prop.rect
	return Rect2()

static func run(canvas: CanvasItem, points: PackedVector2Array, _color: Color, live: bool, art := "cable_straight") -> void:
	preload("res://rooms/whole-room/decoration_props.gd").service_run(canvas,points,6.0,art)
	# Solid flush bridge plate wherever a horizontal run crosses the central aisle.
	for i in range(points.size()-1):
		var a: Vector2=points[i]
		var b: Vector2=points[i+1]
		if absf(a.y-b.y)<0.1 and minf(a.x,b.x)<-22 and maxf(a.x,b.x)>22:
			var cover:=Rect2(Vector2(-22,a.y-6),Vector2(44,12))
			preload("res://rooms/whole-room/decoration_props.gd").fit(canvas,preload("res://assets/floor-utilities-style-v2/floor_sprites.gd").texture("mat_straight"),cover)
	for endpoint in [points[0],points[points.size()-1]]:
		canvas.draw_circle(endpoint,5,Color("273538"))
		canvas.draw_arc(endpoint,4,0,TAU,16,Color("8c9c94"),1)
	var junction: Vector2=points[1]
	canvas.draw_rect(Rect2(junction-Vector2(7,5),Vector2(14,10)),Color("364548"))
	canvas.draw_rect(Rect2(junction-Vector2(6,4),Vector2(12,8)),Color("74847f"),false,0.8)
	canvas.draw_circle(junction+Vector2(3,0),1.4,Color("90bb9e") if live else Color("414c49"))

static func render(canvas: CanvasItem, props: Array, kind: String, live: bool) -> void:
	if kind=="reactor":
		var cooler:=host(props,"reactor_cooler")
		var chamber:=host(props,"reactor_chamber")
		if cooler.size==Vector2.ZERO or chamber.size==Vector2.ZERO: return
		var start:=Vector2(cooler.get_center().x,cooler.end.y-2)
		var finish:=Vector2(chamber.position.x+2,chamber.get_center().y)
		for offset in [-5,5]:
			var a:=start+Vector2(offset,0)
			var b:=finish+Vector2(0,offset)
			run(canvas,PackedVector2Array([a,Vector2(a.x,b.y),b]),Color("7e8980") if offset<0 else Color("96734b"),live,"pipe_straight")
	elif kind=="hydro":
		var tank:=host(props,"hydro_nutrients")
		if tank.size==Vector2.ZERO:return
		for id in ["hydro_bed_west","hydro_bed_east"]:
			var bed:=host(props,id)
			var start:=Vector2(tank.get_center().x,tank.position.y+2)
			var finish:=Vector2(bed.get_center().x,bed.end.y-2)
			# Covers protect transverse portions; all runs remain floor-only.
			var bend:=Vector2(start.x,38)
			run(canvas,PackedVector2Array([start,bend,Vector2(finish.x,38),finish]),Color("688f86"),live,"pipe_straight")
	elif kind=="crew":
		for id in ["hab_berth_west","hab_berth_east","hab_desk"]:
			var furniture:=host(props,id)
			if furniture.size==Vector2.ZERO:continue
			var start:=Vector2(furniture.position.x+4,furniture.end.y-3)
			var socket:=start+Vector2(-10,7)
			run(canvas,PackedVector2Array([start,socket,socket+Vector2(15,0)]),Color("817361"),live)
			# Small maintenance/personal tag clipped beside each local socket.
			canvas.draw_rect(Rect2(socket+Vector2(-3,7),Vector2(6,8)),Color("b6a487"))
			canvas.draw_line(socket+Vector2(-1,10),socket+Vector2(2,10),Color("615b50"),0.7)

static func identity_details(canvas: CanvasItem, props: Array, kind: String, live: bool) -> void:
	if kind=="medical":
		for prop in props:
			if not str(prop.id).begins_with("med_bed_"):continue
			var bed: Rect2=prop.rect
			var foot:=Vector2(bed.get_center().x,bed.end.y+7)
			preload("res://rooms/whole-room/decoration_props.gd").floor_patch(canvas,"medical_bedside_mat",Rect2(foot-Vector2(23,5),Vector2(46,10)))
			var socket:=Vector2(bed.end.x-3,bed.end.y-3)
			run(canvas,PackedVector2Array([socket,socket+Vector2(8,0),socket+Vector2(8,-18)]),Color("91aaa5"),live)
			canvas.draw_line(foot+Vector2(-3,0),foot+Vector2(3,0),Color("d0ded3"),1.8)
	elif kind=="research":
		var specimens:=host(props,"research_specimens")
		var analyzer:=host(props,"research_analyzer")
		if specimens.size==Vector2.ZERO or analyzer.size==Vector2.ZERO:return
		var a:=Vector2(specimens.get_center().x,specimens.end.y-2)
		var b:=Vector2(analyzer.get_center().x,analyzer.end.y-2)
		var y:=maxf(a.y,b.y)+10
		run(canvas,PackedVector2Array([a,Vector2(a.x,y),Vector2(b.x,y),b]),Color("778da3"),live)
		for id in ["research_scanner","research_analyzer"]:
			var equipment:=host(props,id)
			var mat:=Rect2(equipment.position+Vector2(-4,8),equipment.size+Vector2(8,4))
			canvas.draw_rect(mat,Color("555467"))
			canvas.draw_rect(mat.grow(-2),Color("9899ad"),false,0.8)
			for x in range(6,int(mat.size.x)-6,8):
				canvas.draw_line(mat.position+Vector2(x,mat.size.y-5),mat.position+Vector2(x+3,mat.size.y-5),Color("b4b8c0"),0.7)
	elif kind=="command":
		var table:=host(props,"command_table")
		if table.size==Vector2.ZERO:return
		var mat:=Rect2(table.position-Vector2(8,0),table.size+Vector2(16,17))
		canvas.draw_rect(mat,Color("344b60"))
		canvas.draw_rect(mat.grow(-3),Color("8b9b99"),false,1.1)
		var mark:=Vector2(mat.get_center().x,mat.end.y-8)
		canvas.draw_line(mark-Vector2(12,0),mark+Vector2(12,0),Color("b5ae87"),1.2)
		canvas.draw_circle(mark,2,Color("b5ae87"))
		var systems:=host(props,"command_systems")
		var ops:=host(props,"command_ops")
		var a:=Vector2(systems.get_center().x,systems.end.y-2)
		var b:=Vector2(ops.get_center().x,ops.end.y-2)
		run(canvas,PackedVector2Array([a,Vector2(a.x,b.y),b]),Color("617f94"),live)
