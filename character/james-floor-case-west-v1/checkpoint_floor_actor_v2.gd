extends "res://character/james-cargo-return-bridges-v1/return_actor.gd"
const FLOOR=preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd")
func advance_work_return(main,delta:float)->bool:
	var was_empty:bool=preview_player==null or preview_player.return_plan.is_empty()
	var service_cell:Vector2i=goal_cell
	var contact:Vector2=foot
	# Shared update dispatches needs/fire/flood before this hook. Cue crossing is
	# observed even when a large delta skips its visible hold, before finite cleanup.
	if not was_empty:FLOOR.observe_plan(main,self,preview_player,main.get_visual_time_seconds())
	var result:bool=super.advance_work_return(main,delta)
	if was_empty and preview_player!=null and not preview_player.return_plan.is_empty():
		preview_player.return_plan.floorCell=service_cell
		preview_player.return_plan.floorFoot=contact
	return result
