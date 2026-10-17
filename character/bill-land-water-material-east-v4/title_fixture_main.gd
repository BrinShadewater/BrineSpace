extends "res://character/bill-land-water-material-east-v4/title_fixture_base_main.gd"
const WET_CODEC=preload("res://character/bill-land-water-material-east-v3/checkpoint.gd")
const WET_GATE=preload("res://character/bill-land-water-material-east-v4/title_bridge_envelope.gd")
func _ready()->void:
 var checkpoint:Dictionary=RunSave.pending.duplicate(true)
 await super._ready()
 set_process(false);tick_timer.stop();_set_paused(true,false)
 crew_comms.set_process(false);crew_comms.minimize()
 var view=preload("res://character/bill-land-water-material-east-v4/view.gd").new()
 view.bridge_grid=grid_view;view.embedded=true;view.hide();grid_view.add_child(view);grid_view.rare_room_views["salvage_workshop"]=view
 var admitted:bool=WET_GATE.valid(checkpoint) and WET_CODEC.restore(grid_view,checkpoint.get("staged_bill_water_bridge"))
 set_meta("staged_water_bridge_admitted",admitted)
 set_meta("staged_water_bridge_ready",true)
