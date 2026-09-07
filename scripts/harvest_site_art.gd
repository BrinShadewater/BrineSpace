extends RefCounted
## Reuse audited, unchanged source sprites; depletion removes whole grounded pieces.
const SOURCES := {
	"mining":"res://assets/environment/sub-biomes-v1/nodules-nodule-cluster-v1.png",
	"frame":"res://assets/environment/service-wreckage-v1/collapsed-support-v1.png",
	"cable":"res://assets/environment/service-wreckage-v1/torn-cable-harness-v1.png"
}
var textures := {}
func texture(id: String) -> Texture2D:
	if not textures.has(id):
		var image := Image.new()
		assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes(SOURCES[id]))==OK)
		textures[id] = ImageTexture.create_from_image(image)
	return textures[id]

func draw_site(canvas: CanvasItem, site: Dictionary, center: Vector2, size: float, selected: bool) -> void:
	var fraction := float(site.units)/float(site.capacity)
	var pieces := ceili(fraction*4.0)
	var positions := [Vector2(-0.12,0.08),Vector2(0.19,0.13),Vector2(0.06,-0.13),Vector2(-0.22,-0.15)]
	var widths := [0.48,0.30,0.34,0.23]
	canvas.draw_set_transform(center,0,Vector2(1,0.48))
	canvas.draw_circle(Vector2.ZERO,size*0.34,Color(0.035,0.065,0.06,0.32))
	canvas.draw_set_transform(Vector2.ZERO)
	for i in range(pieces-1,-1,-1):
		var source := "mining" if site.kind=="mining" else "frame" if i%2==0 else "cable"
		var art := texture(source)
		var dimensions := Vector2(widths[i]*size,widths[i]*size*art.get_height()/art.get_width())
		canvas.draw_texture_rect(art,Rect2(center+positions[i]*size-dimensions*0.5,dimensions),false,Color(0.78,0.88,0.85))
	var color := Color("91ae82") if site.kind=="mining" else Color("c29b72")
	# Small survey corners distinguish finite contacts from decorative seabed scatter.
	for side in [-1,1]:
		var at := center+Vector2(side*0.39,-0.31)*size
		canvas.draw_line(at,at+Vector2(-side*0.09,0)*size,color,1.0)
		canvas.draw_line(at,at+Vector2(0,0.09)*size,color,1.0)
	if selected:
		canvas.draw_rect(Rect2(center-Vector2.ONE*size*0.46,Vector2.ONE*size*0.92),color,false,1.5)
		var text := "DEPLETED" if pieces==0 else "%d LOADS" % site.units
		canvas.draw_string(ThemeDB.fallback_font,center+Vector2(-0.35,0.42)*size,text,HORIZONTAL_ALIGNMENT_CENTER,size*0.7,maxi(9,roundi(size*0.085)),color)

func draw_into(canvas: CanvasItem, sites: Dictionary, occupied: Dictionary, cell_size: float, selected: Vector2i) -> void:
	for cell in sites:
		if not sites[cell].discovered or occupied.has(cell): continue
		draw_site(canvas,sites[cell],(Vector2(cell)+Vector2.ONE*0.5)*cell_size,cell_size,cell==selected)
