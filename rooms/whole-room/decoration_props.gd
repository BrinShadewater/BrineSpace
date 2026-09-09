extends RefCounted
## Reviewed reusable art fitted to existing physical mounts. No new obstacles.
const Floor = preload("res://assets/floor-dressing-style-v2/floor_dressing.gd")
const Utilities = preload("res://assets/floor-utilities-style-v2/floor_sprites.gd")
const Wall = preload("res://assets/wall-dressing-style-v2/wall_sprites.gd")
const Hull = preload("res://assets/riser-wall-kit-style-v2/wall_sprites.gd")

static func fit(canvas: CanvasItem, texture: Texture2D, bounds: Rect2, tint := Color.WHITE) -> Rect2:
	var dimensions := Vector2(texture.get_size())
	dimensions *= minf(bounds.size.x/dimensions.x,bounds.size.y/dimensions.y)
	var destination := Rect2(bounds.get_center()-dimensions*.5,dimensions)
	canvas.draw_texture_rect(texture,destination,false,tint)
	return destination

static func floor_patch(canvas: CanvasItem, id: String, bounds: Rect2) -> void:
	fit(canvas,Floor.texture(id),bounds)

static func service_run(canvas: CanvasItem, points: PackedVector2Array, width := 6.0, id := "cable_straight") -> void:
	# Tile floor-only cable art along authored routes; keep endpoints and clearance.
	var texture := Utilities.texture(id)
	var tile_length := width*float(texture.get_width())/float(texture.get_height())
	for index in range(points.size()-1):
		var delta := points[index+1]-points[index]
		if delta.length()<.1: continue
		var tangent := delta.normalized()
		var normal := Vector2(-tangent.y,tangent.x)*width*.5
		var cursor := 0.0
		while cursor<delta.length():
			var length := minf(tile_length,delta.length()-cursor)
			var a := points[index]+tangent*cursor
			var b := a+tangent*length
			canvas.draw_polygon(PackedVector2Array([a-normal,b-normal,b+normal,a+normal]),PackedColorArray([Color.WHITE]),PackedVector2Array([Vector2.ZERO,Vector2(length/tile_length,0),Vector2(length/tile_length,1),Vector2.DOWN]),texture)
			cursor+=length

static func mat_art(host: String) -> String:
	if host.begins_with("hab_") or host.begins_with("lounge_"): return "woven_bedside_rug"
	if host in ["hydro_nutrients","biodome_cultivation_cart"]: return "plant_drip_tray"
	if host in ["hydro_harvest","nursery_supply_trolley","tidal_sampling_bench"]: return "irrigation_drain_tiles"
	if host in ["med_preparation","medical_care_trolley","cryo_supply_trolley","clone_preparation"]: return "medical_bedside_mat"
	if host=="office_consultation": return "briefing_zone_mat"
	if host in ["storage_packing_bench","construction_parts_trolley","mining_component_table","salvage_intake_bench"]: return "pallet_alignment_plate"
	return "tread_service_mat"

static func wall_art(path: String) -> Array:
	var name := path.get_file().trim_suffix("_view.gd")
	match name:
		"crew_hab": return ["picture_ocean","wall_calendar"]
		"crew_lounge": return ["picture_botanical","analog_clock"]
		"command_center": return ["station_map","digital_clock"]
		"med_bay","med_center","med_office": return ["com_panel","wall_calendar"]
		"cryo_chamber","clone_lab": return ["pressure_gauge","com_panel"]
		"brine_core","holographic_core","data_archive": return ["com_panel","digital_clock"]
		"hydroponics","biodome","nursery_furnished": return ["picture_botanical","pressure_gauge"]
		"underwater_life_support","pressure_control","tidal_condenser": return ["pressure_gauge","oxygen_masks"]
		"radio_lab","listening_post": return ["com_handset","digital_clock"]
		"airlock": return ["pressure_gauge","oxygen_masks"]
		"research_lab","bio_lab","xeno_lab","anomaly_lab": return ["sample_display","com_panel"]
		"storage_bay","salvage_drone_bay": return ["notice_board","com_handset"]
		"maintenance_bay","construction_drone_bay","mining_drone_bay": return ["tool_rack","pressure_gauge"]
		"quarantine_cell","isolation_vault": return ["com_panel","alarm_beacon"]
		_: return ["pressure_gauge","small_access_cover"]

static func wall(_room, _bounds: Rect2, _horizontal: bool) -> void:
	# Decorations belong to the raised face drawn by north_wall.gd.
	# Keep the low pressure-hull strip bare in every room and orientation.
	pass
