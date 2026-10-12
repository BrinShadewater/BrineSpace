extends Node2D
## Large-room shells and central machinery, with editable supporting equipment.
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
# The supporting equipment of these rooms starts as ordinary props: movable, resizable, hideable and deletable
# like any Studio prop. Moonbay locker interaction follows its saved prop position.
const MOVABLE_FEATURE_ROOMS := ["tidal_power_plant", "hydroponics_farm", "storage_depot", "moonbay"]
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
var external_actors: Array = []
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
		appearance.studio_props = props
		if room_id == "tidal_power_plant":
			appearance.tidal_chamber = tidal_chamber if not tidal_chamber.is_empty() else {"water":minf(1.0,machine_clock/6.0),"spinning":machine_clock>=6.0,"rotor_angle":fposmod(maxf(0.0,machine_clock-6.0)*0.8,TAU)}
		if room_id == "moonbay" and not moonbay_mission.is_empty():
			appearance.moonbay_mission = moonbay_mission
		VIEWS[room_id].draw(target, appearance, Rect2(at - Vector2.ONE * 384.0 * scale_value, Vector2.ONE * 768.0 * scale_value))
		return
	# Match the ordinary room's actor scale and depth order.
	var queue: Array=[]
	for prop in props:
		if not prop.get("layout_hidden",false): queue.append({"prop":prop,"depth":prop.sort_y})
	for member in external_actors: queue.append({"actor":member,"depth":member.position.y+float(member.texture.get_meta("crew_depth_offset",0.0))})
	queue.sort_custom(func(a,b):return a.depth<b.depth)
	for item in queue:
		if item.has("prop"):
			Store.draw_flip(self,target,item.prop,at,scale_value)
			Library.draw(self,item.prop)
		else:
			target.draw_set_transform(at,0,Vector2.ONE*scale_value)
			var member: Dictionary=item.actor
			var texture: Texture2D=member.texture
			var pixel_scale:=65.28/float(texture.get_meta("crew_standing_height",74.0))
			var pivot: Vector2=texture.get_meta("crew_pivot",Vector2(46,86))
			preload("res://scripts/flood_visuals.gd").draw_crew_shadow(target,member.position,0.0)
			target.draw_texture_rect(texture,Rect2(member.position-pivot*pixel_scale,texture.get_size()*pixel_scale),false)
	target.draw_set_transform(Vector2.ZERO)

static func draw_props(target: CanvasItem, view, at: Vector2, scale_value: float) -> void:
	view.painter = target
	for prop in view.props:
		if prop.get("layout_hidden", false): continue
		Store.draw_flip(view, target, prop, at, scale_value)
		Library.draw(view, prop)
	target.draw_set_transform(Vector2.ZERO)

# The layout entries those pieces have before the owner touches them, for this rotation. They sit under
# the saved layout, so an old layout shows each piece where it used to be until it is moved, hidden or deleted.
static func feature_seed(id: String, q: int) -> Dictionary:
	var result := {}
	if not MOVABLE_FEATURE_ROOMS.has(id): return result
	var features: Array=VIEWS[id].features_for_rotation(q) if id=="moonbay" else VIEWS[id].FEATURES
	for feature in features:
		var prop_id := "library/" + str(feature.path).get_file().get_basename()
		var template: Dictionary = Library.template(prop_id)
		if template.is_empty(): continue
		var source: Rect2 = feature.rect
		var center := source.get_center() if feature.get("fixed_position", false) else source.get_center().rotated(float(posmod(q, 4)) * PI * 0.5)
		var fit := source.size.x / maxf(1.0, template.rect.size.x)
		var size: Vector2 = template.rect.size * fit
		result[prop_id] = [center.x - size.x * 0.5, center.y - size.y * 0.5]
		result["size/" + prop_id] = [fit, fit]
	return result

static func live_props(id: String, q: int) -> Array:
	# Shared read-only runtime data. Apply edits through Store, which invalidates
	# this list; render callers must not mutate its entries in place.
	Store.prime()
	if cache_revision != Store.revision:
		live_cache.clear()
		cache_revision = Store.revision
	var key := id + "/" + str(posmod(q, 4))
	if live_cache.has(key): return live_cache[key]
	var view = new()
	view.room_id = id
	view.quarter = posmod(q, 4)
	var selected: Dictionary = feature_seed(id, q)
	selected.merge(Store.shared_positions("room-" + id, q), true)
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

static func draw_live(target: CanvasItem, room: Dictionary, rect: Rect2, clock := 0.0, operating := true, offline := false) -> void:
	var context := PaintContext.new()
	context.props = live_props(str(room.id), int(room.get("rotation", 0)))
	context.machine_clock = clock
	context.operating = operating
	var wet: Dictionary=target.get_meta("large_wet_equipment",{})
	var key: Variant=room.get("pos",str(room.id))
	var water: float=preload("res://scripts/room_flooding.gd").level(room)
	if water>0.001:
		if not wet.has(key):
			wet[key]=preload("res://scripts/large_wet_equipment.gd").new()
			target.add_child(wet[key]);target.set_meta("large_wet_equipment",wet)
		wet[key].configure(context,rect.get_center(),rect.size.x/768.0,water,clock,offline)
	else:
		if wet.has(key):wet[key].hide()
		draw_props(target, context, rect.get_center(), rect.size.x / 768.0)

static func hide_wet_equipment(target: CanvasItem,occupied: Dictionary) -> void:
	var wet: Dictionary=target.get_meta("large_wet_equipment",{})
	for key in wet.keys():
		wet[key].hide()
		if key is Vector2i and (not occupied.has(key) or not VIEWS.has(str(occupied[key].id))):
			wet[key].queue_free();wet.erase(key)
