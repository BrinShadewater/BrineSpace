extends RefCounted
## Department wall faces share geometry, not a universal painted panel.
static var registrations: Dictionary={}
static var textures: Dictionary={}
const GROUPS={
	"biology":["biomass_digester","mycelium_nursery","hydroponics_bay","biodome"],
	"clinical":["life_support","cryo_chamber","clone_lab","med_bay","med_center","med_office"],
	"habitat":["galley","observation_room","crew_hab","crew_lounge"],
	"engineering":["current_turbine","heat_recovery","construction_drone_bay","solar_array","reactor","battery_array","mining_drone_bay","tidal_condenser","ore_refinery","pressure_control","maintenance_bay","shield_generator"],
	"research":["gravity_loom","research_lab","anomaly_lab","bio_lab"],
	"communications":["data_archive","command_center","listening_post","holographic_core","radio_lab"],
	"logistics":["cold_store","salvage_workshop","salvage_drone_bay","storage_bay","corridor","corner","tee_corridor"],
	"containment":["quarantine_cell","xeno_lab","isolation_vault"]}

static func family(room_id: String) -> String:
	if room_id in ["brine_core","airlock"]: return room_id
	for group in GROUPS:
		if room_id in GROUPS[group]: return group
	return "logistics"

static func catalog() -> Dictionary:
	if registrations.is_empty():
		registrations=JSON.parse_string(FileAccess.get_file_as_string("res://assets/riser-departments-v1/registrations.json"))
		registrations.merge(JSON.parse_string(FileAccess.get_file_as_string("res://assets/room-risers-v2/registrations.json")))
		registrations.merge(JSON.parse_string(FileAccess.get_file_as_string("res://assets/room-risers-v3/registrations.json")))
	return registrations

static func material(room_id: String) -> String:
	return room_id if catalog().has(room_id) else family(room_id)

static func texture(group: String) -> Texture2D:
	if not textures.has(group):
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, catalog()[group].source)
		textures[group]=ImageTexture.create_from_image(image)
	return textures[group]

static func source_rect(group: String, part: String) -> Rect2:
	var r: Array=catalog()[group][part]
	return Rect2(r[0],r[1],r[2],r[3])

static func face(canvas: CanvasItem, room_id: String, target: Rect2, light:=1.0) -> void:
	var group:=material(room_id)
	var region:=source_rect(group,"face")
	# Preserve the source scale for short corridor sections rather than squashing a whole wall.
	var width:=region.size.y*target.size.x/target.size.y
	if width<region.size.x:
		region.position.x+=(region.size.x-width)*0.5;region.size.x=width
	canvas.draw_texture_rect_region(texture(group),target,region,Color(light,light,light))

static func cap(canvas: CanvasItem, room_id: String, target: Rect2) -> void:
	var group:=material(room_id)
	canvas.draw_texture_rect_region(texture(group),target,source_rect(group,"cap"))
