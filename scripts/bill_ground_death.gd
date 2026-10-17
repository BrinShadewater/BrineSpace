extends RefCounted
## Opt-in lowered entry for Bill's finite dry collapse family.
static func prepare(actor,game) -> void:
	actor.death_entry_seconds=0.0
	actor.death_ground_variant=""
	if actor.get_script().resource_path not in ["res://scripts/bill_npc.gd","res://scripts/major_bill_npc.gd","res://scripts/bill_carry_npc.gd"] or actor.dead or actor.movement_medium!="dry":return
	var pose:String=actor.animation_state()
	var grid=game.grid_view;var player=grid.human_water_player;var gear:String="diving-helmet" if actor.helmet_equipped else "";var key:String="death-ground-"+actor.direction
	var clips:Dictionary=player.frames if gear.is_empty() else player.equipment_frames.get(gear,{})
	if not clips.has(key) or not clips[key][0].get_meta("crew_lowered_death_entry",false):return
	if _choose_lateral(actor,clips,key):
		actor.death_ground_variant="lateral"
		key="death-ground-lateral-"+actor.direction
	if pose not in ["kneel","repair","stand"]:return
	var current:Texture2D=grid._get_human_frame_source(pose,actor.direction)
	if current==null:return
	var crown:float=current.get_meta("crew_alpha_extent").position.y
	# Axial falls project the head away/up on the screen. A crown threshold
	# cannot choose their physical posture; use the authored kneeling slot.
	if actor.direction in ["north","south"]:
		if crown>clips[key][0].get_meta("crew_alpha_extent").position.y+.5:actor.death_entry_seconds=.55
		return
	var elapsed:=0.0
	var durations:Array=player.timing[key].durations if gear.is_empty() else player.equipment_timing[gear][key].durations
	for i in clips[key].size():
		# Earliest authored fall pose whose crown does not lift the lowered caller.
		if clips[key][i].get_meta("crew_alpha_extent").position.y>=crown-.5:
			actor.death_entry_seconds=elapsed;return
		elapsed+=float(durations[i])/1000
	actor.death_entry_seconds=elapsed-float(durations[-1])/1000

static func texture(actor,grid,state:String,direction:String) -> Texture2D:
	if actor.get_script().resource_path not in ["res://scripts/bill_npc.gd","res://scripts/major_bill_npc.gd","res://scripts/bill_carry_npc.gd"] or not actor.dead or state!="death-ground":return null
	var player=grid.human_water_player;var gear:String="diving-helmet" if actor.helmet_equipped else "";var key:String=state+"-"+direction
	if actor.death_ground_variant=="lateral":key=state+"-lateral-"+direction
	var clips:Dictionary=player.frames if gear.is_empty() else player.equipment_frames.get(gear,{})
	if not clips.has(key) or not clips[key][0].get_meta("crew_lowered_death_entry",false):return null
	var game=grid._get_main();var elapsed:float=grid._advance_human_animation(key,game.get_visual_time_seconds(),game.get_test_walker_position()/grid._cell_size())
	return player.frame_at_elapsed(key,elapsed+actor.death_entry_seconds,gear)

static func _choose_lateral(actor,clips:Dictionary,key:String) -> bool:
	# Opt-in candidates only. This conservative screen-space test addresses the
	# observed furniture intrusion; it is not an anatomical floor-footprint model.
	if actor.direction not in ["north","south"] or not clips[key][0].get_meta("crew_death_contact_choice",false):return false
	var alternate:String="death-ground-lateral-"+actor.direction
	if not clips.has(alternate) or not clips[alternate][0].get_meta("crew_death_contact_choice",false):return false
	var cell:Vector2i=actor.cell_at(actor.foot)
	if not actor.geometry.has(cell):return false
	var local:Vector2=actor.foot-(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(0,384*.038)
	var blockers:Array=[]
	for prop in actor.geometry[cell].get("props",[]):blockers.append_array(actor.Geometry.prop_collision_rects(prop))
	var original:Rect2=clips[key][-1].get_meta("crew_alpha_extent")
	original.position+=local
	var blocked:=false
	for rect in blockers:
		if original.intersects(rect):blocked=true;break
	if not blocked:return false
	# Require the two settled poses to clear all registered props. Earlier
	# raised upper bodies project over furniture, like the standing caller;
	# those joins still need visual review rather than a floor proxy assertion.
	for i in range(4,clips[alternate].size()):
		var extent:Rect2=clips[alternate][i].get_meta("crew_alpha_extent")
		extent.position+=local
		for rect in blockers:
			if extent.intersects(rect):return false
	return true
