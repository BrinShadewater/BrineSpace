extends SceneTree
class GridProbe extends "res://scripts/grid_canvas.gd":
 var fixture_main
 func _get_main():return fixture_main
class Sites extends RefCounted:
 var active:=false
 func is_site(_main,_pos):return active
class FixtureMain extends RefCounted:
 var Companions=Sites.new()
 var companion_actors={}
 var actor:=false
 func get_cell_size():return 384.0
 func has_test_walker():return actor
 func get_test_walker_position():return Vector2.ZERO
 func has_dr_veld():return false
 func has_chief_branforth():return false
 func has_marsh():return false
var checks:=0
var failed:=false
func check(value:bool,message:String):
 checks+=1
 if not value:failed=true;push_error(message)
func _initialize():
 if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var view=load("res://scripts/james_cargo_workshop.gd").new()
 var grid=GridProbe.new()
 var main=FixtureMain.new();grid.fixture_main=main
 var room={"id":"salvage_workshop","pos":Vector2i.ZERO}
 view.bind_room(room)
 check(view.retained_floor_case_key().is_empty(),"Empty case")
 check(grid._room_setup_skippable(main,room,view),"Empty actor-free workshop can retain")
 room[view.FLOOR.FIELD]={"version":1,"source":view.FLOOR.SOURCE,"anchor":Vector2(10,20)}
 var before:Dictionary=view.retained_floor_case_key()
 check(not before.is_empty(),"Added case invalidates empty key")
 room[view.FLOOR.FIELD]["anchor"]=Vector2(30,40)
 check(before.anchor==Vector2(10,20),"Stored key does not alias mutable payload")
 check(before!=view.retained_floor_case_key(),"Moved case changes key")
 room.erase(view.FLOOR.FIELD)
 check(view.retained_floor_case_key().is_empty(),"Removed case changes key")
 main.actor=true
 check(not grid._room_setup_skippable(main,room,view),"Actor entry prepares workshop")
 main.actor=false
 check(grid._room_setup_skippable(main,room,view),"Actor exit allows retention")
 main.Companions.active=true
 check(not grid._room_setup_skippable(main,room,view),"Companion site remains excluded")
 main.Companions.active=false;room.recovered_derelict=true
 check(not grid._room_setup_skippable(main,room,view),"Recovered derelict remains excluded")
 grid.free();view.free()
 print("WORKSHOP_GUARDS ",checks," checks; failures=",failed)
 quit(1 if failed else 0)
