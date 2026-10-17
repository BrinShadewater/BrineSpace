extends SceneTree
const NormalGrid=preload("res://scripts/grid_canvas.gd")
class Fixture:
	extends RefCounted
	var placed_rooms:Array=[]
	var occupied:Dictionary={}
class Grid extends NormalGrid:
	var fixture=Fixture.new()
	var reference:bool=false
	var sample_size:float=384.0
	var sample_frame:int=0
	func _ready():pass
	func _process(_delta):pass
	func _cell_size()->float:return sample_size
	func _uses_layered_art(room:Dictionary)->bool:return room.get("layered",false)
	func _render_ports(room:Dictionary,_main)->Array[Dictionary]:return room.ports
	func _door_has_connected_neighbor(_main,room:Dictionary,_neighbor:Vector2i,_offset:Vector2i)->bool:return room.connected
	func _door_frame_for_pair(_main,_a:Vector2i,_b:Vector2i,_known_connected:=false)->int:return sample_frame
	func _draw():
		draw_target=self
		if reference:
			reference_doors(fixture,true)
			reference_doors(fixture,false)
		else:
			var plan:Array=_legacy_door_plan(fixture)
			_draw_door_foregrounds(fixture,true,plan)
			_draw_door_foregrounds(fixture,false,plan)
	func reference_doors(main, underlay: bool = false) -> void:
		if door_texture == null:
			if not underlay:
				_draw_static_door_foregrounds(main)
			return
		if door_texture.get_width() <= 0 or door_texture.get_height() <= 0:
			if not underlay:
				_draw_static_door_foregrounds(main)
			return
		var cell_size: float = _cell_size()
		var drawn: Dictionary = {}
		for room in main.placed_rooms:
			for edge_port in _render_ports(room, main):
				var pos: Vector2i = edge_port.cell
				var side: String = edge_port.side
				var offset: Vector2i = _offset_from_side(side)
				var neighbor_pos: Vector2i = pos + offset
				if _uses_layered_art(room) or _uses_layered_art(main.occupied.get(neighbor_pos, {})):
					continue # The modular edge owns its frame; no second legacy door.
				var connected: bool = _door_has_connected_neighbor(main, room, neighbor_pos, offset)
				if connected and _is_duplicate_connected_door_side(side) and not _always_draw_room_doors(room):
					continue
				var key: String = "%s:%s" % [str(pos), side]
				if drawn.has(key):
					continue
				drawn[key] = true
				var edge_center: Vector2 = _door_edge_center(pos, side, cell_size)
				var frame_index: int = _door_frame_for_pair(main, pos, neighbor_pos) if connected else 0
				var source_rect: Rect2 = _door_source_rect(frame_index)
				var door_size: Vector2 = Vector2(cell_size * DOOR_DRAW_SIZE.x, cell_size * DOOR_DRAW_SIZE.y)
				var door_rotation: float = PI * 0.5 if side == "east" or side == "west" else 0.0
				draw_target.draw_set_transform(edge_center, door_rotation, Vector2.ONE)
				if underlay:
					_draw_door_floor_patch(door_size)
				_draw_door_texture_layer(source_rect, door_size, underlay)
				draw_target.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)

var failures:int=0
var pairs:int=0
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	print("ISOLATION_VERIFIED ",OS.get_user_data_dir())
	root.size=Vector2i(720,720)
	var viewports:Array=[];var grids:Array=[]
	for mode in range(2):
		var vp:=SubViewport.new();vp.size=Vector2i(720,720);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);viewports.append(vp)
		var grid:=Grid.new();grid.reference=mode==0;grid.position=Vector2(80.375,80.1875);grid.modulate=Color(.87,.94,1,.8)
		grid.door_texture=grid._load_png_texture("res://legacy/default/dooranimated.png")
		if grid.door_texture==null:push_error("Missing selected door art");quit(1);return
		vp.add_child(grid);grids.append(grid)
	for filtering in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
		for size in [96.0,384.0,521.25]:
			for frame in range(10):
				for connected in [false,true]:
					for layering in range(4):
						for grid in grids:
							grid.texture_filter=filtering;grid.sample_size=size;grid.sample_frame=frame
							var ports:Array[Dictionary]=[]
							for side in ["north","east","south","west","east"]:ports.append({"cell":Vector2i.ZERO,"side":side})
							var room:Dictionary={"id":"legacy","pos":Vector2i.ZERO,"ports":ports,"layered":layering&1!=0,"connected":connected}
							grid.fixture.placed_rooms=[room,room];grid.fixture.occupied.clear()
							for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:grid.fixture.occupied[offset]={"layered":layering&2!=0}
							grid.queue_redraw()
						await process_frame;await RenderingServer.frame_post_draw
						var a:Image=viewports[0].get_texture().get_image();var b:Image=viewports[1].get_texture().get_image();pairs+=1
						if a.get_data()!=b.get_data():
							failures+=1
							if failures==1:a.save_png("user://reference-failure.png");b.save_png("user://candidate-failure.png")
						if filtering==CanvasItem.TEXTURE_FILTER_LINEAR and size==384.0 and frame==5 and not connected and layering==0:b.save_png("user://accepted-sample.png")
	print("LEGACY_PLAN_RASTER pairs=",pairs," failures=",failures)
	for vp in viewports:vp.queue_free()
	await process_frame
	quit(1 if failures else 0)
