extends SceneTree
const Art=preload("res://scripts/drone_art.gd")
class Sample extends Node2D:
	var clock:=0.0
	var width:=360.0
	func _draw():
		Art._draw_articulated(self,"construction",Vector2(400,400),width,clock,Color.WHITE)
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":
		push_error("Drone articulation requires native pixel readback");quit(1);return
	root.size=Vector2i(800,800);root.content_scale_size=Vector2i(800,800)
	var sample:=Sample.new();root.add_child(sample)
	var failures:=0
	for width in [180.0,360.0]:
		sample.width=width
		var factor: float=width/360.0
		var origin:=Vector2(400,400)-Vector2(360,390)*factor/2
		# The central winch below the old y=220 split belongs to the rigid chassis.
		var body_rect:=Rect2i(origin+Vector2(140,200)*factor,Vector2(80,45)*factor)
		var claw_rect:=Rect2i(origin+Vector2(0,300)*factor,Vector2(360,85)*factor)
		var body: PackedByteArray
		var claws: PackedByteArray
		var moved:=false
		for phase in range(8):
			sample.clock=float(phase)*TAU/3.5/8
			sample.queue_redraw()
			await process_frame;RenderingServer.force_draw()
			await process_frame;RenderingServer.force_draw()
			var image:=root.get_texture().get_image()
			var next_body:=image.get_region(body_rect).get_data()
			var next_claws:=image.get_region(claw_rect).get_data()
			if phase==0:body=next_body;claws=next_claws
			else:
				if next_body!=body:failures+=1;push_error("Construction chassis shears at phase %d width %s"%[phase,width])
				if next_claws!=claws:moved=true
		if not moved:failures+=1;push_error("Construction claws are frozen")
	print("CONSTRUCTION ARTICULATION: 16 native poses, %d failures"%failures)
	quit(failures)
