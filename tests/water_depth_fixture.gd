extends "res://scripts/grid_canvas.gd"
class TestClock extends RefCounted:
	var value:=0.0
	func get_visual_time_seconds()->float:return value
var water_test_clock:=TestClock.new()
var test_cell_size:=64.0
var test_first:=Vector2i.ZERO
var test_last:=Vector2i(7,7)
var test_part:="all"
var water_test_draw_usec:=0
func _ready():set_process(false)
func _cell_size()->float:return test_cell_size
func _get_main():return water_test_clock
func _view_rect(_main)->Rect2:return Rect2(-100000,-100000,200000,200000)
func _visible_cell_range(_main,_size,_static=false)->Array:return [test_first,test_last]
func _draw():
	draw_target=self
	var stamp:=Time.get_ticks_usec()
	_draw_underwater_depth(test_part)
	water_test_draw_usec=Time.get_ticks_usec()-stamp
