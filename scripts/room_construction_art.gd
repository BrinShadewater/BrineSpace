extends RefCounted
## Shared, work-driven assembly. Actual destination art supplies the finished shell and fit-out.
static func draw(grid, order: Dictionary, progress: float) -> void:
	var painter: CanvasItem=grid.draw_target
	var size: float=grid._cell_size()
	var scale: float=size/384.0
	var center: Vector2=(Vector2(order.pos)+Vector2.ONE*.5)*size
	var room: Dictionary=grid.RoomDatabaseScript.get_room(order.id).duplicate(true)
	room.pos=order.pos
	room.rotation=order.rotation
	var narrow: bool=grid._is_narrow_corridor(room)
	var bounds:=Rect2(-178,-178,356,356)
	if narrow and order.id=="corridor":
		bounds=Rect2(-52,-184,104,368) if order.rotation%2==0 else Rect2(-184,-52,368,104)
	var p:=clampf(progress,0,1)
	painter.draw_set_transform(center,0,Vector2.ONE*scale)
	painter.draw_rect(Rect2(bounds.position+Vector2(5,9),bounds.size),Color(0,0,0,.3))
	painter.draw_rect(bounds,Color("202b2e"),false,3)
	# Bolted foundation crossmembers extend into the reserved footprint.
	for i in range(7):
		var f:=clampf(p/.28*7-i,0,1)
		if f<=0: continue
		var x: float=bounds.position.x+bounds.size.x*i/6.0
		var a:=Vector2(x,bounds.position.y)
		var b:=Vector2(x,bounds.position.y+bounds.size.y*f)
		painter.draw_line(a+Vector2(0,4),b+Vector2(0,4),Color("151d20"),9)
		painter.draw_line(a,b,Color("53605d"),5)
		for j in range(5):
			var y: float=bounds.position.y+bounds.size.y*j/4.0
			if y<=b.y: painter.draw_rect(Rect2(x-3,y-3,6,6),Color("787567"))
	# Deck plates seat one strip at a time, leaving the underlying supports visible.
	for i in range(8):
		var f:=clampf((p-.22)/.3*8-i,0,1)
		if f<=0: continue
		var plate:=Rect2(bounds.position+Vector2(bounds.size.x*i/8.0,0),Vector2(bounds.size.x/8.0-2,bounds.size.y*f))
		painter.draw_rect(plate,Color("394544"))
		painter.draw_line(plate.position,Vector2(plate.position.x,plate.end.y),Color("58635e"),1)
	# Low pressure-frame segments rise around the deck; no tall scaffold obscures crew.
	var corners: Array=[bounds.position,Vector2(bounds.end.x,bounds.position.y),bounds.end,Vector2(bounds.position.x,bounds.end.y)]
	for i in range(4):
		var f:=clampf((p-.35)/.3*4-i,0,1)
		if f>0:
			var a: Vector2=corners[i]-Vector2(0,10)
			var b: Vector2=corners[(i+1)%4]-Vector2(0,10)
			painter.draw_line(a,a.lerp(b,f),Color("69736b"),6)
	painter.draw_set_transform(Vector2.ZERO)
	if p>=.62:
		if narrow:
			grid._draw_narrow_corridor(room,Rect2(center-Vector2.ONE*size*.5,Vector2.ONE*size),true,p<.85,false)
		else:
			var view=grid._bill_room_view(room)
			if view!=null:
				view.configure_embedded(int(order.rotation),[],false,0.0)
				var props: Array=view.props
				var count: int=clampi(int(ceil((p-.70)/.30*props.size())),0,props.size())
				view.props=props.slice(0,count)
				view.set_meta("layout_editor_preview",true)
				view.render_into(painter,center,scale,false,true)
				view.remove_meta("layout_editor_preview")
				view.props=props
	painter.draw_set_transform(center,0,Vector2.ONE*scale)
	var label: String="FOUNDATION" if p<.22 else "DECK ASSEMBLY" if p<.35 else "PRESSURE FRAME" if p<.62 else "HULL SEALED" if p<.7 else "FITTING INTERIOR"
	painter.draw_rect(Rect2(-92,156,184,21),Color(.04,.08,.09,.94))
	painter.draw_string(grid.get_theme_default_font(),Vector2(-86,170),label+"  "+str(roundi(p*100))+"%",HORIZONTAL_ALIGNMENT_CENTER,172,11,Color("c3b798"))
	painter.draw_rect(Rect2(-92,179,184*p,3),Color("ad9867"))
	painter.draw_set_transform(Vector2.ZERO)
