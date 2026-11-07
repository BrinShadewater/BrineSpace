extends "res://character/bill-carry-cardinal-runtime-v3/stow_actor.gd"
## Selected Bill carry controller; base furniture, needs and hazard logic retained.
func snapshot()->Dictionary:
 var data:Dictionary=super.snapshot()
 data.carry_binding=preview_player.carry_binding() if preview_player!=null else preload("res://scripts/bill_carry_player.gd").MASTER_BINDING
 return data
func rebuild(main,staged:=false)->void:
 preview_player=main.grid_view.human_water_player
 await super.rebuild(main,staged)
func update(main,delta:float)->void:
 preview_player=main.grid_view.human_water_player
 super.update(main,delta)
 if not preview_player.stow_plan.is_empty() and preview_time>=float(preview_player.stow_plan.until):preview_player.stow_plan.clear()
func restore_snapshot(main,data:Dictionary,staged:=false)->void:
 preview_player=main.grid_view.human_water_player
 var restored:Dictionary=data.duplicate(true)
 if not restored.has("carry_binding"):
  restored.carry_binding=BINDING;restored.carry_pivot={};restored.carry_arrival={}
 var binding:String=str(restored.carry_binding)
 if not preload("res://scripts/bill_carry_player.gd").supported_binding(binding):return
 restored.carry_binding=BINDING
 if not preload("res://character/bill-carry-cardinal-runtime-v3/stow_actor.gd").valid_carry_snapshot(restored):return
 if not preview_player.select_binding(binding):return
 await super.restore_snapshot(main,restored,staged)
func set_helmet_equipped(value:bool)->bool:
 var previous:bool=helmet_equipped
 var accepted:bool=super.set_helmet_equipped(value)
 if accepted and previous!=value and preview_player!=null:
  preview_player.clear_carry();preview_player.current_equipment="diving-helmet" if value else "";planted_until=-1;planted_clip=""
 return accepted

func die()->void:
 if preview_player!=null:preview_player.clear_carry()
 planted_until=-1;planted_clip=""
 super.die()
