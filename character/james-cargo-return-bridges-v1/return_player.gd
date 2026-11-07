extends "res://scripts/crew_sprite_player.gd"
## Unselected staged return player; checkpoint admission is deliberately pending.
var return_plan:Dictionary={}
var last_source:Dictionary={}
var return_clock:=0.0
func bank_for(gear:String)->Dictionary:return frames if gear.is_empty() else equipment_frames.get(gear,{})
func return_active(time:float)->bool:
	return not return_plan.is_empty() and time>=return_plan.started and time<return_plan.until
func return_texture(time:float,gear:String)->Texture2D:
	if not return_active(time) or gear!=return_plan.gear:return null
	var cursor:float=time-return_plan.started
	for row in return_plan.rows:
		cursor-=float(row.seconds)
		if cursor<0:return bank_for(gear)[row.key][row.index]
	return null
func remember(texture:Texture2D,key:String,gear:String)->void:
	var bank:Dictionary=bank_for(gear)
	if texture==null or not bank.has(key):last_source.clear();return
	var index:int=bank[key].find(texture)
	last_source={"key":key,"index":index,"gear":gear} if index>=0 else {}
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=false)->Texture2D:
	return_clock=time
	if state!="carry":return_plan.clear()
	var returning:Texture2D=return_texture(time,equipment)
	if returning!=null:return returning
	var result:Texture2D=super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
	remember(result,str(motion.clip) if not str(motion.get("clip","")).is_empty() else current_key,equipment)
	return result
func frame_at_elapsed(key:String,elapsed:float,equipment:String="")->Texture2D:
	var result:Texture2D=super.frame_at_elapsed(key,elapsed,equipment)
	remember(result,key,equipment)
	return result
