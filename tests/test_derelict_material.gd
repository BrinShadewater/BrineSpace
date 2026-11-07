extends SceneTree
var failures:=0
func _init():call_deferred("run")
func check(ok: bool, message: String):
	if not ok:failures+=1;push_error(message)
func capture(view: SubViewport) -> Image:
	await process_frame
	await RenderingServer.frame_post_draw
	return view.get_texture().get_image()
func run():
	if DisplayServer.get_name()=="headless":
		print("SKIP: derelict material requires native rendering");quit(2);return
	var view:=SubViewport.new()
	view.size=Vector2i(320,320);view.transparent_bg=true
	view.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	root.add_child(view)
	var sprite:=Sprite2D.new()
	sprite.texture=preload("res://scripts/safe_image.gd").raw_texture("res://legacy/default/assets/material-polish-cryo-v1/cryo-equipment.png")
	sprite.centered=false;sprite.position=Vector2(24,24)
	sprite.scale=Vector2.ONE*240.0/sprite.texture.get_width()
	sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	view.add_child(sprite)
	var plain: Image=await capture(view)
	var material:=ShaderMaterial.new()
	material.shader=preload("res://scripts/derelict_material.gdshader")
	sprite.material=material
	var aged: Image=await capture(view)
	var changed:=0;var alpha_changes:=0
	for y in range(320):
		for x in range(320):
			var a:=plain.get_pixel(x,y);var b:=aged.get_pixel(x,y)
			if a.a!=b.a:alpha_changes+=1
			if a!=b:changed+=1
	check(alpha_changes==0,"Material preserves every source alpha pixel")
	check(changed>1000,"Equipment surfaces receive visible material wear")
	var repeated: Image=await capture(view)
	check(aged.get_data()==repeated.get_data(),"Static wear does not animate while paused")
	sprite.position+=Vector2(8,8)
	var moved: Image=await capture(view)
	check(aged.get_region(Rect2i(16,16,264,264)).get_data()==moved.get_region(Rect2i(24,24,264,264)).get_data(),"Wear remains attached to source through camera translation")
	sprite.position=Vector2(24,24)
	material.set_shader_parameter("room_light",0.0)
	var unlit: Image=await capture(view)
	var darker:=0;var unlit_alpha_changes:=0
	for y in range(320):
		for x in range(320):
			var a:=aged.get_pixel(x,y);var b:=unlit.get_pixel(x,y)
			if a.a!=b.a:unlit_alpha_changes+=1
			if b.r+b.g+b.b<a.r+a.g+a.b:darker+=1
	check(darker>1000 and unlit_alpha_changes==0,"Lights-off material darkens equipment while preserving alpha")
	sprite.material=null;sprite.position=Vector2(24,24)
	var restored: Image=await capture(view)
	check(plain.get_data()==restored.get_data(),"Removing derelict material exactly restores original artwork")
	print("DERELICT MATERIAL: %s changed=%d alpha_changes=%d failures=%d"%["PASS" if failures==0 else "FAIL",changed,alpha_changes,failures])
	quit(1 if failures else 0)
