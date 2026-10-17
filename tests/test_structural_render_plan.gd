extends SceneTree
const Database=preload("res://scripts/room_database.gd")
const Main=preload("res://scripts/main.gd")
const Door=preload("res://rooms/doors/department_door.gd")
const Store=preload("res://scripts/room_layout_store.gd")
class Grid extends "res://scripts/grid_canvas.gd":
	func _ready():pass
	func _process(_delta):pass
	func _draw():pass
var checks:=0
func check(ok:bool,label:String)->bool:
	checks+=1
	if not ok:push_error(label);quit(1);return false
	return true
func expected(grid,main)->Dictionary:
	var rows:Array=[];var nursery:Dictionary={};var connections:Dictionary={}
	for room in grid.static_draw_rooms:
		var sides:Array=[];var omitted:Array=[];var connected_sides:Array=[]
		for side in range(4):
			var offset:Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][side]
			var linked:bool=grid._door_has_connected_neighbor(main,room,room.pos+offset,offset)
			connected_sides.append(linked)
			if linked:sides.append(side)
			if main.occupied.has(room.pos+offset) and grid._uses_layered_art(main.occupied[room.pos+offset]) and not grid._is_narrow_corridor(main.occupied[room.pos+offset]) and side in [0,3]:omitted.append(side)
		if room.get("size",Vector2i.ONE)==Vector2i.ONE:nursery[room.pos]=[sides,omitted,connected_sides]
		var ports:Array=[]
		for port in grid._render_ports(room,main):
			var pos:Vector2i=port.cell;var side:String=port.side;var offset:Vector2i=grid._offset_from_side(side);var neighbor:Vector2i=pos+offset
			var edge:=Vector3i(mini(pos.x,neighbor.x),mini(pos.y,neighbor.y),0 if offset.x!=0 else 1)
			if not connections.has(edge):connections[edge]=grid._neighbor_connected_from_known_port(main,room,neighbor,offset) if grid.reuse_known_port_connections else grid._door_has_connected_neighbor(main,room,neighbor,offset)
			var linked:bool=connections[edge]
			if linked and side in ["north","west"]:continue
			if not linked and (main.occupied.has(neighbor) or side not in main.get_room_doors(room)):continue
			var other:Dictionary=main.occupied.get(neighbor,room)
			if not grid._uses_layered_art(room) and not grid._uses_layered_art(other):continue
			ports.append([pos,side,neighbor,linked,Door.pair_variant(room,other),grid._is_narrow_corridor(room) or grid._is_narrow_corridor(other)])
		rows.append(ports)
	return {"doors":rows,"nursery":nursery}
func verify(grid,main,label:String)->bool:
	var want:Dictionary=expected(grid,main)
	var got:Dictionary=grid.call("_structural_render_plan",main)
	return check(got==want,"Exact structural plan "+label)
func _init():call_deferred("run")
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var main=Main.new();var grid:Variant=Grid.new()
	if not check(grid.has_method("_structural_render_plan"),"Missing structural render plan API"):main.free();grid.free();return
	Store.prime()
	var cases:Array=[]
	for id in Database.all_rooms():
		for rotation in range(4):
			var room:Dictionary=Database.get_room(str(id));room.pos=Vector2i(8,8);room.rotation=rotation;cases.append(room)
	for room in cases:
		grid.static_draw_rooms=[room];main.occupied={room.pos:room}
		for port in grid._render_ports(room,main):
			var offset:Vector2i=grid._offset_from_side(port.side)
			var other:Dictionary=Database.get_room("reactor");other.pos=port.cell+offset;other.rotation=0
			main.occupied[other.pos]=other
			if not verify(grid,main,"actual port neighbor"):return
			other.branch_owner=Vector2i(31,32)
			if not verify(grid,main,"actual port branch"):return
			main.occupied.erase(other.pos)
		for side in range(4):
			var offset:Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][side]
			var other:Dictionary=Database.get_room("reactor");other.pos=room.pos+offset;other.rotation=side
			main.occupied[other.pos]=other
			if not verify(grid,main,"neighbor"):return
			other.branch_owner=Vector2i(31,32)
			if not verify(grid,main,"branch mutation"):return
			other.erase("branch_owner");other.rotation=(side+1)%4
			if not verify(grid,main,"rotation mutation"):return
			main.occupied.erase(other.pos)
			if not verify(grid,main,"remove neighbor"):return
		if room.has("ports"):
			room.ports.append({"cell":Vector2i.ZERO,"side":"north"})
			if not verify(grid,main,"in-place ports"):return
		room.size=Vector2i(2,2);room.ports=[]
		if not verify(grid,main,"empty explicit footprint"):return
		room.erase("ports");room.erase("size")
		if not verify(grid,main,"missing ports and size"):return
		Store.revision+=1
		if not verify(grid,main,"layout revision"):return
	# Order changes and dictionary replacement must not retain room references.
	grid.static_draw_rooms=cases.slice(0,12)
	main.occupied={}
	for i in range(grid.static_draw_rooms.size()):
		grid.static_draw_rooms[i]=grid.static_draw_rooms[i].duplicate(true);grid.static_draw_rooms[i].pos=Vector2i(i,3);main.occupied[Vector2i(i,3)]=grid.static_draw_rooms[i]
	if not verify(grid,main,"multiple rooms"):return
	grid.static_draw_rooms.reverse()
	if not verify(grid,main,"drawing order"):return
	# Replacing room dictionaries must not leave references to an older world.
	for i in range(grid.static_draw_rooms.size()):
		var room:Dictionary=grid.static_draw_rooms[i].duplicate(true)
		grid.static_draw_rooms[i]=room;main.occupied[room.pos]=room
	if not verify(grid,main,"dictionary replacement"):return
	var builds:int=grid.structural_builds
	main.occupied[Vector2i(10000,10000)]={"id":"reactor","pos":Vector2i(10000,10000),"rotation":0}
	if not verify(grid,main,"unrelated off-screen room"):return
	if not check(grid.structural_builds==builds,"Off-screen room does not invalidate visible plan"):return
	grid.static_draw_rooms[0].branch_owner=Vector2i(31,33)
	if not verify(grid,main,"source branch mutation"):return
	var reactor:Dictionary=Database.get_room("reactor");reactor.pos=Vector2i(5,5);reactor.rotation=0
	var life:Dictionary=Database.get_room("life_support");life.pos=Vector2i(6,5);life.rotation=0
	grid.static_draw_rooms=[reactor,life];main.occupied={reactor.pos:reactor,life.pos:life}
	if not verify(grid,main,"style baseline"):return
	var Painted=load("res://rooms/doors/painted_door.gd")
	var asset:String=Painted.room_assets.get("reactor","room-reactor")
	Store.data={asset+"/0":{"door/style":"life_support"}}
	if not verify(grid,main,"layout dictionary replacement without revision"):return
	Store.reuse_layout_store=false
	Store.data[asset+"/0"]["door/style"]="engineering"
	if not verify(grid,main,"uncached in-place style mutation"):return
	Store.reuse_layout_store=true
	main.free();grid.free()
	FileAccess.open("user://result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":0,"variants":cases.size()}))
	print("STRUCTURAL_PLAN ",checks," checks, 0 failures");quit()
