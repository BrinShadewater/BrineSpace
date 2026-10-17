extends Node2D
## Scene-owned command retention in original rock/selection/wreck/plant order.
const Rock = preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
const Batch = preload("res://scripts/rock_surface_batch.gd")
class Surface extends Node2D:
	var owner_canvas
	var meshes:Array=[]
	var drawn:Array=[]
	func _draw():
		drawn=meshes
		if drawn.size()==2:
			draw_mesh(drawn[0],null,Transform2D.IDENTITY,Color("18383e"))
			draw_mesh(drawn[1],owner_canvas.rock_view.texture(),Transform2D.IDENTITY,Color(.73,.85,.86))
var batch_enabled:=true
var surface:Surface
var surface_key:Array=[]
const Field = preload("res://scripts/wreck_field.gd")
const Plants = preload("res://scripts/seabed_glow.gd")
class Slot extends Node2D:
	var owner_canvas
	var kind := ""
	var cell := Vector2i(-1,-1)
	var key: Array = []
	func _draw(): owner_canvas.paint(self)
var rock_group := Node2D.new()
var wreck_group := Node2D.new()
var selection: Slot
var plants: Slot
var rocks := {}
var wrecks := {}
var game
var grid
var rock_view
var wreck_view
var cell_size := 0.0
var selected := Vector2i(-1,-1)
var cell_redraws := 0
var plant_redraws := 0
func _init():
	add_child(rock_group)
	surface=Surface.new();surface.owner_canvas=self;rock_group.add_child(surface)
	selection = make_slot(self,"selection")
	add_child(wreck_group)
	plants = make_slot(self,"plants")
func make_slot(parent: Node, kind: String, cell := Vector2i(-1,-1)) -> Slot:
	var slot := Slot.new()
	slot.owner_canvas=self;slot.kind=kind;slot.cell=cell
	parent.add_child(slot)
	return slot
func update_key(slot: Slot, key: Array):
	if slot.key!=key:
		slot.key=key.duplicate(true)
		slot.queue_redraw()
func submit(main, size: float, host, rock, wreck):
	game=main;grid=host;rock_view=rock;wreck_view=wreck
	cell_size=size;selected=main.selected_room_cell
	for entries in [rocks,wrecks]:
		for cell in entries.keys():
			if not main.wrecks.has(cell):
				entries[cell].hide();entries[cell].queue_free();entries.erase(cell)
	var index:=1
	var key:Array=[size,batch_enabled]
	for cell in main.wrecks:
		if Rock.is_rock(main.wrecks,cell):key.append([cell,Rock.connections(main.wrecks,cell)])
	if key!=surface_key:
		surface_key=key.duplicate(true)
		surface.meshes=Batch.build(main.wrecks,size) if batch_enabled else []
		surface.queue_redraw()
	for cell in main.wrecks:
		if not rocks.has(cell):rocks[cell]=make_slot(rock_group,"rock",cell)
		if not wrecks.has(cell):wrecks[cell]=make_slot(wreck_group,"wreck",cell)
		if rocks[cell].get_index()!=index:rock_group.move_child(rocks[cell],index)
		if wrecks[cell].get_index()!=index-1:wreck_group.move_child(wrecks[cell],index-1)
		index+=1
		var w: Dictionary=main.wrecks[cell]
		var visible:=Field.visible(main.wrecks,cell)
		var common: Array=[size,w.kind,w.progress,w.cleared,visible]
		update_key(rocks[cell],common+[Rock.connections(main.wrecks,cell),batch_enabled])
		update_key(wrecks[cell],common+[selected==cell])
	update_key(selection,[size,selected,Rock.is_rock(main.wrecks,selected)])
	update_key(plants,[size,Plants.spots(main)])
func paint(slot: Slot):
	if game==null:return
	var started: int=Time.get_ticks_usec() if grid!=null and grid.profile_draw else 0
	match slot.kind:
		"rock":rock_view.draw_into(slot,game.wrecks,cell_size,game.visual_time_seconds,Vector2i(-1,-1),false,[slot.cell],batch_enabled)
		"wreck":wreck_view.draw_into(slot,game.wrecks,cell_size,game.visual_time_seconds,selected,false,[slot.cell])
		"selection":Rock.draw_selection(slot,game.wrecks,cell_size,selected)
		"plants":Plants.draw_plants(slot,game,cell_size)
	if slot.kind=="plants":plant_redraws+=1
	else:cell_redraws+=1
	if started:
		var elapsed:=Time.get_ticks_usec()-started
		grid.draw_usec_since_read+=elapsed
		grid.draw_profile_usec["env_terrain_cells"]=int(grid.draw_profile_usec.get("env_terrain_cells",0))+elapsed
		grid.draw_profile_totals_usec["env_terrain_cells"]=int(grid.draw_profile_totals_usec.get("env_terrain_cells",0))+elapsed
