extends SceneTree
const Art=preload("res://scripts/environment_art.gd")
class Clock extends RefCounted:
	var clock:=0.0
	func get_visual_time_seconds()->float:return clock
class Reference extends "res://scripts/grid_canvas.gd":
	var fake=Clock.new()
	var cell_pixels:=65.0
	var region:=Rect2()
	var part:="lines"
	func _ready():cull_room_drawing=false;set_process(false);mouse_filter=Control.MOUSE_FILTER_IGNORE
	func _process(_delta):pass
	func _get_main():return fake
	func _cell_size()->float:return cell_pixels
	func _view_rect(_main)->Rect2:return region
	func _draw():draw_target=self;_draw_underwater_depth(part)
class Candidate extends "res://scripts/grid_canvas.gd":
	var fake=Clock.new()
	var cell_pixels:=65.0
	var region:=Rect2()
	var part:="lines"
	func _ready():set_process(false);mouse_filter=Control.MOUSE_FILTER_IGNORE
	func _process(_delta):pass
	func _get_main():return fake
	func _cell_size()->float:return cell_pixels
	func _view_rect(_main)->Rect2:return region
	func _draw():draw_target=self;_draw_underwater_depth(part)
var pairs:=0
var failures:=0
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(400,300)
	var saved:Texture2D=Art.texture("water-wave")
	var atlas:=AtlasTexture.new();atlas.atlas=saved;atlas.region=Rect2(0,0,saved.get_width()*.75,saved.get_height())
	var shader:=ShaderMaterial.new();shader.shader=Shader.new();shader.shader.code="shader_type canvas_item; void vertex(){ VERTEX.y += 12.0; } void fragment(){ COLOR *= vec4(.8,.9,1.,.8); }"
	var parents:Array=[];var grids:Array=[];var views:Array=[]
	for i in range(2):
		var vp:=SubViewport.new();vp.size=Vector2i(400,300);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);views.append(vp)
		var clip:=Control.new();clip.size=Vector2(400,300);clip.clip_contents=true;vp.add_child(clip);parents.append(clip)
		var grid=Reference.new() if i==0 else Candidate.new();grid.size=Vector2(5000,5000);clip.add_child(grid);grids.append(grid)
	for texture in [saved,null,atlas]:
		Art.cache["water-wave"]=texture
		for filtering in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
			for material_mode in [0,1,2]:
				for cell_size in [16.7,65.375,120.25]:
					for view_origin in [Vector2(-30.125,-21.875),Vector2(49.3125,65.125),Vector2(1234.375,1357.25)]:
						for clock in [0.0,7.99,183.125]:
							for i in range(2):
								parents[i].texture_filter=filtering;parents[i].material=shader if material_mode==2 else null
								grids[i].material=shader if material_mode==1 else null;grids[i].use_parent_material=material_mode==2
								grids[i].fake.clock=clock;grids[i].cell_pixels=cell_size;grids[i].position=-view_origin;grids[i].region=Rect2(view_origin,Vector2(400,300));grids[i].modulate=Color(.83,.92,.88,.87);grids[i].queue_redraw()
							await process_frame;await RenderingServer.frame_post_draw;pairs+=1
							var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image()
							if a.get_data()!=b.get_data() or not a.get_used_rect().has_area():
								failures+=1
								if failures<=4:print("MISMATCH ",[texture,filtering,material_mode,cell_size,view_origin,clock]);a.save_png("user://reference-failure.png");b.save_png("user://candidate-failure.png")
							if pairs==1:a.save_png("user://reference.png");b.save_png("user://candidate.png")
	Art.cache["water-wave"]=saved
	FileAccess.open("user://results.json",FileAccess.WRITE).store_string(JSON.stringify({"pairs":pairs,"failures":failures}))
	for vp in views:vp.queue_free()
	await process_frame
	print("WAVE_CULLING ",pairs," pairs, ",failures," failures");quit(1 if failures else 0)
