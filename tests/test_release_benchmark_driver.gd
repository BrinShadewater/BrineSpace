extends SceneTree
const Driver = preload("res://tools/release_benchmark.gd").FrameDriver
class Canvas extends Node2D:
	var draws := {}
	func _process(_delta): queue_redraw()
	func _draw():
		var frame_id:=Engine.get_process_frames()
		draws[frame_id]=int(draws.get(frame_id,0))+1
		draw_rect(Rect2(10,10,40,40),Color.CORAL)
var failures:=0
var steps:=0
func check(ok,label):
	if not ok: failures+=1;push_error(label)
func _init():call_deferred("run")
func step():steps+=1
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var canvas=Canvas.new();root.add_child(canvas)
	var driver=Driver.new();driver.process_priority=-1000;root.add_child(driver)
	var counts:={}
	for mode in ["signal","node"]:
		for index in range(5):
			await process_frame
			if mode=="signal":canvas.queue_redraw();step()
			else:driver.action=canvas.queue_redraw;driver.advance=step
			await RenderingServer.frame_post_draw
			if index>0:
				var count:int=canvas.draws.get(Engine.get_process_frames(),0)
				if not counts.has(mode):counts[mode]=[]
				counts[mode].append(count)
	check(steps==10,"Exactly one simulation step per requested frame")
	check(driver.steps==5,"Driver ran only the five scheduled steps")
	check(counts.node.all(func(n):return n==1),"Node driver coalesces redraws")
	check(counts.signal.all(func(n):return n==2),"Historical signal driver reproduces duplicate drawing")
	await process_frame
	await RenderingServer.frame_post_draw
	check(steps==10,"Idle driver does not repeat a consumed action")
	print("BENCHMARK DRIVER ",counts," steps=",steps," failures=",failures)
	canvas.queue_free();driver.queue_free();await process_frame
	quit(0 if failures==0 else 1)
