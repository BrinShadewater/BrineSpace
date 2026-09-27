extends RefCounted
## The approved 48-second habitat study, fitted inside registered tank glass.
const PATHS := {
	"skimmer":"res://assets/new-room-props-2026-09-26/animation-studies/aquarium/aquarium-preview/sprites/ribbon-skimmer.png",
	"bell":"res://assets/new-room-props-2026-09-26/animation-studies/aquarium/aquarium-preview/sprites/bell-grazer.png",
	"driftling":"res://assets/new-room-props-2026-09-26/animation-studies/aquarium/aquarium-preview/sprites/plated-driftling.png",
	"frond":"res://assets/new-room-props-2026-09-26/animation-studies/aquarium/aquarium-preview/sprites/spiral-frond.png",
	"weed":"res://assets/new-room-props-2026-09-26/animation-studies/aquarium/aquarium-preview/seaweed.png",
	"coral":"res://assets/new-room-props-2026-09-26/animation-studies/aquarium/aquarium-preview/coral.png",
	"bed":"res://assets/new-room-props-2026-09-26/animation-studies/aquarium/aquarium-preview/sand-rocks.png"
}
static var textures := {}
static var regions := {}
static func texture(id:String) -> Texture2D:
	if not textures.has(id):
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes(PATHS[id]))!=OK:return null
		textures[id]=ImageTexture.create_from_image(image)
		regions[id]=Rect2(image.get_used_rect())
	return textures[id]

static func patch(canvas, id:String, dest:Rect2, source:Rect2, clip:PackedVector2Array, flip:float=1.0) -> void:
	if dest.size.x<0.01 or dest.size.y<0.01:return
	var tex:=texture(id)
	var box:=PackedVector2Array([dest.position,Vector2(dest.end.x,dest.position.y),dest.end,Vector2(dest.position.x,dest.end.y)])
	for polygon in Geometry2D.intersect_polygons(box,clip):
		var uv:=PackedVector2Array()
		for p in polygon:
			var f:Vector2=(p-dest.position)/dest.size
			if flip<0:f.x=1-f.x
			uv.append((source.position+f*source.size)/Vector2(tex.get_size()))
		canvas.draw_polygon(polygon,PackedColorArray([Color.WHITE]),uv,tex)

static func plant(canvas,id:String,at:Vector2,height:float,phase:float,clip:PackedVector2Array) -> void:
	texture(id)
	var src:Rect2=regions[id]
	var width:=height*src.size.x/src.size.y
	for j in range(24):
		var f:=float(j)/24
		var bend:=sin(phase+f*1.5)*pow(1-f,2)*height*.055
		patch(canvas,id,Rect2(at+Vector2(-width/2+bend,-height+height*f),Vector2(width,height/24+.15)),Rect2(src.position+Vector2(0,src.size.y*f),Vector2(src.size.x,src.size.y/24+.5)),clip)

static func swimmer(canvas,id:String,at:Vector2,width:float,phase:float,flip:float,clip:PackedVector2Array) -> void:
	var tex:=texture(id)
	var size:=Vector2(tex.get_size())
	var height:=width*size.y/size.x
	var drawn_width:=width*absf(flip)
	for j in range(24):
		var f:=float(j)/24
		var x:=f if flip>=0 else 1-f-1.0/24
		var dy:=sin(phase+f*5)*height*.025
		patch(canvas,id,Rect2(at+Vector2(-drawn_width/2+x*drawn_width,-height/2+dy),Vector2(drawn_width/24+.08,height)),Rect2(Vector2(size.x*f,0),Vector2(size.x/24+.3,size.y)),clip,flip)

static func draw(room,prop:Dictionary) -> void:
	var data:Dictionary=prop.registration.aquarium
	var a:Array=data.window
	var rect:Rect2=prop.rect
	var r:=Rect2(rect.position+rect.size*Vector2(a[0],a[1]),rect.size*Vector2(a[2],a[3]))
	var round_tank:bool=data.get("round",false)
	var clip:=PackedVector2Array([r.position,Vector2(r.end.x,r.position.y),r.end,Vector2(r.position.x,r.end.y)])
	if round_tank:
		# Curved bottom follows the existing cylindrical glass, not the brass rim.
		clip=PackedVector2Array([r.position,Vector2(r.end.x,r.position.y),Vector2(r.end.x,r.end.y-r.size.y*.1)])
		for i in range(17):
			var t:=float(i)/16*PI
			clip.append(Vector2(r.get_center().x+cos(t)*r.size.x*.5,r.end.y-r.size.y*.1+sin(t)*r.size.y*.1))
	var p:=fposmod(float(room.machine_clock),48)/48*TAU
	var c=room.painter
	var w:=r.size.x
	var h:=r.size.y
	var unit:=w/(273.0 if round_tank else 506.0)
	if round_tank:patch(c,"bed",Rect2(Vector2(r.position.x-4*unit,r.end.y-52*unit),Vector2(w+8*unit,56*unit)),Rect2(150,510,1100,75),clip)
	var bed_w:=w*1.06
	var bed_h:=bed_w*332/1923
	patch(c,"bed",Rect2(r.position+Vector2(-w*.03,h-bed_h+5*unit),Vector2(bed_w,bed_h)),Rect2(33,309,1923,332),clip)
	if not round_tank:patch(c,"bed",Rect2(r.position+Vector2(w*.30,h-45*unit),Vector2(269,147)*.20*unit),Rect2(1366,403,269,147),clip)
	var offset:=1.0 if round_tank else 0.0
	var frond:=texture("frond")
	plant(c,"frond",r.position+Vector2(w*.20,h*.92),h*.31*frond.get_height()/frond.get_width(),p*4+offset,clip)
	plant(c,"weed",r.position+Vector2(w*.79,h-19*unit),h*.64,p*4+offset,clip)
	plant(c,"weed",r.position+Vector2(w*.11,h-15*unit),h*.48,p*4+offset+1.4,clip)
	texture("coral")
	var coral:Rect2=regions.coral
	var cw:=w*(.25 if round_tank else .16)
	var ch:=cw*coral.size.y/coral.size.x
	patch(c,"coral",Rect2(r.position+Vector2(w*(.44 if round_tank else .57)-cw/2,h-10*unit-ch),Vector2(cw,ch)),coral,clip)
	if round_tank:
		swimmer(c,"bell",r.position+Vector2(w*(.55+.08*sin(p)),h*(.35+.06*sin(p*2))),w*.52,p,1,clip)
	else:
		swimmer(c,"skimmer",r.position+Vector2(w*(.56+.18*sin(p)),h*(.29+.04*sin(p*2))),w*.34,p,-cos(p)/sqrt(pow(cos(p),2)+.08),clip)
		swimmer(c,"driftling",r.position+Vector2(w*(.47+.19*sin(p+2.4)),h*(.56+.045*sin(p*2+1))),w*.22,p+2.4,-cos(p+2.4)/sqrt(pow(cos(p+2.4),2)+.08),clip)
	c.draw_colored_polygon(clip,Color(0.118,0.216,0.255,.09))
