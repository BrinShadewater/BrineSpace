extends SceneTree
const Fixture=preload("res://tests/test_modular_floor.gd")
const Floor=preload("res://rooms/whole-room/modular_floor.gd")
class Bench extends Fixture.SurfaceCanvas:
	var cpu_usec:=0
	func _draw() -> void:
		var start:=Time.get_ticks_usec()
		for i in range(100): super._draw()
		cpu_usec=Time.get_ticks_usec()-start
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(512,512); DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED); Engine.max_fps=0
	var canvas:=Bench.new(); root.add_child(canvas)
	for y in range(8):
		for x in range(8): canvas.values["tile/%d/%d"%[x,y]]=[x%4,y%4]
	var rows: Array=[]
	for reference in [true,false]:
		canvas.reference=reference
		for i in range(10): canvas.queue_redraw(); await process_frame; RenderingServer.force_draw()
		var cpu:=0.0; var total:=0.0
		for i in range(60):
			var start:=Time.get_ticks_usec()
			canvas.queue_redraw(); await process_frame; RenderingServer.force_draw()
			cpu+=canvas.cpu_usec/1000.0; total+=(Time.get_ticks_usec()-start)/1000.0
		rows.append({"reference":reference,"floor_submission_ms":cpu/60,"frame_ms":total/60,"floor_count":100,"samples":60,"mesh_builds":Floor.builds})
	var file:=FileAccess.open("res://output/tiled-floor-pilot/profile.json",FileAccess.WRITE); file.store_string(JSON.stringify(rows,"\t")); file.close()
	print("FLOOR PROFILE: "+JSON.stringify(rows)); quit()
