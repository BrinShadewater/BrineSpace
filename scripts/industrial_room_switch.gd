extends Button
## Generated housing with a mechanically animated rocker; Button retains keyboard input.
var art: ImageTexture
var amount := 0.0
var room_mode := false

func _ready() -> void:
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/playtest-visual-v1/switch-source.png")) == OK:
		art = ImageTexture.create_from_image(image)
	set_process(true)

func _process(delta: float) -> void:
	room_mode = text in ["SUSPEND ROOM", "RESUME ROOM"]
	var target := 1.0 if text == "SUSPEND ROOM" else 0.0
	amount = move_toward(amount, target, delta / 0.18)
	queue_redraw()

func _draw() -> void:
	if not room_mode or art == null: return
	# Cover the inherited action label only for room operation, never salvage/repair.
	draw_rect(Rect2(Vector2.ZERO,size),Color("121b1e"))
	var box := Rect2(5,2,82,size.y-4)
	draw_texture_rect_region(art,box,Rect2(130,32,1730,730),Color(0.78,0.80,0.79))
	var rocker := Rect2(34,10-amount*2,25,15+amount*2)
	draw_rect(Rect2(32,7,29,23),Color("101517"))
	draw_texture_rect_region(art,rocker,Rect2(750,287,475,237),Color(0.65,0.69,0.67))
	draw_line(rocker.position,rocker.position+Vector2(25,0),Color("86908b"),1)
	draw_rect(Rect2(41,6,11,2),Color("41453a").lerp(Color("b3a16b"),amount))
	var label := "ROOM ON" if text == "SUSPEND ROOM" else "ROOM OFF"
	var ink := Color("b8c4bd") if not disabled else Color("626c68")
	draw_string(get_theme_default_font(),Vector2(96,size.y*0.5+5),label,HORIZONTAL_ALIGNMENT_LEFT,size.x-100,14,ink)
	if has_focus(): draw_rect(Rect2(Vector2.ONE,size-Vector2.ONE*2),Color("8eaaa0"),false,1)
