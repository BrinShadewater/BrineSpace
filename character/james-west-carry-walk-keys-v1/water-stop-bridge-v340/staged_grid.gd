extends "res://scripts/grid_canvas.gd"
## Fixture-only renderer clearance hook; normal grid selection is unchanged.
var fixture_visual_time:=10.0
func _water_transition_clear(actor)->bool:
	if _is_james_actor(actor) and actor.movement_medium=="flooded" and branforth_player.has_method("preview_water_transition"):
		var gear:String="diving-helmet" if actor.helmet_equipped else ""
		var clock:float=fixture_visual_time if fixture_visual_time>=0 else _get_main().get_visual_time_seconds()
		var key:String=branforth_player.preview_water_transition(actor.animation_state(),actor.direction,clock,gear)
		if key.begins_with("swim-stop-") or key.begins_with("swim-restart-phase-") or key.begins_with("swim-reorient-"):
			var extent:Array=branforth_player.clip_extent(key,gear)
			var previous:String=branforth_player.motion.get("direction",actor.direction)
			return not extent.is_empty() and actor.swim_segment_clear(actor.foot,actor.foot,actor.direction,previous,false,extent)
	return super._water_transition_clear(actor)
