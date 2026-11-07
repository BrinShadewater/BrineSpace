extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
class SelectionGrid extends Grid:
	var requested:Dictionary={}
	var markers:Dictionary={}
	func _lazy_view(key:StringName,_script:Script):
		requested[key]=int(requested.get(key,0))+1
		if not markers.has(key):markers[key]=RefCounted.new()
		return markers[key]
var failures:=0
func check(ok:bool,message:String):
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	var expected={"research_lab":&"research_view","hydroponics_bay":&"hydroponics_view","life_support":&"life_support_view","mycelium_nursery":&"nursery_view","unknown-fixture":&"nursery_view"}
	var grid:=SelectionGrid.new()
	for id in expected:
		grid.requested.clear()
		var view=grid._bill_room_view({"id":id})
		check(grid.requested.size()==1 and grid.requested.has(expected[id]),"Only the selected room view initializes: "+id)
		check(view==grid.markers.get(expected[id]),"Selected view/fallback remains the same: "+id)
	for item in [grid.seabed_background,grid.wreck_view,grid.rock_view]:
		if item is Node:item.free()
	grid.free()
	print("ROOM_VIEW_SELECTION ","PASS" if failures==0 else "FAIL "+str(failures))
	quit(1 if failures else 0)
