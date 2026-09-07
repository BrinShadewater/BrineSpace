extends SceneTree
const Lighting = preload("res://rooms/whole-room/room_lighting.gd")
class Sample extends Node2D:
	func _draw() -> void:
		draw_rect(Rect2(0,0,1600,900),Color("343b45"))
		for column in range(3):
			for row in range(3):
				draw_set_transform(Vector2(260+column*500,240+row*290),0,Vector2.ONE*(0.7+row*0.3))
				Lighting.draw_pools(self,float(row+1)/3.0,column==1,column==2)
		draw_set_transform(Vector2.ZERO)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size = Vector2i(1600,900)
	var subject := Sample.new()
	root.add_child(subject)
	Lighting.batch_pools = false
	subject.queue_redraw()
	await RenderingServer.frame_post_draw
	var before := root.get_texture().get_image()
	Lighting.batch_pools = true
	subject.queue_redraw()
	await RenderingServer.frame_post_draw
	var after := root.get_texture().get_image()
	var a := before.get_data()
	var b := after.get_data()
	var maximum := 0
	var changed := 0
	for i in range(a.size()):
		var difference := absi(int(a[i])-int(b[i]))
		maximum = maxi(maximum,difference)
		if difference > 0: changed += 1
	print("LIGHT POOL PARITY: max byte difference=%d changed=%d/%d" % [maximum,changed,a.size()])
	after.save_png("res://output/light-pools-mesh.png")
	quit(0 if maximum <= 1 else 1)
