extends SceneTree
class Original extends RefCounted:
	static func _draw_water(canvas: CanvasItem, floor: Rect2, level: float, clock: float, pumping: bool) -> void:
		if level<=0.001: return
		var height := floor.size.y*clampf(level,0,1)
		var wet := Rect2(floor.position+Vector2(0,floor.size.y-height),Vector2(floor.size.x,height))
		# Depth colour stays translucent so the real deck/grating remains readable.
		var vertices := PackedVector2Array([wet.position,Vector2(wet.end.x,wet.position.y),wet.end,Vector2(wet.position.x,wet.end.y)])
		canvas.draw_polygon(vertices,PackedColorArray([Color(0.11,0.35,0.42,0.45),Color(0.11,0.35,0.42,0.45),Color(0.06,0.24,0.31,0.34),Color(0.06,0.24,0.31,0.34)]))
		# Soft contact shadows along the walls, without an unfilled floor margin.
		for i in range(4):
			var inset := float(i)*2.0
			var alpha := 0.055*(1.0-float(i)/4.0)
			var stripe_height := maxf(0.0,wet.size.y-inset*2.0)
			if stripe_height<=0: break
			canvas.draw_rect(Rect2(wet.position+Vector2(inset,inset),Vector2(2,stripe_height)),Color(0.02,0.09,0.12,alpha))
			canvas.draw_rect(Rect2(Vector2(wet.end.x-inset-2,wet.position.y+inset),Vector2(2,stripe_height)),Color(0.02,0.09,0.12,alpha))
		# Sparse moving caustic ribbons: short uneven curves rather than a bright grid.
		if wet.size.y>8.0:
			var row:=0
			var y:=wet.position.y+8.0
			while y<wet.end.y-4.0:
				var x:=wet.position.x+6.0
				var column:=0
				while x<wet.end.x-6.0:
					var seed:=float(row*13+column*7)
					var length:=minf(18.0+7.0*sin(seed*1.7),wet.end.x-x-3.0)
					var ribbon:=PackedVector2Array()
					var cos_offset:=cos(seed+clock*0.4)*2.0
					for point_index in range(7):
						var along:=float(point_index)/6.0
						var yy:=y+sin(along*PI+seed+clock*0.65)*3.0+cos_offset
						ribbon.append(Vector2(x+along*length,clampf(yy,wet.position.y+2,wet.end.y-2)))
					canvas.draw_polyline(ribbon,Color(0.55,0.76,0.73,0.07+0.025*sin(seed+clock)),1.1,true)
					x+=36.0+5.0*cos(seed)
					column+=1
				y+=27.0+3.0*sin(float(row)*2.0)
				row+=1
		# Pump turbulence is contained by the actual wetted footprint.
		if pumping and wet.size.y>12.0:
			var drain:=Vector2(wet.get_center().x,wet.end.y-10.0)
			for ring in range(3):
				var radius:=5.0+fposmod(clock*9.0+float(ring)*12.0,36.0)
				var arc:=PackedVector2Array()
				for step in range(25):
					var point:=drain+Vector2.RIGHT.rotated(PI+float(step)*PI/24.0)*Vector2(radius,radius*0.45)
					if wet.has_point(point): arc.append(point)
					elif arc.size()>1: canvas.draw_polyline(arc,Color(0.53,0.74,0.73,0.13),1,true); arc=PackedVector2Array()
				if arc.size()>1: canvas.draw_polyline(arc,Color(0.53,0.74,0.73,0.13),1,true)
		if level<0.999:
			var surface:=PackedVector2Array()
			for i in range(25):
				var xx:=lerpf(wet.position.x,wet.end.x,float(i)/24.0)
				surface.append(Vector2(xx,wet.position.y+sin(float(i)*0.7+clock*1.5)*minf(1.5,height*0.1)))
			canvas.draw_polyline(surface,Color(0.53,0.73,0.73,0.38),1.3,true)

const Candidate=preload("res://rooms/large-rooms/moonbay.gd")
class Paint extends Node2D:
	var candidate:=false
	var floor:=Rect2(-180,-180,360,360)
	var level:=1.0
	var clock:=0.0
	var pumping:=false
	func _draw():
		draw_set_transform(Vector2(240.375,250.1875),0,Vector2(.91,1.03))
		if candidate:Candidate._draw_water(self,floor,level,clock,pumping)
		else:Original._draw_water(self,floor,level,clock,pumping)
var pairs:=0
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(480,480)
	var views:Array=[];var paints:Array=[]
	for mode in range(2):
		var viewport:=SubViewport.new();viewport.size=Vector2i(480,480);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport);views.append(viewport)
		var canvas:=Paint.new();canvas.candidate=mode==1;canvas.modulate=Color(.8,.9,1,.7);viewport.add_child(canvas);paints.append(canvas)
	for floor in [Rect2(-192,-192,384,384),Rect2(-80,-40,160,80),Rect2(-45,-9,90,18)]:
		for level in [0.0,.001,.1,.5,.998,1.0]:
			for clock in [0.0,.375,3.125]:
				for pumping in [false,true]:
					for scale_value in [.73,1.0]:
						for canvas in paints:canvas.floor=floor;canvas.level=level;canvas.clock=clock;canvas.pumping=pumping;canvas.scale=Vector2.ONE*scale_value;canvas.queue_redraw()
						await process_frame;await RenderingServer.frame_post_draw;pairs+=1
						check(views[0].get_texture().get_image().get_data()==views[1].get_texture().get_image().get_data(),"Exact water command replay")
						check(paints[1].get_meta("moonbay_water_commands",{}).size()<=16,"Bounded canvas-owned lookup")
	var oldest:=Rect2(-125,-100,210,160)
	for i in range(22):
		for canvas in paints:canvas.floor=Rect2(-125,-100,210+float(i),160);canvas.level=1.0;canvas.clock=0.0;canvas.pumping=false;canvas.queue_redraw()
		await process_frame;await RenderingServer.frame_post_draw;pairs+=1
		check(views[0].get_texture().get_image().get_data()==views[1].get_texture().get_image().get_data(),"Eviction sequence remains exact")
		check(paints[1].get_meta("moonbay_water_commands").size()<=16,"Limit exercised")
	check(paints[1].get_meta("moonbay_water_commands").size()==16,"Cache reaches bounded capacity")
	check(not paints[1].get_meta("moonbay_water_commands").has([oldest,1.0,0.0,false]),"Old key evicted")
	for canvas in paints:canvas.floor=oldest;canvas.queue_redraw()
	await process_frame;await RenderingServer.frame_post_draw;pairs+=1
	check(views[0].get_texture().get_image().get_data()==views[1].get_texture().get_image().get_data(),"Evicted commands reconstruct exactly")
	check(paints[1].get_meta("moonbay_water_commands").has([oldest,1.0,0.0,false]),"Old key evicted and prepared again")
	# Repeated full water must retain its stationary geometry across activity/pause.
	var stationary_build:int=paints[1].get_meta("water_stroke_build_usec",0)
	for clock in [0.0,0.0,.375,0.0,1.375]:
		for canvas in paints:canvas.clock=clock;canvas.level=1.0;canvas.queue_redraw()
		await process_frame;await RenderingServer.frame_post_draw;pairs+=1
		check(views[0].get_texture().get_image().get_data()==views[1].get_texture().get_image().get_data(),"Activity and pause preserve pixels")
		check(paints[1].get_meta("water_stroke_build_usec",0)==stationary_build,"Stationary commands reused after activity")
	check(paints[1].get_meta("water_stroke_topology",{}).size()>0,"Dynamic topology preparation exercised")
	check(paints[1].get_meta("water_stroke_topology",{}).size()<=1024,"Dynamic topology stays bounded")
	var weak: WeakRef = weakref(paints[1])
	for view in views:view.queue_free()
	for attempt in range(8):
		if weak.get_ref()==null: break
		print("OWNER_RELEASE attempt=",attempt," valid=",is_instance_valid(weak.get_ref())," queued=",weak.get_ref().is_queued_for_deletion())
		await process_frame
	check(weak.get_ref()==null,"Cache-owning canvas released")
	FileAccess.open("user://context.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"raster_pairs":pairs}))
	print("MOONBAY_WATER ",checks," checks, ",failures," failures");quit(1 if failures else 0)
