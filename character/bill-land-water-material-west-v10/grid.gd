extends "res://character/bill-land-water-material-west-v9/grid.gd"
var source_head_sizes:Dictionary={}
var head_probe_texture:Texture2D
func bridge_bank(gear:String,enter:bool)->Array:
 var bank:Array=super.bridge_bank(gear,enter)
 var count:int=5 if enter else 6
 for i in range(count):source_head_sizes[bank[0][i+1]]=Vector2(21,23) if gear.is_empty() else Vector2(40,40)
 return bank
func bind_swim_centers()->void:
 super.bind_swim_centers()
 for gear in ["","diving-helmet"]:
  var poses:Array=human_water_player.frames.get("swim-west",[]) if gear.is_empty() else human_water_player.equipment_frames.get(gear,{}).get("swim-west",[])
  if poses.size()!=7:continue
  for texture in poses:source_head_sizes[texture]=Vector2(21,23) if gear.is_empty() else Vector2(40,40)
func _get_human_frame_source(state:String,direction:String)->Texture2D:
 if head_probe_texture!=null:
  bind_swim_centers()
  material_source=head_probe_texture;material_weight=-1;head_binding_kind="controlled-normal-swim-probe"
  return head_probe_texture
 return super._get_human_frame_source(state,direction)
