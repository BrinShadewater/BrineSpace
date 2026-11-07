extends SceneTree
const Context=preload("res://scripts/retained_wall_context.gd")
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(value:bool,label:String):
	checks+=1
	if not value:failures+=1;push_error(label)
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var rooms:Array=[{"pos":Vector2i.ZERO,"id":"reactor","rotation":0},{"pos":Vector2i.RIGHT,"id":"corridor","rotation":0}]
	var occupied:Dictionary={Vector2i.ZERO:rooms[0],Vector2i.RIGHT:rooms[1]}
	var powered:Dictionary={Vector2i.ZERO:true,Vector2i.RIGHT:true}
	var hardware:Dictionary={"interior":true,"walls":true,"power":true,"pumps":true,"exterior":true,"doors":false,"sprinklers":false}
	var common:Array=[hardware,384.0,rooms,2,powered,[],1,true,Vector2i(-1,-1),true,0.0]
	var cache=Context.new()
	cache.prepare(common,occupied,powered,rooms)
	var shell:Array=cache.key(rooms[0],0.0).duplicate(true)
	var corridor:Array=cache.key(rooms[1],1.0).duplicate(true)
	var builds:int=cache.builds
	hardware.interior=false
	cache.prepare(common,occupied,powered,rooms)
	check(cache.key(rooms[0],0.0)==shell,"Interior switch does not invalidate room shell")
	check(cache.key(rooms[1],1.0)==corridor,"Interior switch alone does not invalidate corridor geometry")
	check(cache.builds==builds,"Interior-only toggle reuses context preparation")
	check(cache.key(rooms[1],0.25)!=corridor,"Corridor fade still invalidates its shade")
	check(common[0].has("interior") and not common[0].interior,"Projection preserves caller hardware")
	for flag in ["walls","power","pumps","exterior","doors","sprinklers"]:
		var before:Array=cache.key(rooms[0],0.0).duplicate(true)
		hardware[flag]=not hardware[flag]
		cache.prepare(common,occupied,powered,rooms)
		check(cache.key(rooms[0],0.0)!=before,"Other hardware dependency remains: "+flag)
	print("WALL INTERIOR INVALIDATION ",JSON.stringify({"checks":checks,"failures":failures}))
	quit(1 if failures else 0)
