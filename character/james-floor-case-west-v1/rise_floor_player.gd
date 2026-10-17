extends "res://character/james-cargo-return-bridges-v1/return_player.gd"
const FLOOR=preload("res://character/james-floor-case-west-v1/rise_floor_state.gd")
var preview_game
var preview_view
var preview_cell:=Vector2i(-1,-1)
func observe(texture:Texture2D,equipment:String)->void:
	if preview_game==null or preview_view==null:return
	var actor=preview_game.branforth_npc
	var now:float=preview_game.get_visual_time_seconds()
	if return_active(now) and return_texture(now,equipment)==texture:
		FLOOR.observe_plan(preview_game,actor,self,now)
	preview_view.bind_room(preview_game.occupied.get(preview_cell,{}))
	preview_view.bind_frame(texture,self,equipment,actor.foot-(Vector2(preview_cell)+Vector2.ONE*.5)*384)
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
	var texture:Texture2D=super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
	observe(texture,equipment);return texture
func frame_at_elapsed(key:String,elapsed:float,equipment:String="")->Texture2D:
	var texture:Texture2D=super.frame_at_elapsed(key,elapsed,equipment)
	observe(texture,equipment);return texture
