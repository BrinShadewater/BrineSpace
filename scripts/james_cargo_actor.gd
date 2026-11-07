extends "res://character/james-floor-case-west-v1/checkpoint_floor_actor_v2.gd"
func workshop_pickup_active()->bool:
	return active and not dead and movement_medium=="dry" and stage=="workshop_pickup" and path.is_empty()
func animation_state()->String:
	if workshop_pickup_active():return "pickup"
	return super.animation_state()
func action_elapsed()->float:
	if workshop_pickup_active():return clampf(.52-timer,0.0,.52)
	return super.action_elapsed()
func update(main,delta:float)->void:
	preview_player=main.grid_view.branforth_player if main.grid_view.branforth_player.has_method("return_texture") else null
	var ordinary_cell:Vector2i=goal_cell
	var ordinary_foot:Vector2=foot
	var elapsed_before:float=action_elapsed()
	var ordinary_release:=false
	if active and not dead and movement_medium=="dry" and stage=="workshop_unload" and direction=="west" and goal=="curiosity" and service_available(main,ordinary_cell) and preview_player!=null:
		var gear:String="diving-helmet" if helmet_equipped else ""
		if FLOOR.cue_available(preview_player,gear):
			var clocks:Dictionary=preview_player.timing if gear.is_empty() else preview_player.equipment_timing[gear]
			var release_elapsed:=0.0
			for index in range(FLOOR.RELEASE_INDEX):release_elapsed+=float(clocks["unload-west"].durations[index])/1000.0
			ordinary_release=elapsed_before+delta>=release_elapsed
	super.update(main,delta)
	# Ordinary unload also owns the prop after its release cue. Priorities run first;
	# loss of the room/floor or a hazard cancels this observation.
	var continued:bool=stage=="workshop_unload" and goal=="curiosity"
	var completed:bool=elapsed_before+delta>=2.0 and stage==""
	var no_return:bool=preview_player==null or preview_player.return_plan.is_empty()
	if ordinary_release and no_return and (continued or completed) and active and not dead and movement_medium=="dry" and goal not in ["fire-retreat","flood-retreat"] and main.occupied.get(ordinary_cell,{}).get("id")=="salvage_workshop" and can_stand(ordinary_foot):
		var anchor:Vector2=ordinary_foot-(Vector2(ordinary_cell)+Vector2.ONE*.5)*384
		var value:Dictionary={"version":1,"source":FLOOR.SOURCE,"anchor":anchor}
		if FLOOR.valid_payload(value):main.occupied[ordinary_cell][FLOOR.FIELD]=value
func advance_work_return(main,delta:float)->bool:
	if preview_player!=null and preview_player.return_plan.is_empty() and not str(preview_player.last_source.get("key","")).ends_with("-west"):
		var player=preview_player;preview_player=null
		var result:bool=super.advance_work_return(main,delta)
		preview_player=player;return result
	return super.advance_work_return(main,delta)
func snapshot()->Dictionary:
	var data:Dictionary=super.snapshot()
	if data.stage=="unadmitted_james_cargo_return":data.stage=stage
	return data
