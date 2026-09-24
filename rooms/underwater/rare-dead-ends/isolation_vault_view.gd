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

# Remove borrowed battery furniture only when rebuilding above. Repeated embedded
# setup must retain the full-wall wrapper's saved library props; filtering them
# here emptied the live room after its first pass while cards still looked correct.
