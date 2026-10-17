extends RefCounted
## Slot-owned invariant monitor geometry; original dynamic clock math and commands retained.
const Library=preload("res://scripts/room_asset_library.gd")
## Read-only normalized samples, shared by one scene; no art or prior-clock retention.
class FramePatterns extends RefCounted:
	var valid:=false
	var clock:=0.0
	var waves:Dictionary={}
	var builds:=0
	static func build_wave(phase:float)->PackedVector2Array:
		var result:=PackedVector2Array()
		for i in range(25):
			var x:float=float(i)/24.0
			var y:float=0.5+0.42*(sin(x*9.0+phase*2.2)*0.6+sin(x*23.0-phase*3.1)*0.4)
			result.append(Vector2(x,y))
		return result
	func wave(time:float,index:int)->PackedVector2Array:
		if not valid or clock!=time:
			waves.clear();clock=time;valid=true
		if waves.has(index):return waves[index]
		var result:PackedVector2Array=build_wave(time+index*1.7)
		builds+=1
		if waves.size()<64:waves[index]=result
		return result
class Screen extends RefCounted:
	var index:int
	var box:Rect2
	var kind:int
	var center:Vector2
	var radius:float
	var inner:Rect2
	var count:int
	var spacing:float
class Prepared extends RefCounted:
	var color:Color
	var width:float
	var screens:Array[Screen]=[]
static func build(reg:Dictionary,anchor:Vector2,scale_value:float)->Prepared:
	var color:=Color(str(reg.operating_screen_color)) if reg.has("operating_screen_color") else Color(.13,.75,.78,.8)
	var width:float=maxf(.55,scale_value*1.4)
	var prepared:=Prepared.new();prepared.color=color;prepared.width=width
	for index in range(reg.get("operating_screens",[]).size()):
		var s:Array=reg.operating_screens[index]
		var a:Vector2=anchor+(Library.source_uv(reg,Vector2(s[0],s[1]))-reg.pivot)*scale_value
		var b:Vector2=anchor+(Library.source_uv(reg,Vector2(s[0]+s[2],s[1]+s[3]))-reg.pivot)*scale_value
		var box:=Rect2(Vector2(minf(a.x,b.x),minf(a.y,b.y)),(b-a).abs())
		var aspect:float=float(s[2])/maxf(1.0,float(s[3]))
		var row:=Screen.new();row.index=index;row.box=box
		if float(s[2])*float(s[3])>=10000.0 and aspect>1.3 and aspect<2.6:
			row.kind=0;row.center=box.get_center();row.radius=minf(box.size.x,box.size.y)*0.42
		elif aspect>=1.6:
			row.kind=1;row.inner=box.grow_individual(-box.size.x*0.08,-box.size.y*0.15,-box.size.x*0.08,-box.size.y*0.15)
		else:
			row.kind=2;row.inner=box.grow(-minf(box.size.x,box.size.y)*0.14);row.count=4 if aspect<1.0 else 5;row.spacing=float(row.inner.size.x)/row.count
		prepared.screens.append(row)
	return prepared
static func draw(room,data:Prepared,patterns:FramePatterns=null)->void:
	if not room.operating:return
	var t:float=0.0 if preload("res://scripts/title_settings.gd").reduced_motion else room.machine_clock
	var color:Color=data.color;var width:float=data.width
	for row:Screen in data.screens:
		var box:Rect2=row.box;var index:int=row.index
		room.painter.draw_rect(box,Color(color,0.10))
		var phase:float=t+index*1.7
		if row.kind==0:
			var c:Vector2=row.center;var radius:float=row.radius
			room.painter.draw_arc(c,radius,0,TAU,32,Color(color,0.25),width*0.6)
			room.painter.draw_arc(c,radius*0.5,0,TAU,24,Color(color,0.18),width*0.6)
			var sweep:float=fposmod(phase*1.2,TAU)
			for k in range(5):
				var trail:float=sweep-k*0.09
				room.painter.draw_line(c,c+Vector2(cos(trail),sin(trail))*radius,Color(color,0.7*(1.0-k*0.2)),width)
			for i in range(3):
				var angle:float=float(i)*2.39996+index
				var since:float=fposmod(sweep-angle,TAU)
				var blip:Vector2=c+Vector2(cos(angle),sin(angle))*radius*(0.3+0.2*i)
				room.painter.draw_circle(blip,width*1.2,Color(color.lightened(0.3),maxf(0.0,1.0-since/2.5)))
		elif row.kind==1:
			var inner:Rect2=row.inner
			for g in [0.25,0.75]:
				var y:float=inner.position.y+inner.size.y*g
				room.painter.draw_line(Vector2(inner.position.x,y),Vector2(inner.end.x,y),Color(color,0.15),width*0.6)
			var trace:=PackedVector2Array()
			var wave:PackedVector2Array=patterns.wave(t,index) if patterns!=null else FramePatterns.build_wave(phase)
			for point in wave:trace.append(inner.position+inner.size*point)
			room.painter.draw_polyline(trace,color,width,true)
		else:
			var inner:Rect2=row.inner;var count:int=row.count;var spacing:float=row.spacing
			for i in range(count):
				var level:float=0.25+0.65*(0.5+0.5*sin(phase*1.6+i*1.3))
				var bar:=Rect2(inner.position.x+spacing*(i+0.2),inner.end.y-inner.size.y*level,spacing*0.6,inner.size.y*level)
				room.painter.draw_rect(bar,Color(color,0.55))
