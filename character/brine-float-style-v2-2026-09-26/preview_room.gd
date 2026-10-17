extends "res://rooms/underwater/brine-core/brine_core_view.gd"
var room_id: String="brine_core"
var float_texture: ImageTexture
var float_mesh: ArrayMesh
func _ready() -> void:
	var floors=preload("res://rooms/whole-room/room_floor.gd")
	floors.profile_for(self)
	floors.floor_profiles[get_script().resource_path]=floors.floor_profiles.get("res://rooms/underwater/brine-core/brine_core_view.gd",{}).duplicate(true)
	super._ready()
	var im:=Image.new()
	if im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/brine-float-style-v2-2026-09-26/body.png")) != OK:
		push_error("Preview image could not be loaded")
		return
	float_texture=ImageTexture.create_from_image(im)
func drift(uv: Vector2,t: float) -> Vector2:
	var phase:=TAU*t/8.0
	var y:=uv.y
	var arm:=smoothstep(0.16,0.38,absf(uv.x-0.5)) * sin(PI*clampf((y-0.22)/0.42,0,1))
	var legs:=smoothstep(0.60,1.0,y)
	var hair: float=(1.0-smoothstep(0.08,0.22,y))*smoothstep(0.12,0.35,absf(uv.x-0.5))
	return Vector2(1.4*sin(phase)+arm*2.0*sin(phase+uv.x*2.0)+legs*2.4*sin(phase+1.2)+hair*1.2*sin(phase+0.7),3.2*sin(phase-0.4)+arm*0.7*sin(phase+1.0)+legs*0.8*sin(phase+uv.x*2.0))
func draw_prop_occupant(prop: Dictionary) -> void:
	if prop.id!="brine_chamber":
		super.draw_prop_occupant(prop)
		return
	if float_texture==null: return
	var t: float=machine_clock if operating and pod_power()>0 else 0.0
	var ratio: float=float_texture.get_width()/float(float_texture.get_height())
	var h:=168.0
	var rect:=Rect2(Vector2(626-ratio*h/2,593),Vector2(ratio*h,h))
	var verts:=PackedVector2Array()
	var uvs:=PackedVector2Array()
	var indices:=PackedInt32Array()
	for row in range(25):
		for col in range(11):
			var uv:=Vector2(col/10.0,row/24.0)
			var pt:=rect.position+uv*rect.size+drift(uv,t)
			verts.append(life_point(prop,pt))
			uvs.append(uv)
	for row in range(24):
		for col in range(10):
			var a:=row*11+col
			indices.append_array(PackedInt32Array([a,a+1,a+12,a,a+12,a+11]))
	var arrays:=[]
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX]=verts
	arrays[Mesh.ARRAY_TEX_UV]=uvs
	arrays[Mesh.ARRAY_INDEX]=indices
	var mesh:=ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
	float_mesh=mesh
	var tint:=Color(0.9,0.95,0.98,1)*lerpf(0.12,1.0,pod_power())
	tint.a=1
	painter.draw_mesh(mesh,float_texture,Transform2D.IDENTITY,tint)

