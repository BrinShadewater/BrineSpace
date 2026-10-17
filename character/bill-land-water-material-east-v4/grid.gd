extends "res://character/bill-land-water-runtime-east-v1/grid.gd"
## Per-instance presentation parameters; never mutate shared source textures.
var material_source:Texture2D
var material_weight:float=-1
var material_head_offset:=Vector2.ZERO
func _get_human_frame_source(state:String,direction:String)->Texture2D:
 var shown:Texture2D=super._get_human_frame_source(state,direction)
 material_source=shown
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
 var crowns:Array=[Vector2(171,82),Vector2(177,91),Vector2(180,124),Vector2(183,157),Vector2(187,188)] if enter else [Vector2(189,181),Vector2(184,145),Vector2(179,108),Vector2(168,98),Vector2(165,76)]
 if index==0:material_head_offset=Vector2(0,-58) if enter else Vector2(22,-6)
 elif index>=bridge.poses.size()-1:material_head_offset=Vector2(22,-6) if enter else Vector2(0,-58)
 else:material_head_offset=(crowns[index-1]+Vector2(8,15)-Vector2(160,224))*(65.28/148)
 return shown

func bridge_bank(gear:String,enter:bool)->Array:
 if not enter:return super.bridge_bank(gear,enter)
 var id:String=gear+"-enter"
 if not bridge_banks.has(id):
  var files:Dictionary={"":"res://character/bill-land-water-east-v5/bare/manifest.json","diving-helmet":"res://character/bill-land-water-east-v5/helmet/manifest.json"}
  var loader=preload("res://scripts/crew_sprite_player.gd").new();loader.load_manifest(files[gear],true)
  bridge_banks[id]=[loader.frames["land-swim-east"],loader.timing["land-swim-east"].durations]
 return bridge_banks[id]
