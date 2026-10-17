extends SceneTree
const Context=preload("res://scripts/retained_floor_context.gd")
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func common(rooms:Array,powered:Dictionary,hardware:Dictionary)->Array:
	var structures:Array=[];var entries:Array=[]
	for room in rooms:
		structures.append(room.duplicate(true))
		entries.append([room.pos,[false,false,false,false],1.0,false,"",true,0,false,0.0,true])
	return [hardware,128.0,structures,rooms.size(),powered,entries,1,true,Vector2i(-1,-1),true,0.0]
func keys(ctx,rooms:Array)->Dictionary:
	var result:Dictionary={}
	for room in rooms:result[room.pos]=ctx.key(room,0.0).duplicate(true)
	return result
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var ctx:=Context.new();var occupied:Dictionary={};var rooms:Array=[];var power:Dictionary={}
	var hardware:={"walls":true,"interior":true,"power":true}
	for y in range(5):
		for x in range(8):
			var room:={"id":"reactor","pos":Vector2i(x,y),"rotation":0,"ports":["north","east"],"water_level":0.0}
			occupied[room.pos]=room;rooms.append(room);power[room.pos]=true
	var c:Array=common(rooms,power,hardware);ctx.prepare(c,occupied,power,rooms)
	var before:Dictionary=keys(ctx,rooms)
	occupied[Vector2i(40,40)]={"id":"corridor","pos":Vector2i(40,40),"rotation":0}
	c[3]+=1;ctx.prepare(c,occupied,power,rooms)
	check(before==keys(ctx,rooms),"Unrelated offscreen room count does not dirty floors")
	var changed:=Vector2i(3,2);occupied[changed].rotation=1
	c=common(rooms,power,hardware);ctx.prepare(c,occupied,power,rooms)
	for room in rooms:
		var local:bool=absi(room.pos.x-changed.x)<=1 and absi(room.pos.y-changed.y)<=1
		check((before[room.pos]!=ctx.key(room,0.0))==local,"Rotation dirties exactly local dependency footprint")
	before=keys(ctx,rooms);hardware.interior=false;c=common(rooms,power,hardware);ctx.prepare(c,occupied,power,rooms)
	for room in rooms:check(before[room.pos]!=ctx.key(room,0.0),"Interior lighting remains a floor dependency")
	before=keys(ctx,rooms);c=common(rooms,power,hardware);c[5][0][2]=0.4;c[5][0][9]=false;ctx.prepare(c,occupied,power,rooms)
	for room in rooms:check((before[room.pos]!=ctx.key(room,0.0))==(room==rooms[0]),"Room light/bake state remains local")
	before=keys(ctx,rooms);c=common(rooms,power,hardware);c[6]+=1;ctx.prepare(c,occupied,power,rooms)
	for room in rooms:check(before[room.pos]!=ctx.key(room,0.0),"Layout revision dirties every floor")
	var snapshot:Array=ctx.key(rooms[0],0.0).duplicate(true);occupied[Vector2i(0,0)].ports.append("west")
	check(ctx.key(rooms[0],0.0)==snapshot,"Retained key immutable under nested input mutation")
	c=common(rooms,power,hardware);ctx.prepare(c,occupied,power,rooms)
	check(ctx.key(rooms[0],0.0)!=snapshot,"Nested structural mutation observed")
	rooms.pop_back();ctx.prepare(common(rooms,power,hardware),occupied,power,rooms)
	check(ctx.keys.size()==39,"Only current room keys retained")
	print("LOCAL_FLOOR_KEYS ",JSON.stringify({"checks":checks,"failures":failures}));quit(1 if failures else 0)
