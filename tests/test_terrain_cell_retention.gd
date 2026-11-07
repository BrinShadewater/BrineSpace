extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
const Field=preload("res://scripts/wreck_field.gd")
class GameData extends RefCounted:
	var wrecks:=Field.initial()
	var selected_room_cell:=Vector2i(16,20)
	var visual_time_seconds:=1.23
	var placed_rooms:Array=[{"pos":Vector2i(20,20)}]
	var occupied:Dictionary={Vector2i(20,20):true}
class TerrainPass extends Node2D:
	var grid=Grid.new()
	var game
	var size:=24.3
	func _draw():
		grid.draw_target=self
		grid._draw_environment_layer(game,size,Grid.Env.STATIC_TERRAIN)
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/").simplify_path()!=expected or DisplayServer.get_name()=="headless":push_error("Native isolated profile required");quit(2);return
	for size in [16.0,24.3]:
		for offset in [0.0,0.5]:
			for filtering in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
				var game=GameData.new();var views:=[];var passes:=[]
				for mode in range(2):
					var viewport:=SubViewport.new();viewport.size=Vector2i(512,300);viewport.transparent_bg=true
					viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport);views.append(viewport)
					var layer:=TerrainPass.new();layer.game=game;layer.size=size
					layer.position=-Vector2(10,16)*size+Vector2.ONE*offset;layer.texture_filter=filtering
					layer.grid.retain_terrain_cells=mode==1
					viewport.add_child(layer);passes.append(layer)
				for step in range(34):
					game.selected_room_cell=Vector2i(16,20) if step<13 else Vector2i(18,18)
					if step<20:game.wrecks[game.selected_room_cell].progress=float(step)*0.71
					if step==20:game.wrecks[Vector2i(16,20)].cleared=true
					if step==21:game.wrecks[Vector2i(12,21)].cleared=true
					if step==22:game.wrecks[Vector2i(18,18)].cleared=true
					if step==23:game.wrecks[Vector2i(16,20)].cleared=false
					if step==24:game.wrecks[Vector2i(16,20)].buried=true
					if step==25:game.wrecks[Vector2i(16,20)].buried=false
					if step==26:game.wrecks[Vector2i(15,16)]={"kind":"basalt","progress":1.0,"cleared":false,"active":true}
					if step==27:game.wrecks.erase(Vector2i(15,16))
					if step==28:game.wrecks=game.wrecks.duplicate(true)
					if step==29:
						for layer in passes:layer.scale=Vector2.ONE*1.12;layer.position+=Vector2(17,-9)
					if step==30:passes[1].grid.retain_terrain_cells=false
					if step==31:passes[1].grid.retain_terrain_cells=true
					if step==32:game.wrecks.clear()
					for layer in passes:layer.queue_redraw()
					await frame()
					var a:Image=views[0].get_texture().get_image()
					var b:Image=views[1].get_texture().get_image()
					check(a.get_data()==b.get_data(),"Exact integrated terrain, including first frame: %s/%s/%d/%d"%[size,offset,filtering,step])
					if step==18 and size==24.3 and offset==0 and filtering==CanvasItem.TEXTURE_FILTER_LINEAR:b.save_png("user://terrain-integrated.png")
					if step==33:
						var content=passes[1].grid.terrain_content
						check(content.rocks.is_empty() and content.wrecks.is_empty(),"Removed cells release slots")
				var dependency_game=GameData.new()
				var prior_key:Array=passes[1].grid._environment_terrain_key(dependency_game,size)
				dependency_game.wrecks[Vector2i(16,20)].buried=true
				check(passes[1].grid._environment_terrain_key(dependency_game,size)!=prior_key,"Buried visibility invalidates the actual pass")
				var held:WeakRef=weakref(passes[1].grid.terrain_content)
				var grids:=[passes[0].grid,passes[1].grid]
				for viewport in views:viewport.queue_free()
				for unused in range(10):
					if held.get_ref()==null:break
					await process_frame
				check(held.get_ref()==null,"Scene exit releases terrain host")
				for grid in grids:grid.free()
	print("TERRAIN CELL RETENTION: %d checks; %d failures"%[checks,failures])
	quit(1 if failures else 0)
