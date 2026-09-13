extends "res://rooms/production-ten/battery_array_view.gd"

func _ready() -> void:
	super._ready()
	# This scene originally borrowed the Battery Array renderer, including all of
	# its furnishings. The vault keeps the shell but owns no battery equipment.
	life_items=[]
	dressing=Dressing.new(self,"res://rooms/underwater/rare-dead-ends/isolation-composition-v2.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout=[{"cell":Vector2i.ZERO,"rotation":quarter,"kind":3}]
	edges=Geometry.edges(layout)
	for edge in edges:edge.open=edge.port
	props=props.filter(func(prop): return prop.registration.get("dressing",false))
	if dressing!=null: dressing.place()

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	props=props.filter(func(prop): return prop.registration.get("dressing",false))
	if dressing!=null: dressing.place()
