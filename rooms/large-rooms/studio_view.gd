extends Node2D
## The large rooms keep their painted shell and fixed equipment. Studio layouts add props.
const Library = preload("res://scripts/room_asset_library.gd")
const Store = preload("res://scripts/room_layout_store.gd")
const Database = preload("res://scripts/room_database.gd")
const VIEWS = {
	"hydroponics_farm": preload("res://rooms/large-rooms/hydroponics_farm.gd"),
	"storage_depot": preload("res://rooms/large-rooms/storage_depot.gd"),
	"moonbay": preload("res://rooms/large-rooms/moonbay.gd"),
	"tidal_power_plant": preload("res://rooms/large-rooms/tidal_power_plant.gd")
}
static var live_cache: Dictionary = {}
static var cache_revision := -1
class PaintContext extends RefCounted:
	var props: Array = []
	var painter: CanvasItem
	var operating := true
	var machine_clock := 0.0
	var drone_visual = null
	func prop_visual_bounds(prop: Dictionary) -> Rect2:
		return Library.bounds(prop)
var room_id := "hydroponics_farm"
var quarter := 0
var props: Array = []
var embedded := false
var operating := true
var machine_clock := 0.0
var drone_visual = null
# Studio previews of the room's machinery (scripts/studio_effect_preview.gd); empty leaves the room's own state.
var tidal_chamber: Dictionary = {}
var moonbay_mission: Dictionary = {}
var painter: CanvasItem

func configure_embedded(q: int, _open_sides: Array, _running: bool, _time_seconds: float) -> void:
	quarter = posmod(q, 4)
	props.clear()

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	return Library.bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	Library.draw(self, prop)

func render_into(target: CanvasItem, at: Vector2, scale_value: float, floor_only := false, _include_floor := true) -> void:
	painter = target
	if floor_only:
		var appearance: Dictionary = Database.get_room(room_id).duplicate(true)
		appearance.rotation = quarter
		appearance.raised_walls = true
		if room_id == "tidal_power_plant":
			appearance.tidal_chamber = tidal_chamber if not tidal_chamber.is_empty() else {"water":minf(1.0,machine_clock/6.0),"spinning":machine_clock>=6.0,"rotor_angle":fposmod(maxf(0.0,machine_clock-6.0)*0.8,TAU)}
		if room_id == "moonbay" and not moonbay_mission.is_empty():
			appearance.moonbay_mission = moonbay_mission
		VIEWS[room_id].draw(target, appearance, Rect2(at - Vector2.ONE * 384.0 * scale_value, Vector2.ONE * 768.0 * scale_value))
		return
	draw_props(target, self, at, scale_value)

static func draw_props(target: CanvasItem, view, at: Vector2, scale_value: float) -> void:
	view.painter = target
	for prop in view.props:
		if prop.get("layout_hidden", false): continue
		Store.draw_flip(view, target, prop, at, scale_value)
		Library.draw(view, prop)
	target.draw_set_transform(Vector2.ZERO)

static func live_props(id: String, q: int) -> Array:
	Store.prime()
	if cache_revision != Store.revision:
		live_cache.clear()
		cache_revision = Store.revision
	var key := id + "/" + str(posmod(q, 4))
	if live_cache.has(key): return live_cache[key]
	var view = new()
	view.room_id = id
	view.quarter = posmod(q, 4)
	var selected: Dictionary = Store.shared_positions("room-" + id, q)
	view.set_meta("layout_asset", "room-" + id)
	Library.apply(view, selected)
	Store.copies(view, selected)
	Library.apply_variants(view, selected)
	view.props = view.props.filter(func(prop): return not (selected.has(str(prop.id)) and selected[str(prop.id)] == null) and not Store.is_common_decoration(prop))
	for prop in view.props:
		prop.layout_flip = Store.flip_axes(view, str(prop.id))
		prop.layout_hidden = selected.get("hidden/" + str(prop.id), false)
		Store.resize_prop(prop, selected.get("size/" + str(prop.id), [1.0, 1.0]))
		Store.move_prop(prop, Vector2(selected[str(prop.id)][0], selected[str(prop.id)][1]))
		prop.sort_y += float(selected.get("order/" + str(prop.id), 0)) * 512.0
	var result: Array = view.props
	live_cache[key] = result
	view.free()
	return result

static func draw_live(target: CanvasItem, room: Dictionary, rect: Rect2, clock := 0.0, operating := true) -> void:
	var context := PaintContext.new()
	context.props = live_props(str(room.id), int(room.get("rotation", 0)))
	context.machine_clock = clock
	context.operating = operating
	draw_props(target, context, rect.get_center(), rect.size.x / 768.0)
