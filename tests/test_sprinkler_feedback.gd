extends SceneTree
const Main=preload("res://scripts/main.gd")
const Controls=preload("res://scripts/hardware_panel.gd")
var failures:=0
func check(ok:bool,message:String)->void:
	if not ok:failures+=1;print("FAIL: ",message)
func _initialize()->void:run.call_deferred()
func run()->void:
	var game=Main.new();game.resources={"water":0,"power":1};game.hardware.sprinklers=true
	var panel=Controls.new();panel.game=game;root.add_child(panel)
	panel.refresh()
	check(panel.controls.sprinklers.status.text=="ARMED","Enabled switch distinguishes armed from currently spraying")
	var room:Dictionary={"id":"galley","display_name":"Galley","pos":Vector2i.ZERO,"fire":.8,"fire_water_seconds":0.0}
	game.placed_rooms.append(room);panel.refresh()
	check(panel.controls.sprinklers.status.text=="NO WATER","An enabled dry system shows the actual blockage")
	room.fire_water_seconds=2.0;panel.refresh()
	check(panel.controls.sprinklers.status.text=="SPRAYING","Prepaid spray still works with an empty reserve")
	game.placed_rooms.append({"id":"reactor","display_name":"Reactor","pos":Vector2i.RIGHT,"fire":.8,"fire_water_seconds":0.0});panel.refresh()
	check(panel.controls.sprinklers.status.text=="LOW WATER","Partial coverage is visible when another room is dry")
	var tip:String=game._resource_sources_tip("water",{"offline":{},"added_crew":0})
	check(tip.contains("2 burning") and tip.contains("5s") and tip.contains("per-cycle"),"Water hint separates live sprinkler demand from the cycle forecast")
	game.hardware.power=false;panel.refresh()
	check(panel.controls.sprinklers.status.text=="NO POWER","Master power loss is shown even with prepaid Water")
	game.hardware.sprinklers=false;panel.refresh()
	check(panel.controls.sprinklers.status.text=="OFF","Disabled remains off")
	check(game.resources.water==0 and game.resources.power==1,"Feedback spends no resources")
	panel.free();game.free()
	print("SPRINKLER FEEDBACK failures=",failures)
	quit(1 if failures else 0)
