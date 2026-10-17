extends "res://character/bill-land-water-material-east-v2/grid.gd"
var material_source:Texture2D
func _get_human_frame_source(state:String,direction:String)->Texture2D:
 material_source=super._get_human_frame_source(state,direction)
 return material_source
