extends SceneTree
const Content=preload("res://scripts/room_content_canvas.gd")
const Library=preload("res://scripts/room_asset_library.gd")
class Context extends RefCounted:
	var painter:CanvasItem
	var operating:=false
	var machine_clock:=0.0
	var actor:=Vector2.ZERO
	var external_actor_texture:Texture2D
	func props_rebuilt_each_configure()->bool:return true
	func prop_visual_bounds(prop:Dictionary)->Rect2:return prop.rect if prop.has("portable_view") else Library.bounds(prop)
class Reference extends Node2D:
	var painter:CanvasItem=self
	var operating:=false
	var machine_clock:=0.0
	var prop:Dictionary={}
	func _draw():
		if prop.is_empty() or prop.get("layout_hidden",false):return
		draw_set_transform(Vector2(160.375,190.125))
		Library.draw(self,prop)
var checks:=0
var failures:=0
var pairs:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(320,320)
	var image:=Image.create(64,64,false,Image.FORMAT_RGBA8)
	for y in range(64):
		for x in range(64):image.set_pixel(x,y,Color(float(x)/63,float(y)/63,.4,float((x+y)%4)/3))
	var texture:=ImageTexture.create_from_image(image)
	var reg:Dictionary={"width":64,"height":64,"pivot":Vector2(32,64),"pieces":[PackedVector2Array([Vector2.ZERO,Vector2(64,0),Vector2(64,64),Vector2(0,64)])]}
	var prop:Dictionary={"id":"library/sp-fixture","registration":reg,"rect":Rect2(-70,-90,140,180),"library_texture":texture,"layout_flip":Vector2.ONE,"library_asset":true}
	var views:Array=[]
	for i in range(2):
		var vp:=SubViewport.new();vp.size=Vector2i(320,320);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);views.append(vp)
	var reference:=Reference.new();views[0].add_child(reference)
	var content:=Content.new();content.cull_props=false;content.draw_origin=Vector2(160.375,190.125);views[1].add_child(content)
	var context:=Context.new()
	var builds:=0
	for change in ["initial","same","move","resize","mirror","pieces","texture","floor","hidden","unhide","empty","restore"]:
		match change:
			"move":prop.rect.position+=Vector2(9.25,-7.125)
			"resize":prop.rect.size*=.83
			"mirror":prop.registration=Library.mirror_registration(prop.registration)
			"pieces":prop.registration.pieces.append(PackedVector2Array([Vector2(10,20),Vector2(50,10),Vector2(40,50),Vector2(30,30),Vector2(0,40)]))
			"texture":prop.library_texture=ImageTexture.create_from_image(image)
			"floor":prop.floor_piece=true
			"hidden":prop.layout_hidden=true
			"unhide":prop.layout_hidden=false
		var empty:bool=change=="empty"
		reference.prop={} if empty else prop;reference.queue_redraw()
		content.submit(context,[] if empty else [{"kind":"prop","prop":prop}])
		await process_frame;await RenderingServer.frame_post_draw;pairs+=1
		check(views[0].get_texture().get_image().get_data()==views[1].get_texture().get_image().get_data(),"Cache transition exact "+change)
		if empty or change=="hidden":check(not content.slots[0].has_meta("triangle_base"),"Unused slot cache released")
		elif change=="same":check(content.ordinary_builds==builds,"Stable geometry reused")
		else:check(content.ordinary_builds>builds,"Changed geometry rebuilt")
		builds=content.ordinary_builds
	for flag in ["custom_library_draw","portable_view","drone_dock","aquarium"]:
		content.slots[0].set_meta("triangle_base",{"sentinel":true})
		if flag in ["drone_dock","aquarium"]:prop.registration[flag]={}
		else:prop[flag]=true
		content.submit(context,[{"kind":"prop","prop":prop}])
		check(not content.slots[0].has_meta("triangle_base"),"Excluded path releases cache "+flag)
		if flag in ["drone_dock","aquarium"]:prop.registration.erase(flag)
		else:prop.erase(flag)
	content.submit(context,[{"kind":"library_live","prop":prop}])
	check(not content.slots[0].has_meta("triangle_base"),"Reclassified slot cache released")
	var weak:WeakRef=weakref(content)
	for vp in views:vp.queue_free()
	for attempt in range(8):
		if weak.get_ref()==null:break
		await process_frame
	check(weak.get_ref()==null,"Cache owner released")
	FileAccess.open("user://results.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"raster_pairs":pairs,"builds":builds}))
	print("TRIANGLE_CACHE ",checks," checks ",failures," failures");quit(1 if failures else 0)

