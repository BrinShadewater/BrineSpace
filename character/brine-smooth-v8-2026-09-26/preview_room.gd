extends "res://rooms/underwater/brine-core/brine_core_view.gd"
var room_id: String="brine_core"
var float_texture: ImageTexture
var float_mesh: ArrayMesh
var body_layer: FloatLayer
var front_layer: FloatLayer
var overlay_pass:=false
class FloatLayer extends Node2D:
	var host
	var prop: Dictionary
	var foreground:=false
	func _draw() -> void:
		if prop.is_empty(): return
		var previous=host.painter
		host.painter=self
		if foreground:
			host.overlay_pass=true
			host.draw_prop_glass(prop)
			host.draw_prop_bubbles(prop)
			host.draw_prop_front(prop)
			host.overlay_pass=false
		else: host.draw_smooth_body(prop)
		host.painter=previous
func _ready() -> void:
	var floors=preload("res://rooms/whole-room/room_floor.gd")
	floors.profile_for(self)
	floors.floor_profiles[get_script().resource_path]=floors.floor_profiles.get("res://rooms/underwater/brine-core/brine_core_view.gd",{}).duplicate(true)
	super._ready()
	var im:=Image.new()
	if im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/brine-face-v7-2026-09-26/body.png")) != OK:
		push_error("Preview image could not be loaded")
		return
	float_texture=ImageTexture.create_from_image(im)
func drift(uv: Vector2,t: float) -> Vector2:
	var phase:=TAU*t/8.0
	var y:=uv.y
	var arm:=smoothstep(0.16,0.38,absf(uv.x-0.5))*smoothstep(0.22,0.43,y)*(1.0-smoothstep(0.54,0.68,y))
	var legs:=smoothstep(0.60,1.0,y)
	# Head and face translate as one rigid region: no differential deformation
	# across eyes or mouth. Limbs lag the body with smooth spatial envelopes.
	var body:=Vector2(0.9*sin(phase),2.8*sin(phase-0.4))
	var follow:=smoothstep(0.18,0.30,y)
	var side_phase:=0.7 if uv.x<0.5 else 1.0
	var limbs:=Vector2(arm*1.2*sin(phase+side_phase)+legs*1.4*sin(phase+0.75),arm*0.35*sin(phase+0.8)+legs*0.45*sin(phase+0.9))
	return body+limbs*follow
func draw_prop_occupant(prop: Dictionary) -> void:
	if prop.id!="brine_chamber":
		super.draw_prop_occupant(prop)
		return
	if body_layer==null:
		body_layer=FloatLayer.new()
		body_layer.host=self
		body_layer.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
		painter.add_child(body_layer)
		front_layer=FloatLayer.new()
		front_layer.host=self
		front_layer.foreground=true
		front_layer.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		painter.add_child(front_layer)
	for layer in [body_layer,front_layer]:
		layer.prop=prop
		layer.position=view_origin
		layer.scale=Vector2.ONE*view_scale
		layer.queue_redraw()
func draw_prop_glass(prop: Dictionary) -> void:
	if prop.id!="brine_chamber" or overlay_pass: super.draw_prop_glass(prop)
func draw_prop_bubbles(prop: Dictionary) -> void:
	if prop.id!="brine_chamber" or overlay_pass: super.draw_prop_bubbles(prop)
func draw_prop_front(prop: Dictionary) -> void:
	if prop.id!="brine_chamber" or overlay_pass: super.draw_prop_front(prop)
func draw_smooth_body(prop: Dictionary) -> void:
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
	var tint:=Color.WHITE*lerpf(0.12,1.0,pod_power())
	tint.a=1
	painter.draw_mesh(mesh,float_texture,Transform2D.IDENTITY,tint)






