extends "res://scripts/branforth_npc.gd"
## Candidate fixture actor. Needs/fire/flood run before inherited work-return hook.
## Missing standing/floor join remains explicit; not normally installed.
var preview_player
var return_reason:=""
var return_geometry:Dictionary={}
func cargo_return_active()->bool:
	return preview_player!=null and active and not dead and movement_medium=="dry" and goal=="" and stage=="" and state=="idle" and not preview_player.return_plan.is_empty() and ("diving-helmet" if helmet_equipped else "")==preview_player.return_plan.gear and preview_player.return_active(preview_player.return_clock)
func die()->void:
	if preview_player!=null:preview_player.return_plan.clear()
	super.die()
func set_helmet_equipped(value:bool)->bool:
	var accepted:bool=super.set_helmet_equipped(value)
	if preview_player!=null and not preview_player.return_plan.is_empty() and ("diving-helmet" if helmet_equipped else "")!=preview_player.return_plan.gear:preview_player.return_plan.clear()
	return accepted
func _init()->void:
	# Filename-based legacy lazy loading would otherwise choose Bill for a subclass.
	var profile:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/chief-engineer-branforth-v2/clearance.json"))
	swim_clearance=profile.swim;tread_clearance=profile.tread;action_clearance=profile.actions
func update(main,delta:float)->void:
	if preview_player!=null and not preview_player.return_plan.is_empty():
		var plan:Dictionary=preview_player.return_plan
		if dead or not active or movement_medium!="dry" or ("diving-helmet" if helmet_equipped else "")!=plan.gear or goal in ["fire-retreat","flood-retreat"] or not can_stand(foot):
			preview_player.return_plan.clear();return_reason="priority cancelled"
	super.update(main,delta)
	if preview_player!=null and not preview_player.return_plan.is_empty() and (dead or not active or movement_medium!="dry" or goal!="" or stage!=""):
		preview_player.return_plan.clear();return_reason="normal service or hazard replaced return"
func advance_work_return(main,delta:float)->bool:
	if preview_player==null:return super.advance_work_return(main,delta)
	var now:float=main.get_visual_time_seconds();preview_player.return_clock=now
	if not preview_player.return_plan.is_empty():
		if now<preview_player.return_plan.started or now>=preview_player.return_plan.until:
			preview_player.return_plan.clear();preview_player.motion.clear();preview_player.current_key="";return_reason="finite source segment complete; standing/floor join pending"
			return false
		return true
	if not active or dead or movement_medium!="dry" or stage not in ["workshop_pickup","workshop_carry","workshop_unload"] or service_available(main,goal_cell):return super.advance_work_return(main,delta)
	var source:Dictionary=preview_player.last_source
	if source.is_empty():return_reason="missing displayed source";return false
	var plan:Dictionary=preload("res://character/james-east-cargo-heads-v3/return_plan.gd").build(preview_player,source.key,source.index,source.gear)
	if plan.is_empty() or plan.gaps.any(func(gap):return str(gap.to).begins_with("unload-")):return_reason="held join missing";return false
	var bank:Dictionary=preview_player.bank_for(source.gear);var extent:=Rect2();var first:=true
	var initial:Texture2D=bank[source.key][source.index];var new_drawing:=false
	var seconds:=0.0
	for row in plan.rows:
		var texture:Texture2D=bank[row.key][row.index]
		if not preload("res://character/james-east-cargo-heads-v3/return_plan.gd").same(initial,texture):new_drawing=true
		var bounds:Rect2=texture.get_meta("crew_alpha_extent")
		extent=bounds if first else extent.merge(bounds);first=false;seconds+=row.seconds
	var envelope_clear:bool=swim_segment_clear(foot,foot,direction,direction,false,[extent.position.x,extent.position.y,extent.end.x,extent.end.y])
	return_geometry={"newDrawing":new_drawing,"envelopeClear":envelope_clear,"footClear":can_stand(foot),"extent":extent}
	# An immutable terminal pose already on screen adds no new body/case geometry.
	# Hold it finitely at the existing valid foot; changing poses still need clearance.
	if new_drawing and not envelope_clear:return_reason="return source envelope blocked";return false
	plan.started=now;plan.until=now+seconds;preview_player.return_plan=plan
	preview_player.motion.clear();preview_player.current_key=""
	path.clear();goal="";stage="";state="idle";timer=0;activity="returning workshop case"
	return_reason="source-bound return admitted"
	return true
func animation_state()->String:
	if cargo_return_active():return "carry"
	return super.animation_state()
func action_elapsed()->float:
	if cargo_return_active():return -1.0
	return super.action_elapsed()
func can_step_aside()->bool:
	return not cargo_return_active() and super.can_step_aside()
func snapshot()->Dictionary:
	var data:Dictionary=super.snapshot()
	# Prevent normal RunSave from silently omitting a candidate return lifecycle.
	# Paired save/restore admission must precede production selection.
	if preview_player!=null and not preview_player.return_plan.is_empty():data.stage="unadmitted_james_cargo_return"
	return data
