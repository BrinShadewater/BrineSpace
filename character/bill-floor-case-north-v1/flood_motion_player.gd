extends "res://character/bill-floor-case-north-v1/finish_player.gd"
## Fixture-only authored source playback; no controller or route acceptance claim.
var study_key:=""
var study_elapsed:=0.0
func frame(state:String,direction:String,time:float,position_cells:Vector2,equipment:String="",allow_water_transition:bool=true)->Texture2D:
 if not study_key.is_empty():return frame_at_elapsed(study_key,study_elapsed,equipment)
 return super.frame(state,direction,time,position_cells,equipment,allow_water_transition)
