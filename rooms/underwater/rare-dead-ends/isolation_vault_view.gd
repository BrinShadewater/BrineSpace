extends "res://rooms/production-ten/battery_array_view.gd"

func _ready() -> void:
	super._ready()
	# This scene originally borrowed the Battery Array renderer, including all of
	# its furnishings. The vault keeps the shell but owns no battery equipment.
	life_items=[]
	dressing=Dressing.new(self,"res://rooms/underwater/rare-dead-ends/isolation-composition-v2.json")
	rebuild()

# What this drops is the inherited Battery Array equipment. A prop the layout put in
# the room is not that, and dropping those as well emptied the vault: the second
# configure_embedded threw away the wall bank the first one installed, and the bank is
# only reinstalled off a fresh rebuild, so the room stayed empty from then on.
static func keeps(prop: Dictionary) -> bool:
	return prop.registration.get("dressing",false) or prop.get("library_asset",false)

# place() ends in a room-wide keep_props_inside_walls(), which clamps to a flat 360
# interior and so drags a wall-mounted bank 16px off its wall. With no dressing left to
# position there is nothing to place, and running it anyway moved the bank on exactly
# the reconfigures that reused the bank instead of reinstalling it.
func place_dressing() -> void:
	if dressing==null: return
	for prop in props:
		if prop.registration.get("dressing",false):
			dressing.place()
			return

func rebuild() -> void:
	super.rebuild()
	layout=[{"cell":Vector2i.ZERO,"rotation":quarter,"kind":3}]
	edges=Geometry.edges(layout)
	for edge in edges:edge.open=edge.port
	props=props.filter(keeps)
	place_dressing()

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	props=props.filter(keeps)
	place_dressing()
