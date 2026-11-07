extends SceneTree
const OUT="res://assets/drone-runtime-2026-09-26/review"
const Motion=preload("res://scripts/drone_animation.gd")
const Dock=preload("res://scripts/drone_dock.gd")
class Preview extends Node2D:
	var time:=0.0
	func _draw() -> void:
		draw_rect(Rect2(0,0,900,450),Color("182a30"))
		for i in range(3):
			var kind:String=["construction","mining","salvage"][i]
			var t:=time;var phase:="docked";var elapsed:=t
			if t>=10.4:phase="docked";elapsed=t-10.4
			elif t>=9.2:phase="docking";elapsed=t-9.2
			elif t>=8.2:phase="returning";elapsed=t-8.2
			elif t>=4.2:phase="working";elapsed=t-4.2
			elif t>=3.2:phase="outbound";elapsed=t-3.2
			elif t>=2:phase="launching";elapsed=t-2
			var d:Dictionary={"kind":kind,"phase":phase,"elapsed":elapsed,"clock":t,"animation_phase":phase,"animation_started":t-elapsed,"animation_work_duration":4.0,"animation_heading":"south" if phase!="returning" else "north","animation_distance":maxf(0,t-3.2)*35,"animation_rotor":t*60,"job":"construct" if t<10.4 else "","cargo":{"metal":1} if phase in ["returning","docking"] else {}}
			var width:float=Dock.record(kind).world_width*1.7
			var rect:=Rect2(150+i*300-width*.5,55,width,width)
			Dock.draw(self,rect,kind,d,true,t)
			if phase in ["outbound","working","returning"]:
				var alpha:=clampf(elapsed*3,0,1) if phase=="outbound" else clampf((1-elapsed)*3,0,1) if phase=="returning" else 1.0
				Motion.draw(self,d,Vector2(150+i*300,345),1.7,.42,true,t,alpha)
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(900,450);root.content_scale_size=root.size
	DirAccess.make_dir_recursive_absolute(OUT)
	var preview:=Preview.new();preview.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(preview)
	for n in range(180):
		preview.time=n/15.0;preview.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(OUT+"/frame-%03d.png"%n)
	print("DRONE NATIVE REVIEW: 180 frames, all three docks and work/cargo layers")
	quit()
