extends SceneTree
var canvas
var material=ShaderMaterial.new()
func _init():call_deferred("run")
func make_shader(code:String,counting:=false)->Shader:
 if counting:
  for anchor in ["float illumination=0.0;","vec2 point=mix(lights[i].xy,world,float(step)/24.0);","COLOR=vec4(water,clamp(opacity+haze*.035,.12,.995));"]:
   assert(code.count(anchor)==1,"Shadow-work instrumentation anchor changed: "+anchor)
  code=code.replace("float illumination=0.0;","float illumination=0.0; float qa_steps=0.0;")
  code=code.replace("vec2 point=mix(lights[i].xy,world,float(step)/24.0);","qa_steps+=1.0; vec2 point=mix(lights[i].xy,world,float(step)/24.0);")
  code=code.replace("COLOR=vec4(water,clamp(opacity+haze*.035,.12,.995));","COLOR=vec4(qa_steps/1104.0,0.0,0.0,1.0);")
 var shader=Shader.new();shader.code=code;return shader
func capture(shader:Shader)->Image:
 material.shader=shader
 canvas.queue_redraw()
 for i in 4:await process_frame
 await RenderingServer.frame_post_draw
 return root.get_texture().get_image()
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 root.size=Vector2i(320,240);root.content_scale_mode=Window.CONTENT_SCALE_MODE_DISABLED;root.content_scale_size=Vector2i.ZERO;root.set_disable_input(true)
 preload("res://tools/release_benchmark.gd").configure_test_window(root)
 canvas=ColorRect.new();canvas.size=Vector2(320,240);canvas.color=Color.WHITE;canvas.material=material;root.add_child(canvas)
 var terrain=Image.create(40,40,false,Image.FORMAT_RGBA8);terrain.fill(Color(0,1,0,1))
 var terrain_texture=ImageTexture.create_from_image(terrain)
 var positions=PackedVector4Array();var directions=PackedVector4Array()
 for i in 48:positions.append(Vector4(2,1,10,1.0-float(i)/96.0));directions.append(Vector4(0,1,0,0))
 var source=FileAccess.get_file_as_string("res://scripts/underwater_fog.gdshader")
 material.shader=make_shader(source,true)
 for pair in [["terrain",terrain_texture],["lights",positions],["directions",directions],["light_count",48],["cell_size",80.0],["clock",7.0]]:material.set_shader_parameter(pair[0],pair[1])
 var counted=await capture(material.shader)
 var maximum=0
 for y in counted.get_height():
  for x in counted.get_width():maximum=maxi(maximum,counted.get_pixel(x,y).r8)
 print("SHADOW_STEP_RED_MAX ",maximum," (one useful lamp bound <=8)")
 if maximum==0 or maximum>8:push_error("Redundant shadow marches: weaker overlapping lamps exceed one useful lamp's work");quit(1);return
 print("SHADOW_PRUNING_WORK_BOUND_PASS")
 var reference=FileAccess.get_file_as_string("res://tests/fixtures/underwater_fog_reference.gdshader.txt")
 var random=RandomNumberGenerator.new();random.seed=927335
 var total=0
 for case in 16:
  terrain.fill(Color(0,1,0,1))
  if case>0:
   for y in 6:
    for x in 8:
     if random.randf()<0.3:terrain.set_pixel(x,y,Color(1,random.randf(),random.randf()*0.55,1))
  terrain_texture.update(terrain)
  positions=PackedVector4Array();directions=PackedVector4Array()
  for i in 48:
   var angle=random.randf_range(0,TAU)
   positions.append(Vector4(random.randf_range(0,6),random.randf_range(0,5),random.randf_range(0.4,4),random.randf()))
   directions.append(Vector4(cos(angle),sin(angle),0,0))
  material.set_shader_parameter("lights",positions);material.set_shader_parameter("directions",directions)
  material.set_shader_parameter("light_count",[0,1,12,24,48,48,48,48][case % 8])
  material.set_shader_parameter("cell_size",[48,64,80,120,192,80,80,80][case % 8])
  material.set_shader_parameter("clock",case*7.125)
  material.set_shader_parameter("motion",0.0 if case % 8==6 else 1.0)
  material.set_shader_parameter("shafts",0.0 if case>=8 else 0.15)
  material.set_shader_parameter("caustic_light",0.0 if case>=12 else 0.2)
  material.set_shader_parameter("depth_tint",0.0 if case>=12 else 0.3)
  material.set_shader_parameter("caustics_tex",terrain_texture)
  material.set_shader_parameter("use_caustics_tex",case>=8)
  var a=await capture(make_shader(reference))
  var b=await capture(make_shader(source))
  var left:PackedByteArray=a.get_data();var right:PackedByteArray=b.get_data()
  var count=0;var maximum_difference=0
  for i in left.size():
   if left[i]!=right[i]:count+=1;maximum_difference=maxi(maximum_difference,absi(int(left[i])-int(right[i])))
  print("FOG_PIXELS case=",case," different_channels=",count," max_difference=",maximum_difference)
  if count>0:push_error("Fog pixels changed");quit(1);return
  total+=left.size()
 print("FOG_PIXEL_PARITY_PASS channels=",total);quit()
