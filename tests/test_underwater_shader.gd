extends SceneTree
var failures:=0
var viewport: SubViewport
var fog: Node2D
var material:=ShaderMaterial.new()
class Fog extends Node2D:
	func _draw(): draw_rect(Rect2(0,0,640,384),Color.WHITE)
func _init(): call_deferred("run")
func check(ok: bool,message: String):
	if not ok: failures+=1;push_error(message)
func capture() -> Image:
	fog.queue_redraw()
	for i in range(2): await process_frame
	await RenderingServer.frame_post_draw
	return viewport.get_texture().get_image()
func run():
	viewport=SubViewport.new();viewport.size=Vector2i(640,384);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var background:=ColorRect.new();background.color=Color(.55,.65,.6);background.size=Vector2(640,384);viewport.add_child(background)
	fog=Fog.new();material.shader=load("res://scripts/underwater_fog.gdshader");fog.material=material;viewport.add_child(fog)
	var mask:=Image.create(40,40,false,Image.FORMAT_RGBA8);mask.fill(Color.BLACK)
	var texture:=ImageTexture.create_from_image(mask)
	material.set_shader_parameter("terrain",texture);material.set_shader_parameter("cell_size",128.0)
	var lights:=PackedVector4Array();var directions:=PackedVector4Array();lights.resize(48);directions.resize(48)
	lights[0]=Vector4(1,1.5,3.5,1);directions[0]=Vector4(1,0,0,0)
	material.set_shader_parameter("lights",lights);material.set_shader_parameter("directions",directions);material.set_shader_parameter("light_count",1)
	var open:=await capture()
	check(open.get_pixel(230,192).get_luminance()>open.get_pixel(26,192).get_luminance()+.08,"Beam follows heading, not circular reveal")
	mask.set_pixel(2,1,Color.RED);texture.update(mask)
	var blocked:=await capture()
	check(open.get_pixel(384,192).get_luminance()>blocked.get_pixel(384,192).get_luminance()+.05,"Solid terrain casts a native shader shadow")
	mask.set_pixel(2,1,Color.BLACK);texture.update(mask)
	var excavated:=await capture()
	check(open.get_data()==excavated.get_data(),"Excavation restores exact open beam")
	check((await capture()).get_data()==excavated.get_data(),"Frozen visual clock is pixel stable")
	material.set_shader_parameter("clock",8.0)
	check((await capture()).get_data()!=excavated.get_data(),"Haze drifts with visual clock")
	material.set_shader_parameter("light_count",0)
	var dark:=await capture()
	mask.set_pixel(3,1,Color.GREEN);texture.update(mask)
	var remembered:=await capture()
	check(remembered.get_pixel(448,192).get_luminance()>dark.get_pixel(448,192).get_luminance()+.015,"Survey remains faintly mapped after lights leave")
	check(remembered.get_pixel(448,192).get_luminance()<open.get_pixel(300,192).get_luminance(),"Survey memory is dimmer than active illumination")
	print("UNDERWATER SHADER: %s failures=%d"%["PASS" if failures==0 else "FAIL",failures]);quit(1 if failures else 0)
