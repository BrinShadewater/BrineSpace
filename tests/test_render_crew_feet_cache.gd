extends SceneTree
var checks:=0
var failures:=0
class Grid extends "res://scripts/grid_canvas.gd":
	var test_size:=96.0
	func _cell_size()->float:return test_size
class Companion extends RefCounted:
	var active:=true
	var foot:=Vector2(1152,768)
class Station extends RefCounted:
	var size_value:=96.0
	var cell:=Vector2(4,3)
	var queries:=0
	var companion_actors:Dictionary={"fixture":Companion.new()}
	func has_test_walker()->bool:return true
	func has_dr_veld()->bool:return false
	func has_chief_branforth()->bool:return false
	func has_marsh()->bool:return false
	func get_test_walker_position()->Vector2:
		queries+=1
		return cell*size_value
func _init():call_deferred("run")
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;print("FAILED: ",message)
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var grid:=Grid.new();var station:=Station.new()
	var first:PackedVector2Array=grid._crew_feet(station)
	check(first[0].is_equal_approx(Vector2(384,291.648)),"Initial crew foot uses current scale and lift")
	check(first[1]==Vector2(288,192),"Companion foot uses current scale")
	check(grid._crew_feet(station)==first and station.queries==1,"Unchanged same-frame input reuses gathered positions")
	grid.test_size=192;station.size_value=192
	var zoomed:PackedVector2Array=grid._crew_feet(station)
	check(zoomed[0].is_equal_approx(Vector2(768,583.296)),"Same-frame zoom invalidates crew pixel positions")
	check(zoomed[1]==Vector2(576,384),"Same-frame zoom invalidates companion pixel positions")
	check(grid._nearest_crew_foot(station,Vector2(768,584)).is_equal_approx(Vector2(768,583.296)),"Door depth query uses updated zoom position")
	var other:=Station.new();other.size_value=192;other.cell=Vector2(5,5)
	var replaced:PackedVector2Array=grid._crew_feet(other)
	check(replaced[0].is_equal_approx(Vector2(960,967.296)),"Same-frame station replacement invalidates owner")
	check(grid._crew_feet(other)==replaced and other.queries==1,"Replacement owner reuses only its own gathered positions")
	var previous_tick:=Engine.get_process_frames()
	while Engine.get_process_frames()==previous_tick:await process_frame
	grid._crew_feet(other)
	check(other.queries==2,"Next frame refreshes moving crew input")
	grid.free()
	FileAccess.open("user://result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
	print("CREW FEET CACHE: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
