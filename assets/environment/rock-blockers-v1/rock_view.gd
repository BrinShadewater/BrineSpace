extends RefCounted
const EnvironmentArt = preload("res://scripts/environment_art.gd")
## Continuous world-mapped material; only exposed sides receive cliff edges.
const Field := preload("res://scripts/wreck_field.gd")
const SOURCE := "res://legacy/default/assets/environment/rock-blockers-v1/basalt-surface-v1.png"
const DIRECTIONS := [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]
var surface: Texture2D
var surface_attempted:=false
# Reference switch keeps the original submissions available for native comparison.
var skip_empty_minerals := not OS.get_cmdline_user_args().has("--reference-empty-minerals")

func texture() -> Texture2D:
	if not surface_attempted:
		surface_attempted=true
		surface=EnvironmentArt.texture("basalt-surface")
		if surface!=null:return surface
		var source := Image.new()
		if preload("res://scripts/safe_image.gd").load_png(source, SOURCE) == OK:
			surface = ImageTexture.create_from_image(source)
	return surface

static func is_rock(field: Dictionary, cell: Vector2i) -> bool:
	return Field.blocks(field,cell) and (field[cell].kind == "basalt" or not Field.visible(field,cell))

static func connections(field: Dictionary, cell: Vector2i) -> int:
	var mask := 0
	for i in range(4):
		if is_rock(field,cell+DIRECTIONS[i]):
			mask |= 1<<i
	return mask

static func material_uv(point: Vector2) -> Vector2:
	# Mirrored four-cell spans meet on identical source pixels. No source edit
	# and no assumption that generation produced a perfectly tileable texture.
	point = (point+Vector2(1.0,2.0))/4.0
	return Vector2(1.0-absf(fposmod(point.x,2.0)-1.0),1.0-absf(fposmod(point.y,2.0)-1.0))

static func edges(cell: Vector2i, mask: int) -> Array[PackedVector2Array]:
	var corners := [Vector2.ZERO,Vector2.RIGHT,Vector2.ONE,Vector2.DOWN]
	for i in range(4):
		# Connected boundaries always reach the shared lattice corner, ensuring
		# even L, T, holes and diagonal configurations cannot open internal cracks.
		if not (mask & (1<<i)) and not (mask & (1<<((i+3)%4))):
			corners[i] = corners[i].lerp(Vector2(0.5,0.5),0.20)
	var result: Array[PackedVector2Array] = []
	for side in range(4):
		var points := PackedVector2Array([corners[side]])
		if not (mask & (1<<side)):
			for step in range(1,7):
				var p: Vector2 = corners[side].lerp(corners[(side+1)%4],float(step)/7.0)
				var jitter := float(posmod(cell.x*31+cell.y*17+side*13+step*7,11))/110.0
				p -= Vector2(DIRECTIONS[side])*(0.025+jitter*0.45)
				points.append(p)
		points.append(corners[(side+1)%4])
		result.append(points)
	return result

func draw_into(canvas: CanvasItem, field: Dictionary, cell_size: float, time: float, selected: Vector2i, show_work_effects := true, only_cells: Array = [], skip_surface:=false) -> void:
	var art := texture()
	for cell in (field if only_cells.is_empty() else only_cells):
		if not is_rock(field,cell):
			continue
		var rock: Dictionary = field[cell]
		var mask := connections(field,cell)
		var boundary := edges(cell,mask)
		var polygon := PackedVector2Array()
		var uv := PackedVector2Array()
		for side in boundary:
			for i in range(side.size()-1):
				polygon.append((Vector2(cell)+side[i])*cell_size)
				uv.append(material_uv(Vector2(cell)+side[i]))
		# Generated source has partial alpha throughout. An opaque stone backing
		# prevents seabed props from showing through; source pixels stay untouched.
		if not skip_surface:
			canvas.draw_colored_polygon(polygon,Color("18383e"))
			canvas.draw_polygon(polygon,PackedColorArray([Color(0.73,0.85,0.86)]),uv,art)
		# A continuous geological grade, independent of excavation state or cell masks.
		# Vertex alpha agrees on shared boundaries; mineral-rich eastern rock keeps
		# exactly the existing blocked-cell geometry, payment and clearance rules.
		var mineral := EnvironmentArt.texture("mineral-surface")
		if mineral != null:
			var grade := PackedColorArray()
			var visible_grade := false
			for point in polygon:
				grade.append(Color(.73,.85,.86,smoothstep(19.0,25.0,point.x/cell_size)))
				visible_grade = visible_grade or grade[-1].a > 0.0
			# Zero at every vertex means zero across every interpolated triangle.
			if not skip_empty_minerals or visible_grade:
				canvas.draw_polygon(polygon,grade,uv,mineral)
		for side in range(4):
			if mask & (1<<side):
				continue
			var cliff := PackedVector2Array()
			var ridge := PackedVector2Array()
			for point in boundary[side]:
				cliff.append((Vector2(cell)+point)*cell_size)
				# Keep all relief within the blocked cell, away from new rooms.
				ridge.append((Vector2(cell)+point.lerp(Vector2(0.5,0.5),0.13))*cell_size)
			var strip := cliff.duplicate()
			for i in range(ridge.size()-1,-1,-1):
				strip.append(ridge[i])
			if not EnvironmentArt.cliff(canvas,cliff,ridge,Color(.45,.55,.56) if side in [1,2] else Color(.72,.82,.80)):
				canvas.draw_colored_polygon(strip,Color(0.035,0.10,0.13,0.80 if side in [1,2] else 0.43))
			canvas.draw_polyline(ridge,Color(0.43,0.56,0.54,0.55 if side in [0,3] else 0.24),cell_size*0.009)
		var rect := Rect2(Vector2(cell)*cell_size,Vector2.ONE*cell_size)
		var fraction := float(rock.progress)/Field.DURATION
		if fraction>0:
			var crack := PackedVector2Array()
			for i in range(1+roundi(fraction*6)):
				crack.append(rect.position+Vector2(0.24+i*0.075,0.35+float(i%2)*0.13)*cell_size)
			var crack_art:=EnvironmentArt.texture("excavation-crack")
			if crack_art!=null:
				canvas.draw_texture_rect_region(crack_art,Rect2(rect.position+Vector2(.24,.33)*cell_size,Vector2(.45*fraction,.18)*cell_size),Rect2(Vector2.ZERO,Vector2(crack_art.get_width()*fraction,crack_art.get_height())))
			if crack_art==null and crack.size()>1:
				canvas.draw_polyline(crack,Color(0.025,0.07,0.08,0.85),cell_size*0.012)
			var bar := Rect2(rect.position+Vector2(0.14,0.86)*cell_size,Vector2(0.72,0.018)*cell_size)
			canvas.draw_rect(bar,Color("14282b"))
			bar.size.x *= fraction
			canvas.draw_rect(bar,Color("9eafa0"))
		if rock.active and show_work_effects:
			var at := rect.position+Vector2(0.3+0.4*fmod(time*0.15,1.0),0.48)*cell_size
			if not EnvironmentArt.sprite(canvas,"cut-glow",at,Vector2.ONE*cell_size*.038,Color(.53,.75,.72,.35+sin(time*8)*.12)):
				canvas.draw_circle(at,cell_size*0.019,Color(0.53,0.75,0.72,0.35+sin(time*8)*0.12))
			for i in range(6):
				var age := fmod(time*0.6+i/6.0,1.0)
				if not EnvironmentArt.sprite(canvas,"sediment-puff",at+Vector2(-age*.13,sin(i*2.1)*age*.1)*cell_size,Vector2.ONE*cell_size*(.008+age*.018),Color(.37,.47,.43,(1-age)*.55)):
					canvas.draw_circle(at+Vector2(-age*0.13,sin(i*2.1)*age*0.1)*cell_size,cell_size*(0.004+age*0.009),Color(0.37,0.47,0.43,(1.0-age)*0.55))
	draw_selection(canvas,field,cell_size,selected)

static func draw_selection(canvas: CanvasItem, field: Dictionary, cell_size: float, selected: Vector2i) -> void:
	if is_rock(field,selected):
		var outline := Rect2(Vector2(selected)*cell_size,Vector2.ONE*cell_size).grow(-cell_size*0.012)
		canvas.draw_rect(outline,Color("c39861"),false,cell_size*0.006)
