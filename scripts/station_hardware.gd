extends RefCounted
const DEFAULTS={"power":true,"walls":true,"interior":true,"exterior":true,"sprinklers":false,"doors":false,"pumps":true}
static func valid(value) -> bool:
	if not value is Dictionary: return false
	for key in value:
		if not DEFAULTS.has(key) or not value[key] is bool: return false
	return true
static func restored(value) -> Dictionary:
	var result:=DEFAULTS.duplicate()
	if valid(value): result.merge(value,true)
	return result
static func set_control(game, key: String, enabled: bool) -> bool:
	if not DEFAULTS.has(key) or game._gameplay_input_blocked(): return false
	if key=="doors" and enabled:
		for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:
			if not actor.active: continue
			var local: Vector2=actor.foot-Vector2(actor.cell_at(actor.foot))*384.0
			if minf(minf(local.x,384-local.x),minf(local.y,384-local.y))<26:
				game._log("Door lock held: wait for crew to clear the threshold.",false); return false
	game.hardware[key]=enabled
	if key in ["power","pumps"]:
		var forecast: Dictionary=game._simulate_room_economy(true,game.cycle+1)
		game.powered_room_cells=forecast.working_cells.duplicate()
		game.offline_reasons=forecast.offline.duplicate()
		game.unpowered_room_cells=forecast.offline.duplicate()
		game.active_synergy_links=game.DiscoveryManagerScript.functioning_links(game.connected_synergy_links,game.powered_room_cells)
	if key=="doors":
		for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:
			actor.hardware_doors_locked=enabled
			actor.signature=""; actor.path.clear()
	game.grid_view.surface_key=[]; game.grid_view.door_surface_key=[]; game.grid_view.light_surface_key=[]
	game.grid_view.queue_redraw()
	game.play_station_sound("ui_select")
	game._refresh_all()
	return true
static func draw_effects(canvas, game, rooms: Array, size: float) -> void:
	var time: float=game.get_visual_time_seconds()
	for room in rooms:
		var center: Vector2=(Vector2(room.pos)+Vector2.ONE*0.5)*size
		if game.hardware.power and game.hardware.exterior and not room.get("suspended",false) and (game.powered_room_cells.has(room.pos) or room.id=="brine_core"):
			for direction in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
				if game.occupied.has(room.pos+direction): continue
				var housing_visible: bool=game.hardware.walls and (direction!=Vector2i.UP or preload("res://scripts/title_settings.gd").raised_walls)
				draw_exterior_light(canvas,center,Vector2(direction),size,housing_visible)

		var fire=preload("res://scripts/room_fire.gd")
		if not fire.burning(room): continue
		var status: String=fire.sprinkler_status(game,room)
		var unit := size/384.0
		var pixel := maxf(1,unit*2)
		for side in [-1,1]:
			var nozzle := center+Vector2(side*88,-92)*unit
			canvas.draw_rect(Rect2(nozzle-Vector2(5,3)*unit,Vector2(10,6)*unit),Color("637c7b"))
			canvas.draw_rect(Rect2(nozzle-Vector2(2,0)*unit,Vector2(4,4)*unit),Color("b6d4d1") if status=="SPRAYING" else Color("394f53"))
			if status!="SPRAYING": continue
			for i in range(22):
				var phase := fposmod(time*1.2+i*.173+side*.21,1.0)
				var spread := float(i%11-5)/5.0
				var drop := nozzle+Vector2(spread*72*phase,phase*165)*unit
				drop=(drop/pixel).floor()*pixel
				canvas.draw_rect(Rect2(drop,Vector2(pixel,pixel*2)),Color(.63,.84,.88,.7*(1-phase*.55)))
		var color := Color("9acbd4") if status=="SPRAYING" else Color("d3a479")
		var font: Font=ThemeDB.fallback_font
		var label := "SPRINKLERS / "+status
		var font_size := maxi(9,roundi(12*unit))
		var width := font.get_string_size(label,HORIZONTAL_ALIGNMENT_LEFT,-1,font_size).x
		var position := center+Vector2(-width*.5,125*unit)
		canvas.draw_rect(Rect2(position-Vector2(5,font_size),Vector2(width+10,font_size+5)),Color(.025,.06,.07,.88))
		canvas.draw_string(font,position,label,HORIZONTAL_ALIGNMENT_LEFT,-1,font_size,color)

static func exterior_mount(center: Vector2, direction: Vector2, size: float) -> Vector2:
	# Mount to the solid rim, not the empty space below the foundation supports.
	var reach:=202.0
	if direction.y<0: reach=-preload("res://rooms/whole-room/riser_geometry.gd").CAP_TOP+8.0
	elif direction.y>0: reach=198.0
	return center+direction*size*reach/384.0

static func exterior_light_radius(size: float) -> float:
	return size*.38

static func draw_exterior_light(canvas: CanvasItem, center: Vector2, direction: Vector2, size: float, housing_visible := true) -> void:
	var lamp:=exterior_mount(center,direction,size)
	# The underwater visibility pass owns illumination and terrain occlusion.
	# This foreground pass draws only the physical fixture.
	if not housing_visible: return
	var tangent:=Vector2(-direction.y,direction.x)
	var housing:=PackedVector2Array([lamp-tangent*size*0.026-direction*size*0.007,lamp+tangent*size*0.026-direction*size*0.007,lamp+tangent*size*0.026+direction*size*0.009,lamp-tangent*size*0.026+direction*size*0.009])
	canvas.draw_colored_polygon(housing,Color("233c40"))
	canvas.draw_line(lamp-tangent*size*0.018,lamp+tangent*size*0.018,Color("d8f4d9"),maxf(1.0,size*0.006))
