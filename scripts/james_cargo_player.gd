extends "res://character/james-cargo-return-bridges-v1/return_player.gd"
const FLOOR=preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd")
var game
var case_texture:Texture2D
func _init()->void:
	var image:=Image.new()
	if preload("res://scripts/safe_image.gd").load_png(image,FLOOR.ART_PATH)==OK:case_texture=ImageTexture.create_from_image(image)
func join_north_unload_entry()->void:
	# Reuse the whole registered standing drawing at this stationary cut.
	# Clocks, remaining poses and equipment banks keep their authored data.
	for bank in [frames]+equipment_frames.values():
		if not bank.has("carry-turn-west-north") or not bank.has("unload-north"):continue
		if bank["carry-turn-west-north"].is_empty() or bank["unload-north"].is_empty():continue
		var endpoint:Texture2D=bank["carry-turn-west-north"][-1]
		var entrance:Texture2D=bank["unload-north"][0]
		if endpoint.get_size()!=entrance.get_size() or endpoint.get_meta("crew_pivot")!=entrance.get_meta("crew_pivot") or endpoint.get_meta("crew_standing_height")!=entrance.get_meta("crew_standing_height"):continue
		bank["unload-north"][0]=endpoint
func load_manifest(path:String,merge:bool=false,load_stride_overrides:bool=true)->void:
	super.load_manifest(path,merge,load_stride_overrides)
	join_north_unload_entry()
func load_equipment_manifest(equipment:String,path:String)->bool:
	var loaded:bool=super.load_equipment_manifest(equipment,path)
	if loaded:join_north_unload_entry()
	return loaded
func floor_texture()->Texture2D:
	if game!=null:
		var view=game.grid_view.rare_room_views.get("salvage_workshop")
		if is_instance_valid(view) and view.has_method("case_rect"):return view.case_texture
	return case_texture
func observe()->void:
	if game==null:return
	FLOOR.observe_plan(game,game.branforth_npc,self,game.get_visual_time_seconds())
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
	var texture:Texture2D=super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
	observe();return texture
func frame_at_elapsed(key:String,elapsed:float,equipment:String="")->Texture2D:
	if game!=null and key=="unload-north":
		var arrival:Dictionary=preload("res://scripts/james_workshop_arrival.gd").presentation(game.branforth_npc,self,elapsed,equipment)
		if not arrival.is_empty():
			key=arrival.key;elapsed=arrival.elapsed
	var texture:Texture2D=super.frame_at_elapsed(key,elapsed,equipment)
	observe();return texture
