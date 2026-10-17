extends "res://character/bill-land-water-runtime-east-v1/grid.gd"
## Per-instance presentation parameters; never mutate shared source textures.
var material_weight:float=-1
var material_head_offset:=Vector2.ZERO
func _get_human_frame_source(state:String,direction:String)->Texture2D:
 var shown:Texture2D=super._get_human_frame_source(state,direction)
 material_weight=-1
 if bridge.is_empty():return shown
 var enter:bool=bridge.target_state=="swim"
 var elapsed:float=clampf(_get_main().get_visual_time_seconds()-float(bridge.started),0,.5)
 var progress:float=smoothstep(0,.5,elapsed)
 material_weight=progress if enter else 1-progress
 var index:int=0;var cursor:float=elapsed
 for duration in bridge.durations:
  if cursor<float(duration)/1000:break
  cursor-=float(duration)/1000;index+=1
 var crowns:Array=[Vector2(171,88),Vector2(177,118),Vector2(183,157),Vector2(187,188)] if enter else [Vector2(189,181),Vector2(184,145),Vector2(179,108),Vector2(168,98),Vector2(165,76)]
 if index==0:material_head_offset=Vector2(0,-58) if enter else Vector2(22,-6)
 elif index>=bridge.poses.size()-1:material_head_offset=Vector2(22,-6) if enter else Vector2(0,-58)
 else:material_head_offset=(crowns[index-1]+Vector2(8,15)-Vector2(160,224))*(65.28/148)
 return shown
