extends SceneTree
const Pool=preload("res://scripts/crew_texture_pool.gd")
const Solar=preload("res://rooms/full-wall-v1/solar_array_view.gd")
const Corridor=preload("res://rooms/underwater/corridor_surfaces.gd")
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func exercise() -> Array:
	var pool=Pool.new()
	var rooms:=[]
	for index in range(3):
		var room=Solar.new();room.embedded=true;room.hide()
		if index>0:room.set_meta("room_texture_pool",pool)
		root.add_child(room);rooms.append(room)
	for key in rooms[0].dressing.textures:
		var original:ImageTexture=rooms[0].dressing.textures[key]
		var shared:ImageTexture=rooms[1].dressing.textures[key]
		check(shared==rooms[2].dressing.textures[key],"Dressing shares identical storage")
		check(shared!=original,"Reference uses independent storage")
		check(shared.get_image().get_data()==original.get_image().get_data(),"Dressing exact pixel parity")
		check(shared.get_size()==original.get_size(),"Dressing dimensions preserved")
	var before:int=pool.stats.uploads
	var first=Corridor.load_sources(pool)
	var second=Corridor.load_sources(pool)
	var original=Corridor.load_sources()
	for index in range(first.size()):
		check(first[index]==second[index],"Corridor views share source")
		check(first[index].get_image().get_data()==original[index].get_image().get_data(),"Corridor exact pixel parity")
	check(pool.stats.uploads==before+2,"Only two corridor uploads")
	var weak:=[weakref(pool),weakref(first[0]),weakref(first[1])]
	for key in rooms[1].dressing.textures:weak.append(weakref(rooms[1].dressing.textures[key]))
	for room in rooms:room.free()
	return weak
func run():
	var weak=exercise()
	await process_frame
	check(weak.all(func(reference):return reference.get_ref()==null),"Scene owners release pool, lookup tables and shared images")
	print("ROOM IMAGE SHARING ","PASS" if failures==0 else "FAIL"," checks=",checks," failures=",failures)
	quit(0 if failures==0 else 1)
