extends RefCounted
## Dedicated transit, utility and observation walls for straight and turning routes.
const NAMES=["transit","utility","observation","reinforced","service","acoustic","sage","clay","slate","panoramic","ribbed","bulkhead"]
static var records: Dictionary={}
static var textures: Dictionary={}
static func key(turning: bool, variant: int, junction: bool=false) -> String:
	return ("tee-" if junction else "corner-" if turning else "straight-")+NAMES[posmod(variant,NAMES.size())]
static func catalog() -> Dictionary:
	if records.is_empty():
		records=JSON.parse_string(FileAccess.get_file_as_string("res://assets/corridor-risers-v2/registrations.json"))
	return records
static func texture(id: String) -> Texture2D:
	if not textures.has(id):
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, catalog()[id].source)
		textures[id]=ImageTexture.create_from_image(image)
	return textures[id]
static func region(id: String, part: String) -> Rect2:
	var r: Array=catalog()[id][part]
	return Rect2(r[0],r[1],r[2],r[3])
# Preserve cap texture aspect on narrow corridor tops/returns.
static func fitted_cap(canvas: CanvasItem, id: String, points: PackedVector2Array, light: float) -> void:
	var source:=region(id,"cap")
	var length:=points[0].distance_to(points[1])
	var depth:=points[1].distance_to(points[2])
	if length<=0 or depth<=0: return
	var scale:=depth/source.size.y
	var count:=maxi(1,ceili(length/(source.size.x*scale)))
	for i in range(count):
		var a:=float(i)/count
		var b:=float(i+1)/count
		var crop:=source
		crop.size.x=length/count/scale
		crop.position.x+=(source.size.x-crop.size.x)*0.5
		var quad:=PackedVector2Array([points[0].lerp(points[1],a),points[0].lerp(points[1],b),points[3].lerp(points[2],b),points[3].lerp(points[2],a)])
		var uv:=PackedVector2Array([crop.position,Vector2(crop.end.x,crop.position.y),crop.end,Vector2(crop.position.x,crop.end.y)])
		for j in range(4): uv[j]/=Vector2(texture(id).get_size())
		canvas.draw_polygon(quad,PackedColorArray([Color(light,light,light)]),uv,texture(id))
static func polygon(canvas: CanvasItem, id: String, points: PackedVector2Array, part: String, light: float) -> void:
	if part=="cap" and catalog()[id].get("fitted_caps",false):
		fitted_cap(canvas,id,points,light)
		return
	var r:=region(id,part)
	var uv:=PackedVector2Array([r.position,Vector2(r.end.x,r.position.y),r.end,Vector2(r.position.x,r.end.y)])
	for i in range(4):uv[i]/=Vector2(texture(id).get_size())
	canvas.draw_polygon(points,PackedColorArray([Color(light,light,light)]),uv,texture(id))
# Shared panel bays own both the cladding and fitting reservations.
static func fitting_bays(target: Rect2, variant: int) -> Array[Rect2]:
	var inner:=target.grow(-7)
	if target.size.x>=190:inner.size.x-=62
	if posmod(variant,3)==0 and inner.size.x>=125:
		return [Rect2(inner.position,Vector2(38,inner.size.y)),Rect2(inner.position+Vector2(46,0),Vector2(inner.size.x-46,inner.size.y))]
	return [inner]

static func face(canvas: CanvasItem, id: String, target: Rect2, light: float) -> void:
	var variant:int=NAMES.find(id.get_slice("-",1))
	if catalog()[id].has("glazing"):
		draw_glazing(canvas,id,target,light,variant>=10)
		return
	# Keep ribs at bay boundaries instead of repeating a rib beneath a window.
	solid(canvas,id,target,light)
	var bays:=fitting_bays(target,variant)
	if target.size.x>=190:bays.append(Rect2(target.end.x-65,target.position.y+7,58,target.size.y-14))
	for bay in bays:
		var source:=region(id,"panel" if catalog()[id].has("panel") else "low")
		draw_panel(canvas,id,bay,source,light)
		var rib:=Rect2(bay.position.x-4,target.position.y,3,target.size.y)
		canvas.draw_texture_rect_region(texture(id),rib,region(id,"return"),Color(light,light,light))
	var end_rib:=Rect2(target.end.x-6,target.position.y,3,target.size.y)
	canvas.draw_texture_rect_region(texture(id),end_rib,region(id,"return"),Color(light,light,light))
	if variant==1:
		# Protected services run below the viewing bay, never through the glazing.
		canvas.draw_texture_rect_region(texture(id),Rect2(target.position.x+7,target.end.y-12,target.size.x-14,9),Rect2(80,453,1608,54),Color(light,light,light))
	if catalog()[id].has("vent"):
		canvas.draw_texture_rect_region(texture(id),Rect2(target.position.x+7,target.end.y-11,target.size.x-14,7),region(id,"vent"),Color(light,light,light))
static func cap(canvas: CanvasItem, id: String, target: Rect2, light: float) -> void:
	if catalog()[id].get("fitted_caps",false):
		fitted_cap(canvas,id,PackedVector2Array([target.position,Vector2(target.end.x,target.position.y),target.end,Vector2(target.position.x,target.end.y)]),light)
		return
	canvas.draw_texture_rect_region(texture(id),target,region(id,"cap"),Color(light,light,light))

static func solid(canvas: CanvasItem, id: String, target: Rect2, light: float) -> void:
	canvas.draw_texture_rect_region(texture(id),target,region(id,"low"),Color(light,light,light))

static func closed_entry(canvas: CanvasItem, wall: Rect2, light: float) -> void:
	var finish=preload("res://rooms/doors/door_finish.gd")
	if finish.preview_art!=null:
		finish.preview_art.raised_at(canvas,finish.preview_art.progress,wall.get_center().x,wall.position.y+8,wall.size.y-8)
		return
	preload("res://rooms/doors/painted_door.gd").for_variant("hallway").raised_at(canvas,0,wall.get_center().x,wall.position.y+8,wall.size.y-8)

static var detail_texture: Texture2D
static func detail(canvas: CanvasItem, wall: Rect2, variant: int, light: float) -> void:
	if wall.size.x<190:return
	if detail_texture==null:
		var im:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(im,"res://assets/corridor-risers-v2/wall-details.png")
		detail_texture=ImageTexture.create_from_image(im)
	var regions: Array[Rect2]=[Rect2(56,146,680,401),Rect2(792,153,643,396),Rect2(1496,152,623,403)]
	var source:Rect2=regions[posmod(variant,3)]
	var size:=source.size*minf(52/source.size.x,36/source.size.y)
	var center:=Vector2(wall.end.x-36,wall.position.y+27)
	canvas.draw_texture_rect_region(detail_texture,Rect2(center-size*.5,size),source,Color(light,light,light))

# Expansive ocean glazing replaces the solid face; short bays crop the panorama.
static var tunnel_texture: Texture2D
static func draw_glazing(canvas: CanvasItem, id: String, target: Rect2, light: float, ribbed: bool) -> void:
	if tunnel_texture==null:
		var im:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(im,"res://assets/corridor-risers-v2/tunnel-glass.png")
		tunnel_texture=ImageTexture.create_from_image(im)
	var source:=region(id,"glazing")
	source=glazing_crop(source,target.size)
	canvas.draw_texture_rect_region(tunnel_texture,target,source,Color(light,light,light))
	var heavy:bool=catalog()[id].get("bulkhead",false)
	var frame_width:=8.0 if heavy else 3.0
	for x in [target.position.x,target.end.x-frame_width]:
		canvas.draw_texture_rect_region(texture(id),Rect2(x,target.position.y,frame_width,target.size.y),region(id,"return"),Color(light,light,light))
	var rail_height:=5.0 if heavy else 3.0
	for y in [target.position.y,target.end.y-rail_height]:
		canvas.draw_texture_rect_region(texture(id),Rect2(target.position.x,y,target.size.x,rail_height),region(id,"cap"),Color(light,light,light))
	if ribbed:
		var count:=maxi(2,ceili(target.size.x/95.0))
		for i in range(1,count):
			canvas.draw_texture_rect_region(texture(id),Rect2(target.position.x+target.size.x*i/count-frame_width*0.5,target.position.y,frame_width,target.size.y),region(id,"return"),Color(light,light,light))

	# Each pane has a continuous recessed rubber seal inside its metal surround.
	var panes:=maxi(2,ceili(target.size.x/95.0)) if ribbed else 1
	for i in range(panes):
		var left:=target.position.x+target.size.x*i/panes+(frame_width if i==0 else frame_width*0.5)
		var right:=target.position.x+target.size.x*(i+1)/panes-(frame_width if i==panes-1 else frame_width*0.5)
		var opening:=Rect2(left,target.position.y+rail_height,right-left,target.size.y-rail_height*2)
		canvas.draw_rect(opening,Color("151c1e")*Color(light,light,light),false,2.0)

# Uniform sampling: retain a 60-unit scene height even on the low cutaway.
static func glazing_crop(source: Rect2, size: Vector2) -> Rect2:
	var scale_value:=maxf(size.x/source.size.x,60.0/source.size.y)
	var crop_size:=size/scale_value
	return Rect2(source.position+Vector2((source.size.x-crop_size.x)*0.5,source.size.y-crop_size.y),crop_size)

# Repeat a calibrated material sample, cropping the last span without stretching.
static func draw_panel(canvas: CanvasItem, id: String, target: Rect2, source: Rect2, light: float) -> void:
	var scale_value:=46.0/source.size.y
	var span:=source.size.x*scale_value
	var offset:=0.0
	while offset<target.size.x-0.001:
		var width:=minf(span,target.size.x-offset)
		var crop:=Rect2(source.position,Vector2(width/scale_value,target.size.y/scale_value))
		canvas.draw_texture_rect_region(texture(id),Rect2(target.position+Vector2(offset,0),Vector2(width,target.size.y)),crop,Color(light,light,light))
		offset+=width
