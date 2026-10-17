extends SceneTree
const Kelp=preload("res://assets/environment/upright-kelp-v1/upright_kelp_view.gd")
const NewKelp=Kelp
const Fronds=preload("res://scripts/ambient_fronds.gd")
const NewFronds=Fronds
const Settings=preload("res://scripts/title_settings.gd")
class Painter extends Node2D:
 var fn:Callable
 func _draw():fn.call(self)
# Baseline immediate polygons, preserving the pre-optimization strip topology.
func reference(c:CanvasItem,texture:Texture2D,at:Vector2,width:float,clock:float,phase:float,kelp:bool,height:float=0.0):
 var extent:Vector2=texture.get_size()/float(texture.get_width())*width if kelp else Vector2(width,height)
 var origin:Vector2=at-extent*Vector2(.5,.97) if kelp else at
 if Settings.reduced_motion or Settings.effects_quality==0:
  c.draw_texture_rect(texture,Rect2(origin,extent),false,Color(.59,.68,.66,.85));return
 var strips:int=17 if kelp else 6
 for row in range(strips):
  var a:float=float(row)/16.0*.92 if kelp else float(row)/6.0
  var b:float=(float(row+1)/16.0*.92 if row<16 else 1.0) if kelp else float(row+1)/6.0
  var x:float=Kelp.sway_offset(a,clock,phase) if kelp else Fronds.offset(a,clock,phase)
  var y:float=Kelp.sway_offset(b,clock,phase) if kelp else Fronds.offset(b,clock,phase)
  var top:=origin+Vector2(x*width,a*extent.y);var bottom:=origin+Vector2(y*width,b*extent.y)
  c.draw_polygon(PackedVector2Array([top,top+Vector2(width,0),bottom+Vector2(width,0),bottom]),PackedColorArray([Color(.59,.68,.66,.85)]),PackedVector2Array([Vector2(0,a),Vector2(1,a),Vector2(1,b),Vector2(0,b)]),texture)
func _init():call_deferred("run")
func run():
 if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
 root.size=Vector2i(400,400)
 var views:Array=[];var painters:Array=[];var a=Kelp.new();var b=NewKelp.new();a.prepare();b.prepare()
 for i in range(2):
  var view:=SubViewport.new();view.size=Vector2i(400,400);view.transparent_bg=true;view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);views.append(view)
  var painter=Painter.new();view.add_child(painter);painters.append(painter)
 if "--wet-mirror" in OS.get_cmdline_user_args():
  var flood:=ShaderMaterial.new();flood.shader=preload("res://scripts/flood_submersion.gdshader");flood.set_shader_parameter("waterline_y",175.0);flood.set_shader_parameter("world_scale",.73);flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
  for painter in painters:
   painter.material=flood;painter.position=Vector2(400,0);painter.scale=Vector2(-1,1)
 var pairs:=0;var failures:=0;var nonblank:=0
 print("QUAD ",Geometry2D.triangulate_polygon(PackedVector2Array([Vector2(0,0),Vector2(1,0),Vector2(1,1),Vector2(0,1)])))
 var sources:Array=["res://assets/environment/seabed-refresh-v1/runtime/ribbon-kelp.png","res://assets/environment/habitat-refresh-v1/runtime/sea-fans.png","res://assets/environment/seabed-life-refresh-v1/runtime/hydroids.png"]
 var source_index:=0
 for id in Kelp.SOURCES:
  var selected:Texture2D=preload("res://scripts/safe_image.gd").raw_texture(sources[source_index]);source_index+=1
  for clock in [0.0,1.375,7.99,8.0]:
   for width in [35.5,77.25,120.0]:
    for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
     for reduced in [false,true]:
      Settings.reduced_motion=reduced;Settings.effects_quality=1
      for kind in ["kelp","fronds"]:
       for i in range(2):
        var painter=painters[i];painter.texture_filter=filter
        if kind=="kelp":
         var renderer=a if i==0 else b
         if i==0:painter.fn=func(c):reference(c,a.textures[id],Vector2(200.375,350.125),width,clock,2.31,true)
         else:painter.fn=func(c):renderer.draw_swaying_asset(c,id,Vector2(200.375,350.125),width,clock,2.31)
        else:
         var texture:Texture2D=selected;var rect:=Rect2(Vector2(170.375,50.125),Vector2(width,280.5))
         if i==0:painter.fn=func(c):reference(c,texture,rect.position,rect.size.x,clock,2.31,false,rect.size.y)
         else:painter.fn=func(c):NewFronds.draw(c,texture,rect,clock,2.31,Color(.59,.68,.66,.85))
        painter.queue_redraw()
       await process_frame;await process_frame;await RenderingServer.frame_post_draw
       var original:Image=views[0].get_texture().get_image();var candidate:Image=views[1].get_texture().get_image();pairs+=1
       if original.get_used_rect().has_area():nonblank+=1
       if not original.get_used_rect().has_area() or original.get_data()!=candidate.get_data():
        failures+=1
        if failures<=4:print("MISMATCH ",id," ",kind," ",clock," ",width," ",filter," ",reduced);original.save_png("user://original.png");candidate.save_png("user://candidate.png")
 FileAccess.open("user://results.json",FileAccess.WRITE).store_string(JSON.stringify({"pairs":pairs,"failures":failures,"nonblank":nonblank}))
 for view in views:view.queue_free()
 await process_frame
 print("STRIPS ",pairs," comparisons ",failures," failures nonblank ",nonblank);quit(1 if failures else 0)
