extends "res://character/bill-land-water-material-west-v8/grid.gd"
## Fixture-only source-bound head readability; keep V8 baseline and source artwork exact.
var source_head_centers:Dictionary={}
var fitted_head_data:Dictionary={}
var head_binding_kind:String="inactive"
func head_data()->Dictionary:
 if fitted_head_data.is_empty():fitted_head_data=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-land-water-material-west-v9/head-centers.json")).centers
 return fitted_head_data
func bridge_bank(gear:String,enter:bool)->Array:
 var bank:Array=super.bridge_bank(gear,enter)
 var label:String=("entry-" if enter else "exit-")+("bare" if gear.is_empty() else "helmet")
 var centers:Array=head_data()[label]
 for i in range(centers.size()):source_head_centers[bank[0][i+1]]=Vector2(centers[i][0],centers[i][1])
 return bank
func bind_swim_centers()->void:
 for gear in ["","diving-helmet"]:
  var poses:Array=human_water_player.frames.get("swim-west",[]) if gear.is_empty() else human_water_player.equipment_frames.get(gear,{}).get("swim-west",[])
  var centers:Array=head_data()["swim-"+("bare" if gear.is_empty() else "helmet")]
  if poses.size()!=centers.size():continue
  for i in range(poses.size()):source_head_centers[poses[i]]=Vector2(centers[i][0],centers[i][1])
func _get_human_frame_source(state:String,direction:String)->Texture2D:
 bind_swim_centers()
 var shown:Texture2D=super._get_human_frame_source(state,direction)
 head_binding_kind="inactive"
 if material_weight<0:return shown
 head_binding_kind="historical-gait-fallback"
 if source_head_centers.has(shown):
  var pivot:Vector2=shown.get_meta("crew_pivot",Vector2(160,224))
  var scale:float=65.28/float(shown.get_meta("crew_standing_height",148))
  material_head_offset=(Vector2(source_head_centers[shown])-pivot)*scale
  head_binding_kind="current-source-donor-center"
 return shown
