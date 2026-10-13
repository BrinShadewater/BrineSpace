extends SceneTree
const Slot=preload("res://scripts/large_room_canvas.gd")
const Studio=preload("res://rooms/large-rooms/studio_view.gd")
const Views={"moonbay":preload("res://rooms/large-rooms/moonbay.gd"),"hydroponics_farm":preload("res://rooms/large-rooms/hydroponics_farm.gd"),"storage_depot":preload("res://rooms/large-rooms/storage_depot.gd"),"tidal_power_plant":preload("res://rooms/large-rooms/tidal_power_plant.gd")}
const NormalGrid=preload("res://scripts/grid_canvas.gd")
class Grid extends NormalGrid:
	func _ready():pass
	func _process(_delta):pass
	func _draw():pass
	var occupied:Dictionary={}
	func _get_main():return self
class Reference extends Node2D:
	var rooms:Array=[]
	var rects:Array=[]
	var grid
	var offline:=false
	var clock:=.375
	func _draw():
		Studio.hide_wet_equipment(self,grid.occupied)
		for i in rooms.size():
			var room:Dictionary=rooms[i]
			Views[room.id].draw(self,room,rects[i])
			Studio.draw_live(self,room,rects[i],clock,true,offline)
			if offline:draw_rect(rects[i],Color(.05,.02,.03,.35))
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(720,720)
	var retention_grid:=Grid.new();root.add_child(retention_grid);var retention_host:=Node2D.new();root.add_child(retention_host)
	for id in ["hydroponics_farm","storage_depot"]:
		var held=Slot.new();retention_host.add_child(held)
		var state:Dictionary={"id":id,"rotation":0,"ports":[],"port_open":[],"raised_walls":true,"machine_clock":0.0,"tidal_chamber":{"water":0.0,"rotor_angle":0.0,"spinning":false}}
		var bounds:=Rect2(0,0,384,384)
		held.configure(retention_grid,Views[id],state,state,bounds,0.0,true,false)
		await process_frame;await RenderingServer.frame_post_draw
		var before:int=held.base.redraws
		check(before>0,"Retained base actually draws "+id)
		state.machine_clock=1.0;held.configure(retention_grid,Views[id],state,state,bounds,1.0,true,false)
		await process_frame;await RenderingServer.frame_post_draw
		check(held.base.redraws==before and held.base.hits>0,"Generic clock preserves complete base commands "+id)
		state.raised_walls=false;held.configure(retention_grid,Views[id],state,state,bounds,1.0,true,false)
		await process_frame;await RenderingServer.frame_post_draw
		check(held.base.redraws>before,"Wall state invalidates base "+id)
		before=held.base.redraws
		if id=="tidal_power_plant":state.tidal_chamber={"water":0.7,"rotor_angle":0.45,"spinning":true}
		else:state.water_level=0.5
		held.configure(retention_grid,Views[id],state,state,bounds,1.0,true,false)
		await process_frame;await RenderingServer.frame_post_draw
		check(held.base.redraws>before,"Water/chamber state invalidates base "+id)
		held.queue_free();await process_frame
	retention_grid.queue_free();retention_host.queue_free();await process_frame

	FileAccess.open("user://context.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
	print("STATIC_LARGE_BASE ",checks," checks ",failures," failures");quit(1 if failures else 0)
