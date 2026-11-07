extends SceneTree
const Lighting=preload("res://rooms/whole-room/room_lighting.gd")
class Sample extends Node2D:
	var level=1.0
	var props=[{"rect":Rect2(-160,-145,95,72)},{"rect":Rect2(-90,-100,125,90),"footprint":[0.1,0.65,0.8,0.35]},{"rect":Rect2(125,125,95,90)},{"rect":Rect2(-220,65,90,40)},{"rect":Rect2(65,-140,75,60),"layout_hidden":true},{"rect":Rect2(60,-20,70,70),"registration":{"owns_contact_shadow":true}}]
	func prop_visual_bounds(prop):
		return Rect2(prop.rect.position,prop.rect.size+Vector2(0,8+77*level))
	func _draw():
		draw_rect(Rect2(-250,-250,500,500),Color("8d9694"))
		Lighting.draw_equipment_shadows(self,props,level,self)
var failures:=0
var cases:=0
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":
		push_error("Shadow parity requires a native renderer")
		quit(1);return
	var foot:=Rect2(-90,-80,60,40)
	var original:=Lighting.projected_shadow_mesh(foot,12.0)
	assert(original.points!=Lighting.projected_shadow_mesh(Rect2(-89,-80,60,40),12.0).points)
	assert(original.points!=Lighting.projected_shadow_mesh(foot,40.0).points)
	for i in range(2200): Lighting.projected_shadow_mesh(Rect2(i*0.1,0,60,40),12.0)
	assert(Lighting._projected_meshes.size()<=2048)
	assert(Lighting.projected_shadow_mesh(foot,12.0)==original)
	root.size=Vector2i(1100,1100)
	var sample=Sample.new();root.add_child(sample);sample.position=Vector2(550,550)
	for zoom in [0.4,1.0,2.0]:
		sample.scale=Vector2.ONE*zoom
		for level in [0.0,0.5,1.0]:
			sample.level=level
			sample.props[0].rect.position.x+=3.0
			var reference: PackedByteArray
			for batched in [false,true]:
				Lighting.batch_projected_shadows=batched
				sample.queue_redraw()
				await process_frame
				RenderingServer.force_draw()
				await process_frame
				RenderingServer.force_draw()
				var pixels:=root.get_texture().get_image().get_data()
				if not batched:reference=pixels
				else:
					cases+=1
					if pixels!=reference:
						failures+=1
						push_error("Shadow mismatch at zoom %s light %s"%[zoom,level])
	print("PROJECTED SHADOW PARITY: %d cases, %d failures"%[cases,failures])
	quit(failures)
