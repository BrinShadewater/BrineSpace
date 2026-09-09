extends SceneTree
const Store = preload("res://scripts/room_layout_store.gd")
class Canvas extends Node2D:
	var quarter := 0
	var legacy := true
	var elapsed_usec := 0
	var prop := {"id":"fixture", "rect":Rect2(0,0,40,60), "layout_flip":Vector2(-1,1)}
	func prop_visual_bounds(item: Dictionary) -> Rect2: return item.rect
	func _draw() -> void:
		var begin := Time.get_ticks_usec()
		for i in range(4000):
			if legacy:
				var axes: Vector2 = prop.get("layout_flip", Store.flip_axes(self,str(prop.id)))
				var center := prop_visual_bounds(prop).get_center()
				draw_set_transform(Vector2(50,50)+(center-center*axes),0,axes)
			else:
				Store.draw_flip(self,self,prop,Vector2(50,50),1.0)
		elapsed_usec = Time.get_ticks_usec()-begin
		draw_rect(Rect2(0,0,13,45),Color.CORAL)
		draw_rect(Rect2(13,0,27,12),Color.CYAN)
func _init() -> void: call_deferred("run")
func run() -> void:
	assert(DisplayServer.get_name() != "headless", "Requires native rendering")
	Store.loaded = true
	Store.data = {}
	var canvas := Canvas.new()
	canvas.set_meta("layout_asset","room-brine_core")
	root.add_child(canvas)
	var timings := []
	for axes in [Vector2.ONE,Vector2(-1,1),Vector2(1,-1),Vector2(-1,-1),Vector2.ZERO]:
		if axes == Vector2.ZERO:
			canvas.prop.erase("layout_flip")
			canvas.set_meta("layout_draft",{"flip/fixture":[true,true]})
		else: canvas.prop.layout_flip = axes
		canvas.legacy = true
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var reference := root.get_texture().get_image()
		var before := canvas.elapsed_usec
		canvas.legacy = false
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		assert(reference.get_data() == root.get_texture().get_image().get_data(), "Flip optimization must preserve pixels, including uncached drafts")
		timings.append({"axes":str(axes),"before_usec":before,"after_usec":canvas.elapsed_usec})
	print("PROP FLIP PASS: all four flips and uncached draft fallback have identical pixels / ",JSON.stringify(timings))
	canvas.queue_free()
	await process_frame
	quit()
