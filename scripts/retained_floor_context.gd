extends "res://scripts/retained_wall_context.gd"
## Floors share the wall projection's local structural dependencies, including interior light.
func prepare(common:Array,occupied:Dictionary,powered:Dictionary,rooms:Array)->void:
	var floor_common:Array=common.duplicate()
	floor_common.append([common[0].has("interior"),common[0].get("interior")])
	super.prepare(floor_common,occupied,powered,rooms)
