extends SceneTree
class Fleet extends RefCounted:
	var orders: Array=[]
	var drones: Dictionary={}
class Host extends RefCounted:
	var drone_fleet=Fleet.new()
	var occupied: Dictionary={Vector2i.ZERO:{"id":"construction_drone_bay"}}
class Probe extends "res://scripts/grid_canvas.gd":
	var host=Host.new()
	func _ready():pass
	func _process(_delta: float):pass
	func _cell_size() -> float:return 384.0
	func drone_anchors(_room: Dictionary) -> Dictionary:return {"dock":Vector2.ZERO,"hatch":Vector2.ZERO}
	func _draw():
		draw_target=self
		_draw_drones(host)
func _init():call_deferred("run")
func capture(probe) -> PackedByteArray:
	probe.queue_redraw()
	await process_frame;RenderingServer.force_draw()
	await process_frame;RenderingServer.force_draw()
	return root.get_texture().get_image().get_data()
func run():
	if DisplayServer.get_name()=="headless":
		push_error("Drone handoff requires native renderer");quit(1);return
	root.size=Vector2i(384,384);root.content_scale_size=Vector2i(384,384)
	var probe=Probe.new();root.add_child(probe)
	var failures:=0
	for kind in ["construction","mining","salvage"]:
		var drone={"kind":kind,"home":Vector2i.ZERO,"position":Vector2.ZERO,"target":Vector2.ONE,"phase":"launching","elapsed":1.2,"clock":0.0,"job":"construct","order":{}}
		probe.host.drone_fleet.drones={Vector2i.ZERO:drone}
		drone.phase="docked"
		var empty: PackedByteArray=await capture(probe)
		drone.phase="launching"
		var launch: PackedByteArray=await capture(probe)
		if launch==empty:failures+=1;push_error(kind+" drone failed to render")
		drone.phase="outbound";drone.elapsed=0.0
		var outbound: PackedByteArray=await capture(probe)
		if launch!=outbound:failures+=1;push_error(kind+" jumps at launch/outbound")
		drone.phase="returning"
		var returning: PackedByteArray=await capture(probe)
		drone.phase="docking";drone.elapsed=0.0
		var dock: PackedByteArray=await capture(probe)
		if returning!=dock:failures+=1;push_error(kind+" jumps at return/docking")
	print("DRONE HATCH HANDOFF: 6 native comparisons, %d failures"%failures)
	quit(failures)
