extends RefCounted
## Cosmetic state only. Door aperture and water transfer remain simulation-owned.
static func advance(previous: Dictionary, frame: int, clock: float) -> Dictionary:
	if previous.is_empty() or clock<float(previous.get("clock",0)):
		return {"frame":frame,"clock":clock,"closing_until":-1.0}
	var until: float=previous.get("closing_until",-1.0)
	if frame<int(previous.frame): until=clock+0.32
	elif frame>int(previous.frame): until=-1.0
	return {"frame":frame,"clock":clock,"closing_until":until}

static func draw(canvas: CanvasItem, mouth: Vector2, direction: Vector2, aperture: float, difference: float, water: float, closing: bool, clock: float, scale: float) -> void:
	if water<=0.015: return
	var across:=Vector2(-direction.y,direction.x)
	var flow:=direction*(1.0 if difference>=0 else -1.0)
	var amount:=clampf(aperture,0,1)
	var gap:=36.0*amount*amount*(3-2*amount)
	# Wet gasket and compact pressure indicators remain visible after sealing.
	for side in [-1,1]:
		var at:=mouth+across*float(side)*43*scale
		var color:=Color("c98b4e") if closing else Color("668e88")
		canvas.draw_circle(at,1.5*scale,color)
	if amount<=0:
		canvas.draw_line(mouth-across*32*scale-flow*3*scale,mouth+across*32*scale-flow*3*scale,Color(0.42,0.66,0.63,0.28),maxf(0.6,scale*0.7),true)
		return # A sealed door must never suggest water crossing it.
	if absf(difference)<0.015: return
	var strength:=minf(1,absf(difference)*2)
	var reach: float=(6+amount*10)*scale
	var bank:=PackedVector2Array([mouth-across*gap*scale-flow*reach,mouth+across*gap*scale-flow*reach,mouth+across*gap*scale+flow*reach*0.5,mouth-across*gap*scale+flow*reach*0.5])
	canvas.draw_colored_polygon(bank,Color(0.19,0.48,0.5,strength*0.15))
	# Short fragmented foam follows the narrowing aperture, never the whole wall.
	for i in range(5):
		var phase:=fposmod(clock*(0.7+strength)+i*0.21,1.0)
		var offset: float=sin(i*9.7)*gap*0.72
		var at:=mouth+across*offset*scale+flow*(phase-0.5)*reach
		var alpha:=sin(phase*PI)*strength*(0.65 if closing else 0.28)
		var half:=minf(gap*0.18,2.3)*scale
		canvas.draw_line(at-across*half,at+across*half,Color(0.69,0.83,0.76,alpha),maxf(0.65,scale*0.75),true)
	if closing:
		# Compression ripples stay on the higher-water side as leaves meet.
		for layer in range(2):
			var phase:=fposmod(clock*1.8+layer*0.5,1.0)
			var points:=PackedVector2Array()
			for i in range(13):
				var x: float=i/12.0*2-1
				points.append(mouth+across*x*(gap+phase*5)*scale-flow*(3+phase*11+(1-x*x)*4)*scale)
			canvas.draw_polyline(points,Color(0.54,0.75,0.7,(1-phase)*strength*0.38),maxf(0.6,scale*0.7),true)
