extends RefCounted
const Materials=preload("res://scripts/construction_materials.gd")
## Shared, work-driven assembly. Actual destination art supplies the finished shell and fit-out.
static func draw(grid, order: Dictionary, progress: float, show_label:=true) -> void:
	var painter: CanvasItem=grid.draw_target
	var size: float=grid._cell_size()
	var scale: float=size/384.0
	var room: Dictionary=grid.RoomDatabaseScript.get_room(order.id).duplicate(true)
	var footprint: Vector2=Vector2(room.get("size",Vector2i.ONE))
	var center: Vector2=(Vector2(order.pos)+footprint*.5)*size
	room.pos=order.pos
	room.rotation=order.rotation
	room.art_variant=order.get("art_variant",0)
	var narrow: bool=grid._is_narrow_corridor(room)
	var mask:=Materials.hull(room)
	var bounds:=Rect2(mask[0],Vector2.ZERO)
	for point in mask:bounds=bounds.expand(point)
	var p:=clampf(progress,0,1)
	painter.draw_set_transform(center,0,Vector2.ONE*scale)
	var shadow:=PackedVector2Array()
	for point in mask:shadow.append(point+Vector2(5,9))
	painter.draw_colored_polygon(shadow,Color(0,0,0,.3))
	var outline:=mask.duplicate();outline.append(mask[0])
	painter.draw_polyline(outline,Color("202b2e"),3)
	# Bolted foundation crossmembers extend into the reserved footprint.
	var joists:=int(6*footprint.x+1)
	for i in range(joists):
		var f:=clampf(p/.28*joists-i,0,1)
		if f<=0: continue
		var x: float=bounds.position.x+bounds.size.x*i/float(joists-1)
		var a:=Vector2(x,bounds.position.y)
		var b:=Vector2(x,bounds.position.y+bounds.size.y*f)
		Materials.rail(painter,"foundation-joist",a,b,9.0,mask)
	# Deck plates seat one strip at a time, leaving the underlying supports visible.
	var plates:=int(8*footprint.x)
	for i in range(plates):
		var f:=clampf((p-.22)/.3*plates-i,0,1)
		if f<=0: continue
		for row in range(ceili(bounds.size.y/384.0)):
			var height:=clampf(bounds.size.y*f-row*384.0,0,384.0)
			if height<=0:continue
			var plate:=Rect2(bounds.position+Vector2(bounds.size.x*i/float(plates),row*384.0),Vector2(bounds.size.x/float(plates)-2,height))
			Materials.patch(painter,"deck-plate",plate,mask,384.0)
	# Low pressure-frame segments rise around the deck; no tall scaffold obscures crew.
	for i in range(mask.size()):
		var f:=clampf((p-.35)/.3*mask.size()-i,0,1)
		if f>0:
			var a: Vector2=mask[i]
			var b: Vector2=mask[(i+1)%mask.size()]
			Materials.rail(painter,"pressure-rail",a,a.lerp(b,f),8.0,mask)
	painter.draw_set_transform(Vector2.ZERO)
	if p>=.62:
		if footprint!=Vector2.ONE:
			if p>=.85:
				# A queued/scrapped room has no live airlock or operation state yet.
				var rect:=Rect2(Vector2(room.pos)*size+Vector2.ONE,footprint*size-Vector2.ONE*2)
				room.raised_walls=true
				grid.LARGE_ROOM_VIEWS[room.id].draw(painter,room,rect)
				grid.LargeStudioView.draw_live(painter,room,rect,0.0,false)
		elif narrow:
			# Commission the actual destination deck before its shell and fittings.
			if p<.85:
				painter.draw_set_transform(center,0,Vector2.ONE*scale)
				const Corridor=preload("res://rooms/underwater/corridor_geometry.gd")
				const Floors=preload("res://rooms/whole-room/modular_floor.gd")
				Floors.draw(painter,{},true,Corridor.rotation(room),1.0,Vector2.ZERO,.65,"",room.id,int(room.get("art_variant",0)))
				painter.draw_set_transform(Vector2.ZERO)
			else:
				grid._draw_narrow_corridor(room,Rect2(center-Vector2.ONE*size*.5,Vector2.ONE*size),true,false,false)
		else:
			var view=grid._bill_room_view(room)
			if view!=null:
				view.configure_embedded(int(order.rotation),[],false,0.0)
				preload("res://scripts/room_asset_library.gd").strip_retired(view)
				var props: Array=view.props
				var count: int=clampi(int(ceil((p-.70)/.30*props.size())),0,props.size())
				view.props=props.slice(0,count)
				view.set_meta("layout_editor_preview",true)
				view.set_meta("construction_fitting",true)
				view.render_into(painter,center,scale,false,true)
				view.remove_meta("layout_editor_preview")
				view.remove_meta("construction_fitting")
				view.props=props
	if show_label:
		painter.draw_set_transform(center,0,Vector2.ONE*scale)
		var label: String="FOUNDATION" if p<.22 else "DECK ASSEMBLY" if p<.35 else "PRESSURE FRAME" if p<.62 else "HULL SEALED" if p<.7 else "FITTING INTERIOR"
		painter.draw_rect(Rect2(-92,156,184,21),Color(.04,.08,.09,.94))
		painter.draw_string(grid.get_theme_default_font(),Vector2(-86,170),label+"  "+str(roundi(p*100))+"%",HORIZONTAL_ALIGNMENT_CENTER,172,11,Color("c3b798"))
		painter.draw_rect(Rect2(-92,179,184*p,3),Color("ad9867"))
	painter.draw_set_transform(Vector2.ZERO)
