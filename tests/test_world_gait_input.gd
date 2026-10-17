extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
var checks:=0
var failures:=0
func check(value:bool,message:String)->void:
	checks+=1
	if not value:failures+=1;push_error(message)
func make_player():
	var p=Player.new()
	p.frames={"walk-north":[null]}
	p.timing={"walk-north":{"durations":[1000],"loop":true}}
	p.strides={"walk":.12}
	return p
func _initialize():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var grid=load("res://scripts/grid_canvas.gd").new()
	var foot:=Vector2(7858.305,8099.799)
	var world=make_player();var projected=make_player()
	var zooms:Array=[.1875,.159375,.1753125,.19284375,.212128125,.2333409375,.25667503125,.855,.1,.99,1.2,1.0]
	for i in zooms.size():
		var time:float=float(i)/60.0
		var size:float=720.0*float(zooms[i])
		var canonical:Vector2=foot/384.0-Vector2(0,.038)
		var actual:Vector2=grid._branforth_gait_position({"branforth_npc":{"foot":foot}})
		check(actual==canonical,"World gait input matches physical foot")
		world.frame("walk","north",time,actual)
		projected.frame("walk","north",time,(canonical*size)/size)
		check(world.phase==0.0,"Zoom cannot advance stationary world gait")
		var before:Dictionary=world.snapshot().duplicate(true)
		world.frame("walk","north",time,actual)
		check(world.snapshot()==before,"Repeated paused sample preserves playback")
		var resumed=make_player();resumed.restore_snapshot(world.snapshot())
		check(resumed.snapshot()==world.snapshot(),"World gait playback restores exactly")
		world=resumed
	check(projected.phase>0.0,"Fixture reproduces camera round-trip gait error")
	grid.free()
	print("WORLD_GAIT_INPUT ",checks," checks, ",failures," failures")
	quit(0 if failures==0 else 1)
