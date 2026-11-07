extends "res://character/bill-land-water-material-east-v2/view.gd"
var bridge_grid
func draw_actor()->void:
 material_weight=-1
 if is_instance_valid(bridge_grid) and external_actor_texture==bridge_grid.material_source:
  material_weight=bridge_grid.material_weight
  material_head_offset=bridge_grid.material_head_offset
 super.draw_actor()
