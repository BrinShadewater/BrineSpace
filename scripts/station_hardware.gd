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
	if not game.hardware.power: return
	var time: float=game.get_visual_time_seconds()
	for room in rooms:
		var center: Vector2=(Vector2(room.pos)+Vector2.ONE*0.5)*size
		if game.hardware.exterior:
			for direction in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
				if game.occupied.has(room.pos+direction): continue
				var housing_visible: bool=game.hardware.walls and (direction!=Vector2i.UP or preload("res://scripts/title_settings.gd").raised_walls)
				draw_exterior_light(canvas,center,Vector2(direction),size,housing_visible)

		if game.hardware.sprinklers and game.powered_room_cells.has(room.pos) and not str(room.id).begins_with("corridor"):
			for i in range(28):
				var phase:=fposmod(time*0.65+float(i)*0.137,1.0)
				var start:=center+Vector2(sin(i*2.7)*size*0.28,-size*0.25)
				var drop:=start+Vector2(sin(i*1.7)*size*0.08,phase*size*0.5)
				canvas.draw_line(drop,drop+Vector2(0,size*0.024),Color(0.55,0.70,0.72,(1-phase)*0.55),maxf(1,size*0.0015))

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
	preload("res://rooms/whole-room/radial_light.gd").draw(canvas,lamp,Color(.65,.84,.78,1),exterior_light_radius(size)/112.0,false)
	if not housing_visible: return
	var tangent:=Vector2(-direction.y,direction.x)
	var housing:=PackedVector2Array([lamp-tangent*size*0.026-direction*size*0.007,lamp+tangent*size*0.026-direction*size*0.007,lamp+tangent*size*0.026+direction*size*0.009,lamp-tangent*size*0.026+direction*size*0.009])
	canvas.draw_colored_polygon(housing,Color("233c40"))
	canvas.draw_line(lamp-tangent*size*0.018,lamp+tangent*size*0.018,Color("d8f4d9"),maxf(1.0,size*0.006))
