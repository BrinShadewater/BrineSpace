extends RefCounted
const Field := preload("res://scripts/wreck_field.gd")
const ROOT := "res://assets/environment/wrecked-rooms-v1/"
var textures: Dictionary = {}

func texture(kind: String, stage: String) -> Texture2D:
	var key := kind+"-"+stage
	if not textures.has(key):
		var path := ROOT+key+"-v1.png"
		var image := Image.new()
		if FileAccess.file_exists(path) and image.load(path)==OK:
			textures[key] = ImageTexture.create_from_image(image)
		else:
			return null
	return textures[key]

func draw_into(canvas: CanvasItem, wrecks: Dictionary, cell_size: float, time: float, selected: Vector2i, show_work_effects := true) -> void:
	for cell in wrecks:
		var w: Dictionary = wrecks[cell]
		if w.kind in ["basalt", "cryo"]:
			continue # Connected terrain is drawn by RockView, without a hull foundation.
		var rect := Rect2(Vector2(cell)*cell_size,Vector2.ONE*cell_size)
		var t := float(w.progress)/Field.DURATION
		var inner := rect.grow(-cell_size*0.035)
		# A flat remaining foundation, not a functioning hull or doorway.
		canvas.draw_rect(inner,Color(0.12,0.19,0.20,0.38),false,cell_size*0.018)
		if w.cleared:
			continue
		var full := texture(w.kind,"wreck")
		var stripped := texture(w.kind,"stripped")
		var strip_mix := smoothstep(0.38,0.50,t)
		var remaining := 1.0-smoothstep(0.84,0.98,t)
		if full != null:
			canvas.draw_texture_rect(full,rect,false,Color(0.72,0.82,0.83,remaining))
		if stripped != null:
			# Edits returned opaque exterior backgrounds. Use only the registered
			# inner floor; the original transparent hull owns the entire perimeter.
			var interior := Rect2(Vector2(0.085,0.115),Vector2(0.825,0.765))
			var dest := Rect2(rect.position+interior.position*cell_size,interior.size*cell_size)
			var source := Rect2(interior.position*stripped.get_size(),interior.size*stripped.get_size())
			canvas.draw_texture_rect_region(stripped,dest,source,Color(0.72,0.82,0.83,strip_mix*remaining))
		if cell == selected:
			canvas.draw_rect(rect.grow(-cell_size*0.008),Color("c39861"),false,cell_size*0.006)
		if w.active and show_work_effects:
			# Local underwater cutting light and small detached pieces; no fire.
			var at := rect.position+Vector2(0.25+0.5*fmod(time*0.12,1.0),0.52)*cell_size
			canvas.draw_circle(at,cell_size*0.018,Color(0.51,0.87,0.88,0.3+0.2*sin(time*7.0)))
			for i in range(5):
				var p := fmod(time*0.35+i*0.2,1.0)
				canvas.draw_rect(Rect2(at+Vector2(-p*0.12,sin(i*2.0)*0.03)*cell_size,Vector2.ONE*cell_size*0.008),Color(0.50,0.59,0.56,1.0-p))
		if w.progress>0:
			var bar := Rect2(rect.position+Vector2(0.12,0.91)*cell_size,Vector2(0.76,0.018)*cell_size)
			canvas.draw_rect(bar,Color("14282b"))
			bar.size.x *= t
			canvas.draw_rect(bar,Color("78b8ac"))
