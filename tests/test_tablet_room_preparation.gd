extends SceneTree
class Grid extends "res://scripts/grid_canvas.gd":
	var prepared:Array=[]
	func _bill_room_view(room:Dictionary):
		prepared.append(str(room.id))
		return null
class Fleet extends RefCounted:
	var orders:Array=[]
	var drones:Dictionary={}
class Station extends RefCounted:
	var hand:Array=["galley","cold_store","current_turbine"]
	var selected_card_id:=""
	var placed_rooms:Array=[]
	var drone_fleet=Fleet.new()
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
	if not ok:failures+=1;push_error(label)
func run():
	if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	root.set_meta("tablet_controls",true)
	var grid=Grid.new()
	var station=Station.new()
	for i in range(4):grid.prewarm_room_views(station)
	check(grid.prepared.is_empty(),"Unselected tablet cards do not instantiate full room artwork")
	grid.prepared.clear();grid.prewarmed_room_ids.clear()
	station.placed_rooms=[{"id":"crew_hab"}]
	station.drone_fleet.orders=[{"id":"storage_bay"}]
	station.drone_fleet.drones={1:{"order":{"id":"ore_refinery"}}}
	station.selected_card_id="current_turbine"
	for i in range(6):grid.prewarm_room_views(station)
	check(grid.prepared==["current_turbine","crew_hab","storage_bay","ore_refinery"],"Selected, placed and queued/fitting rooms still prepare once")
	station.selected_card_id=""
	for i in range(4):grid.prewarm_room_views(station)
	check(grid.prepared.size()==4,"Returning the card does not start loading unrelated hand rooms")
	if not OS.has_feature("ios"):
		root.set_meta("tablet_controls",false)
		grid.prepared.clear();grid.prewarmed_room_ids.clear()
		grid.prewarm_room_views(station)
		check(grid.prepared==["galley"],"Desktop keeps one hand-room preparation per call")
	grid.free()
	print("TABLET ROOM PREPARATION ",failures," failures")
	quit(1 if failures else 0)
