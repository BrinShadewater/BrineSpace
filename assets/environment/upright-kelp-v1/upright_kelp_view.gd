extends RefCounted
## Owner-requested upright grass silhouette; bottom holdfast is its ground anchor.
const SOURCES := {
	"sea-white-reed-kelp":"res://assets/environment/upright-kelp-v1/runtime/sea-white-reed-kelp.png",
	"violet-reed-kelp":"res://assets/environment/upright-kelp-v1/runtime/violet-reed-kelp.png",
	"emerald-reed-kelp":"res://assets/environment/upright-kelp-v1/runtime/emerald-reed-kelp.png"
}
const WIDTHS := {"emerald-reed-kelp":.28,"sea-white-reed-kelp":.30,"violet-reed-kelp":.28}
const HABITATS := {"kelp":["emerald-reed-kelp","sea-white-reed-kelp","violet-reed-kelp"],"sponge":["sea-white-reed-kelp"],"brine":["sea-white-reed-kelp"],"coral":["violet-reed-kelp"],"iron":["violet-reed-kelp"]}
var textures: Dictionary={}
var prepared:=false
const Settings := preload("res://scripts/title_settings.gd")
const SWAY_PERIOD := 8.0
const ROOT_LOCK := .92
const STRIPS := 16
func prepare() -> void:
	if prepared:return
	prepared=true
	for id in SOURCES:
		textures[id]=preload("res://scripts/safe_image.gd").raw_texture(SOURCES[id])
func draw_asset(canvas: CanvasItem,id: String,at: Vector2,width: float,tint:=Color(.59,.68,.66,.85)) -> void:
	prepare()
	var art: Texture2D=textures.get(id)
	if art==null:return
	var extent:=art.get_size()/float(art.get_width())*width
	canvas.draw_texture_rect(art,Rect2(at-extent*Vector2(.5,.97),extent),false,tint)
static func sway_offset(y: float,clock: float,phase: float) -> float:
	# The whole holdfast stays still. Bend increases smoothly toward the tips.
	if Settings.reduced_motion or Settings.effects_quality==0:return 0.0
	var height:=maxf(0.0,(ROOT_LOCK-y)/ROOT_LOCK)
	var angle:=fposmod(clock,SWAY_PERIOD)*TAU/SWAY_PERIOD
	return height*height*(.10*sin(angle+phase-height*.35)+.015*sin(angle*2.0+phase*1.7-height*.6))
func draw_swaying_asset(canvas: CanvasItem,id: String,at: Vector2,width: float,clock: float,phase: float,tint:=Color(.59,.68,.66,.85)) -> void:
	prepare()
	if Settings.reduced_motion or Settings.effects_quality==0:
		draw_asset(canvas,id,at,width,tint)
		return
	var art: Texture2D=textures.get(id)
	if art==null:return
	var extent:=art.get_size()/float(art.get_width())*width
	var origin:=at-extent*Vector2(.5,.97)
	# Shared UV/vertex edges keep painted detail continuous across the bend.
	# Submit the original ordered strip triangles together; retain float tint precision.
	var points:=PackedVector2Array();var uv:=PackedVector2Array();var indices:=PackedInt32Array()
	for row in range(STRIPS+1):
		var a:=float(row)/STRIPS*ROOT_LOCK
		var b:=float(row+1)/STRIPS*ROOT_LOCK if row<STRIPS else 1.0
		var top:=origin+Vector2(sway_offset(a,clock,phase)*width,a*extent.y)
		var bottom:=origin+Vector2(sway_offset(b,clock,phase)*width,b*extent.y)
		var base:int=points.size()
		points.append_array(PackedVector2Array([top,top+Vector2(width,0),bottom+Vector2(width,0),bottom]))
		uv.append_array(PackedVector2Array([Vector2(0,a),Vector2(1,a),Vector2(1,b),Vector2(0,b)]))
		indices.append_array(PackedInt32Array([base+3,base,base+1,base+1,base+2,base+3]))
	RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),indices,points,PackedColorArray([tint]),uv,PackedInt32Array(),PackedFloat32Array(),art.get_rid())
func placements(regions: Array) -> Array:
	var result: Array=[]
	for region in regions:
		var ids: Array=HABITATS.get(region.biome,[])
		for i in range(ids.size()):
			var at: Vector2=region.center+Vector2(-.20+i*.25,.65)*region.radius
			if at.distance_to(Vector2(20.5,20.5))<3.5:continue
			result.append({"id":ids[i],"at":at,"width":WIDTHS[ids[i]]})
	return result
func render_into(canvas: CanvasItem,cell_size: float,regions: Array,clock:=0.0,visible_rect:=Rect2()) -> void:
	prepare()
	for plant in placements(regions):
		if visible_rect.has_area():
			var art: Texture2D = textures.get(plant.id)
			if art == null: continue
			var width: float = float(plant.width)*cell_size
			var extent := art.get_size()/float(art.get_width())*width
			# The two sine terms can move tips by at most 11.5% of the width.
			# Include that full envelope, including when Reduced Motion changes.
			var bounds := Rect2(plant.at*cell_size-extent*Vector2(.5,.97),extent).grow(width*.115+1.0)
			if not visible_rect.intersects(bounds): continue
		var phase: float=plant.at.x*2.1+plant.at.y*.73
		draw_swaying_asset(canvas,plant.id,plant.at*cell_size,float(plant.width)*cell_size,clock,phase)
