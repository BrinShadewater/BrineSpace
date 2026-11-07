extends SceneTree
const Effects=preload("res://scripts/station_effects.gd")
const Settings=preload("res://scripts/title_settings.gd")
class Grid extends RefCounted:
	func _room_light_level(_room):return 1.0
class Game extends Node:
	var grid_view=Grid.new()
	var placed_rooms: Array=[{"pos":Vector2i.ZERO}]
	var clock:=20.0
	func get_visual_time_seconds():return clock
var failures:=0
func check(value: bool,message: String):
	if not value:failures+=1;push_error(message)
func _initialize():
	var game:=Game.new()
	Settings.effects_quality=1;Settings.reduced_motion=true
	Effects.draw_build_flourish(null,game,[],384)
	game.clock=21.0;game.placed_rooms.append({"pos":Vector2i.ONE})
	Effects.draw_build_flourish(null,game,[],384)
	check(Effects._ripple_start.get(Vector2i.ONE)==21.0,"A normal powered completion still emits its flourish")
	game.clock=0.0;Effects.draw_build_flourish(null,game,[],384)
	check(Effects._ripple_start.is_empty() and Effects._scan_start.is_empty(),"Clock reset must drop prior-loop flourishes")
	game.clock=1.0;game.placed_rooms.append({"pos":Vector2i(2,2)})
	Effects.draw_build_flourish(null,game,[],384)
	check(Effects._ripple_start.get(Vector2i(2,2))==1.0,"Completion still works after a reset")
	Effects.draw_build_flourish(null,game,[],384)
	check(Effects._ripple_start.get(Vector2i(2,2))==1.0,"A paused completion does not restart")
	game.clock=4.0;Settings.reduced_motion=false
	Effects._ripple_start[Vector2i(3,3)]=100.0
	# All legitimate effects are expired. A future timestamp must not draw a
	# negative-radius arc; null canvas makes unintended drawing fail visibly.
	Effects.draw_build_flourish(null,game,[],384)
	check(Effects._ripple_start.is_empty(),"Future ripple timestamps are discarded")
	game.free()
	print("BUILD FLOURISH RESET: %d failures"%failures)
	quit(failures)
