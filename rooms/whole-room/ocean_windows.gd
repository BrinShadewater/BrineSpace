extends RefCounted
## Registered pressure-window inserts. Source bounds exclude generated empty margins.
const SOURCES = {
	"square_steel": ["res://assets/ocean-windows-v3/sources/square-viewing-steel.png", Rect2(109,121,1036,1005)],
	"square_ivory": ["res://assets/ocean-windows-v3/sources/square-viewing-ivory.png", Rect2(98,105,1059,1031)],
	"square_sage": ["res://assets/ocean-windows-v3/sources/square-viewing-sage.png", Rect2(79,89,1096,1065)],
	"oval_brass": ["res://assets/ocean-windows-v3/sources/porthole-oval-brass.png", Rect2(111,104,1407,746)],
	"octagonal": ["res://assets/ocean-windows-v3/sources/bulkhead-octagonal-steel.png", Rect2(70,61,1114,1112)],
	"sage_viewing": ["res://assets/ocean-windows-v3/sources/viewing-sage-divided.png", Rect2(33,102,2107,506)],
	"blue_twin": ["res://assets/ocean-windows-v3/sources/bulkhead-blue-twin.png", Rect2(225,154,1324,570)],
	"porthole": ["res://assets/ocean-windows-v3/sources/porthole-steel.png", Rect2(115,96,1023,1029)],
	"blue": ["res://assets/ocean-windows-v3/sources/bulkhead-blue.png", Rect2(151,216,1073,703)],
	"sage": ["res://assets/ocean-windows-v3/sources/bulkhead-sage.png", Rect2(82,108,1091,995)],
	"viewing": ["res://assets/ocean-windows-v3/sources/viewing-warm.png", Rect2(31,142,1713,603)],
	"corridor": ["res://assets/ocean-windows-v3/sources/corridor-twin.png", Rect2(35,115,1914,537)],
	"corner": ["res://assets/ocean-windows-v3/sources/corner-graphite.png", Rect2(38,182,1559,593)],
	"tee_corridor": ["res://assets/ocean-windows-v3/sources/tee-viewing.png", Rect2(47,121,2081,458)],
}
static var textures: Dictionary = {}
static var calibrated := true
static var render_catalog: Dictionary = {}
const CENTER_MOUNT := Rect2(-28,-244,56,56)

static func render_record(kind: String) -> Dictionary:
	if render_catalog.is_empty():
		render_catalog=JSON.parse_string(FileAccess.get_file_as_string("res://assets/ocean-windows-v3/calibrated/catalog.json"))
	return render_catalog[kind]

static func source_region(kind: String) -> Rect2:
	if not calibrated: return SOURCES[kind][1]
	var r: Array=render_record(kind).region
	return Rect2(r[0],r[1],r[2],r[3])

static func texture(kind: String) -> Texture2D:
	var key := kind+str(calibrated)
	if not textures.has(key):
		var im := Image.new()
		var path: String=render_record(kind).path if calibrated else SOURCES[kind][0]
		if im.load_png_from_buffer(FileAccess.get_file_as_bytes(path)) != OK:
			return null
		textures[key] = ImageTexture.create_from_image(im)
	return textures[key]

static func fitted_rect(kind: String, mount: Rect2) -> Rect2:
	var source: Rect2 = SOURCES[kind][1]
	var factor := minf(mount.size.x/source.size.x, mount.size.y/source.size.y)
	var size := source.size*factor
	return Rect2(mount.get_center()-size*.5,size)

static func draw(canvas: CanvasItem, kind: String, mount: Rect2, light := 1.0) -> void:
	var tex := texture(kind)
	if tex == null: return
	if kind.begins_with("square_"):
		# Generated glazing is 98–99% opaque. A recessed dark backing prevents
		# wall plating showing through while leaving the exterior alpha intact.
		canvas.draw_rect(fitted_rect(kind,mount).grow(-5),Color("0a2f37"))
	canvas.draw_texture_rect_region(tex,fitted_rect(kind,mount),source_region(kind),Color(light,light,light))

static func room_kind(id: String) -> String:
	if id == "cold_store": return "blue"
	var definition: Dictionary = preload("res://scripts/room_database.gd").get_room(id)
	match definition.get("category",""):
		"Science": return "blue"
		"Life Support": return "sage"
		"Recreation": return "viewing"
		"Operations", "Anomaly": return "corner"
	return "porthole"

static func room_allowed(raised: bool, id: String, ports: Array, exterior_hatch := false) -> bool:
	return raised and id != "brine_core" and not ports.has(0) and not exterior_hatch

static func center_kind(id: String) -> String:
	var definition: Dictionary = preload("res://scripts/room_database.gd").get_room(id)
	match definition.get("category",""):
		"Life Support": return "square_sage"
		"Science", "Recreation": return "square_ivory"
	return "square_steel"

static func draw_room(canvas: CanvasItem, id: String, reserves: Array, include_center := true) -> void:
	# Complementary fittings keep room identity without repeating one silhouette.
	var additions := {"galley":"oval_brass", "salvage_workshop":"octagonal", "biomass_digester":"sage_viewing", "cold_store":"blue_twin"}
	for index in range(reserves.size()):
		var r: Array = reserves[index]
		var kind: String = additions[id] if index==1 and additions.has(id) else room_kind(id)
		# The original reserves sit near the upper edge of the inset side panels.
		# Lower their centers into the panel field, above the bottom service band.
		draw(canvas,kind,Rect2(r[0],r[1]+7,r[2],r[3]))
	# Caller gates the entire assembly on a sealed, exposed north face.
	# This square leaves breathing room inside the existing 92-by-79 panel.
	if include_center:draw(canvas,center_kind(id),CENTER_MOUNT)
