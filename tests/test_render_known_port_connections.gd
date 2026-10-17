extends SceneTree
const Database=preload("res://scripts/room_database.gd")
const Main=preload("res://scripts/main.gd")
const Grid=preload("res://scripts/grid_canvas.gd")
var checks:int=0
var failures:int=0
func compare(grid,main,room:Dictionary,cell:Vector2i,side:String):
	var offset:Vector2i=grid._offset_from_side(side)
	var neighbor:Vector2i=cell+offset
	var expected:bool=grid._door_has_connected_neighbor(main,room,neighbor,offset)
	var actual:bool=grid._neighbor_connected_from_known_port(main,room,neighbor,offset)
	checks+=1
	if expected!=actual:
		failures+=1
		if failures<4:push_error("Known port mismatch "+str([room,main.occupied,cell,side]))
func _init():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	print("ISOLATION_VERIFIED ",OS.get_user_data_dir())
	var main=Main.new();var grid=Grid.new();var variants:Array=[]
	for id in Database.all_rooms():
		for q in range(4):
			var room:Dictionary=Database.get_room(str(id));room.pos=Vector2i.ZERO;room.rotation=q
			variants.append(room)
	for template in variants:
		var room:Dictionary=template.duplicate(true);room.pos=Vector2i(8,8)
		for port in grid._render_ports(room,main):
			var cell:Vector2i=port.cell;var side:String=port.side;var neighbor:Vector2i=cell+grid._offset_from_side(side)
			main.occupied.clear();compare(grid,main,room,cell,side)
			main.occupied[neighbor]=room;compare(grid,main,room,cell,side)
			for other_template in variants:
				var other:Dictionary=other_template.duplicate(true)
				# Match and mismatch every authored neighbor port, not merely its anchor.
				var candidates:Array=grid._render_ports(other,main)
				candidates.append({"cell":Vector2i(20,20),"side":"none"})
				for other_port in candidates:
					other.pos=neighbor-Vector2i(other_port.cell)
					other.erase("branch_owner");main.occupied[neighbor]=other
					compare(grid,main,room,cell,side)
					other.branch_owner=Vector2i(40,41);compare(grid,main,room,cell,side)
			# Sentinel fallback must retain main's default-door behavior.
			var sentinel:Dictionary=room.duplicate(true);sentinel.pos+=Vector2i(-1,-1)-cell
			for shifted in grid._render_ports(sentinel,main):
				var at:Vector2i=shifted.cell;main.occupied.clear();main.occupied[at+grid._offset_from_side(shifted.side)]=sentinel
				compare(grid,main,sentinel,at,shifted.side)
	main.free();grid.free()
	print("KNOWN_PORT_GEOMETRY checks=",checks," failures=",failures," variants=",variants.size())
	quit(1 if failures else 0)
