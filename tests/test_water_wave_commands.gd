extends SceneTree
const Art=preload("res://scripts/environment_art.gd")
class Clock extends RefCounted:
 var clock:=0.0
 func get_visual_time_seconds()->float:return clock
class Original extends "res://scripts/grid_canvas.gd":
 var fake=Clock.new()
 var cell_pixels:=65.0
 var part:="lines"
 var range_start:=Vector2i(-1,-1)
 var range_end:=Vector2i(1,1)
 func _ready():use_direct_wave_commands=false;set_process(false);mouse_filter=Control.MOUSE_FILTER_IGNORE
 func _process(_delta:float):pass
 func _get_main():return fake
 func _view_rect(_main)->Rect2:return Rect2(-100000,-100000,200000,200000)
 func _cell_size()->float:return cell_pixels
 func _visible_cell_range(_main,_size:float,_static_layer:=false)->Array:return [range_start,range_end]
 func _draw():
  draw_target=self;_draw_underwater_depth(part)
  draw_rect(Rect2(10,160,8,8),Color(.8,.2,.1,1))
class Candidate extends "res://scripts/grid_canvas.gd":
 var fake=Clock.new()
 var cell_pixels:=65.0
 var part:="lines"
 var range_start:=Vector2i(-1,-1)
 var range_end:=Vector2i(1,1)
 func _ready():set_process(false);mouse_filter=Control.MOUSE_FILTER_IGNORE
 func _process(_delta:float):pass
 func _get_main():return fake
 func _view_rect(_main)->Rect2:return Rect2(-100000,-100000,200000,200000)
 func _cell_size()->float:return cell_pixels
 func _visible_cell_range(_main,_size:float,_static_layer:=false)->Array:return [range_start,range_end]
 func _draw():
  draw_target=self;_draw_underwater_depth(part)
  draw_rect(Rect2(10,160,8,8),Color(.8,.2,.1,1))
func _init():call_deferred("run")
func run():
 if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
 root.size=Vector2i(400,400)
 var saved:Texture2D=Art.texture("water-wave");var atlas:=AtlasTexture.new();atlas.atlas=saved;atlas.region=Rect2(0,0,saved.get_width()*.75,saved.get_height())
 var views:Array=[];var grids:Array=[]
 for i in range(2):
  var view:=SubViewport.new();view.size=Vector2i(400,400);view.transparent_bg=true;view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);views.append(view)
  var grid=Original.new() if i==0 else Candidate.new();view.add_child(grid);grids.append(grid)
 assert(saved is ImageTexture)
 assert(not grids[0].use_direct_wave_commands and grids[1].use_direct_wave_commands)
 var flood:=ShaderMaterial.new();flood.shader=preload("res://scripts/flood_submersion.gdshader");flood.set_shader_parameter("waterline_y",170.0);flood.set_shader_parameter("world_scale",.73);flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
 var pairs:=0;var failures:=0
 for texture in [saved,null,atlas]:
  Art.cache["water-wave"]=texture
  for part in ["lines","rects","all"]:
   for cell_size in [65.375,120.25]:
    for clock in [0.0,7.99]:
     for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
      for mirrored in [false,true]:
       for wet in [false,true]:
        for grid in grids:
         grid.fake.clock=clock;grid.cell_pixels=cell_size;grid.part=part;grid.position=Vector2(150.375,120.125);grid.scale=Vector2(-.85 if mirrored else .85,.85);grid.texture_filter=filter;grid.material=flood if wet else null;grid.modulate=Color(.83,.92,.88,.87);grid.queue_redraw()
        await process_frame;await process_frame;await RenderingServer.frame_post_draw
        var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image();pairs+=1
        if a.get_data()!=b.get_data() or not a.get_used_rect().has_area():
         failures+=1
         if failures<=4:print("MISMATCH ",texture," ",part," ",cell_size," ",clock," ",filter," ",mirrored," ",wet)
        if pairs==1:
         # Exclude the transform-restoration marker: the actual wave must be visible.
         assert(a.get_region(Rect2i(0,0,400,245)).get_used_rect().has_area())
         assert(b.get_region(Rect2i(0,0,400,245)).get_used_rect().has_area())
         a.save_png("user://original.png");b.save_png("user://candidate.png")
 Art.cache["water-wave"]=saved
 FileAccess.open("user://results.json",FileAccess.WRITE).store_string(JSON.stringify({"pairs":pairs,"failures":failures}))
 for view in views:view.queue_free()
 await process_frame
 print("GRID WAVES ",pairs," comparisons ",failures," failures");quit(1 if failures else 0)
