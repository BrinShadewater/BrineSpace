extends SceneTree
const View = preload("res://rooms/power-expansion-v1/power_room_view.gd")
const Rooms = preload("res://scripts/room_database.gd")
const IDS := ["current_turbine","biomass_digester","heat_recovery"]
class Canvas extends Node2D:
	var room
	var q := 0
	var time := 0.0
	var running := false
	var at := Vector2(256,256)
	var scale_value := 1.16
	func _draw() -> void:
		if room==null: return
		room.configure_embedded(q,[],running,time)
		room.render_into(self,at,scale_value)
func _init() -> void: call_deferred("run")
func frame(canvas) -> Image:
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	return root.get_texture().get_image()
func run() -> void:
	root.size=Vector2i(512,512)
	root.content_scale_size=root.size
	root.transparent_bg=true
	DirAccess.make_dir_recursive_absolute("res://output/power-rooms")
	var canvas := Canvas.new()
	root.add_child(canvas)
	var checks := 0
	for id in IDS:
		var view := View.new()
		view.room_id=id
		view.embedded=true
		view.hide()
		root.add_child(view)
		canvas.room=view
		canvas.q=0
		canvas.running=false
		var card := await frame(canvas)
		assert(card.save_png("res://rooms/power-expansion-v1/%s-card.png" % id)==OK)
		for q in range(4):
			canvas.q=q
			canvas.running=true
			canvas.time=0.0
			var first := await frame(canvas)
			assert(first.save_png("res://output/power-rooms/%s-q%d.png" % [id,q])==OK)
			var expected: Array=Rooms.get_layout(Rooms.get_room(id).layout).doors
			var names := ["north","east","south","west"]
			var open: Array=[]
			for side in range(4):
				var should_open: bool=expected.has(names[posmod(side-q,4)])
				assert(view.Geometry.has_port(view.layout[0],side)==should_open,"Door mismatch: "+id)
				if should_open: open.append(side)
			view.configure_embedded(q,open,true,0)
			# Large equipment permits detours rather than requiring straight aisles.
			var visited := {Vector2i.ZERO:true}
			var queue: Array[Vector2i]=[Vector2i.ZERO]
			while not queue.is_empty():
				var cell: Vector2i=queue.pop_front()
				for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
					var next: Vector2i=cell+offset
					if abs(next.x)>22 or abs(next.y)>22 or visited.has(next): continue
					if view.Geometry.can_stand(Vector2(next)*8,view.layout,view.props,view.edges):
						visited[next]=true
						queue.append(next)
			for side in open:
				assert(visited.has(view.Geometry.DIRS[side]*22),"Port unreachable: %s q%d side%d" % [id,q,side])
			for prop in view.props:
				assert(Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),"Sprite outside hull: "+id)
			canvas.time=1.1
			var later := await frame(canvas)
			assert(first.get_data()!=later.get_data(),"Operating cue missing: "+id)
			canvas.running=false
			var stopped := await frame(canvas)
			canvas.time=4.0
			var stopped_later := await frame(canvas)
			assert(stopped.get_data()==stopped_later.get_data(),"Offline machinery still animates: "+id)
			checks+=1
		canvas.room=null
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		view.free()
	print("POWER ROOM ART: PASS — three cards, %d rotation/route/operating/offline checks" % checks)
	quit()
