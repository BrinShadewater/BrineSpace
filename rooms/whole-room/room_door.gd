extends RefCounted
## Two leaves retract into code-owned jambs; no second bitmap frame.
const OPENING := 72.0

static func riser_leaf_rects(open_amount: float) -> Array:
	var rise=preload("res://rooms/whole-room/riser_geometry.gd")
	var width:=OPENING*.5*(1.0-clampf(open_amount,0,1))
	if width<=0: return []
	return [Rect2(-36,rise.TOP,width,rise.HEIGHT+8),Rect2(36-width,rise.TOP,width,rise.HEIGHT+8)]

static func draw_riser_door(canvas: CanvasItem, open_amount: float, ceramic: Texture2D=null, variant: String="generic") -> void:
	preload("res://rooms/doors/door_finish.gd").raised(canvas,open_amount,"brine" if ceramic!=null else variant)

static func riser_detail(canvas: CanvasItem, detail: Rect2, clip: Rect2, color: Color) -> void:
	var visible:=detail.intersection(clip)
	if visible.has_area(): canvas.draw_rect(visible,color)

static func riser_surface(canvas: CanvasItem, detail: Rect2, clip: Rect2, ceramic: Texture2D=null) -> void:
	var visible:=detail.intersection(clip)
	if not visible.has_area(): return
	# A quiet interior patch of the adjacent hull supplies the same painted finish.
	var texture:=preload("res://assets/riser-wall-kit-style-v2/wall_sprites.gd").texture("hull_infill_panel")
	var source:=Rect2(150,45,105,76)
	if ceramic!=null:
		texture=ceramic
		source=Rect2(820,125,330,180)
	var start: Vector2=(visible.position-detail.position)/detail.size
	var extent: Vector2=visible.size/detail.size
	canvas.draw_texture_rect_region(texture,visible,Rect2(source.position+start*source.size,extent*source.size),Color.WHITE if ceramic!=null else Color(.69,.74,.70))
static func leaf_rects(open_amount: float) -> Array:
	var width := OPENING*0.5*(1.0-clampf(open_amount,0,1))
	if width<=0: return []
	return [Rect2(-36,-6,width,12),Rect2(36-width,-6,width,12)]
static func draw_door(canvas: CanvasItem, open_amount: float) -> void:
	for i in range(leaf_rects(open_amount).size()):
		var panel: Rect2=leaf_rects(open_amount)[i]
		preload("res://rooms/doors/door_finish.gd").low_leaf(canvas,panel,i==0,false,"generic")
	for side in [-1,1]:
		canvas.draw_rect(Rect2(side*39-2,-6,4,12),Color("627e7b"))
		canvas.draw_rect(Rect2(side*39-1,-2,2,4),Color("91b7ae"))
