extends SceneTree
const Icons = preload("res://scripts/ui_badge_icons.gd")
const LEGACY := {
	"metal": "res://brineui/hull-ui-v1/icons/metal.png",
	"oxygen": "res://brineui/hull-ui-v1/icons/oxygen.png",
	"water": "res://brineui/hull-ui-v1/icons/water.png",
	"power": "res://brineui/hull-ui-v1/icons/power.png",
	"freeze": "res://brineui/hull-ui-v1/icons/freeze.png",
	"repair": "res://brineui/hull-ui-v1/icons/repair.png",
	"hull_intact": "res://brineui/hull-ui-v1/icons/hull_intact.png",
	"doors_open": "res://brineui/hull-ui-v1/icons/doors_open.png",
	"health": "res://brineui/hull-ui-v1/icons/health.png",
	"fatigue": "res://brineui/hull-ui-v1/icons/fatigue.png",
	"hunger": "res://brineui/hull-ui-v1/icons/hunger.png",
	"working": "res://brineui/hull-ui-v1/icons/working.png",
	"archive": "res://brineui/hull-ui-v1/icons/archive.png",
	"diagnostics": "res://brineui/hull-ui-v1/icons/diagnostics.png",
	"journal": "res://brineui/hull-ui-v1/icons/journal.png",
	"warning": "res://brineui/hull-ui-v1/icons/warning.png",
}
func original(id: String) -> Texture2D:
	var image := Image.new()
	image.load_png_from_buffer(FileAccess.get_file_as_bytes(LEGACY[id]))
	return ImageTexture.create_from_image(image)
const Style = preload("res://scripts/title_button_style.gd")
var failures := 0
var checks := 0
func check(value: bool, message: String) -> void:
	checks += 1
	if not value:
		failures += 1
		push_error(message)
func _initialize() -> void: run.call_deferred()
func icon(texture: Texture2D, side: int) -> TextureRect:
	var node := TextureRect.new()
	node.texture = texture
	node.custom_minimum_size = Vector2(side,side)
	node.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	node.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	node.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	return node
func run() -> void:
	var viewport := SubViewport.new()
	viewport.size = Vector2i(1120,820)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var background := ColorRect.new()
	background.color = Color("0a1d25")
	background.size = viewport.size
	viewport.add_child(background)
	var body := VBoxContainer.new()
	body.theme = Style.menu_theme()
	body.position = Vector2(28,24)
	body.size = Vector2(1064,760)
	body.add_theme_constant_override("separation",18)
	viewport.add_child(body)
	var title := Label.new()
	title.text = "BADGE ICON DENSITY / BEFORE & AFTER"
	title.add_theme_font_size_override("font_size",28)
	body.add_child(title)
	var hint := Label.new()
	hint.text = "Each cell: original 64 px | redraw 64 px | redraw at native badge size"
	body.add_child(hint)
	var grid := GridContainer.new()
	grid.columns = 4
	grid.add_theme_constant_override("h_separation",24)
	grid.add_theme_constant_override("v_separation",20)
	body.add_child(grid)
	for id in ["metal","oxygen","water","power","freeze","repair","hull_intact","doors_open","health","fatigue","hunger","working","archive","diagnostics","journal","warning"]:
		var cell := VBoxContainer.new()
		grid.add_child(cell)
		var label := Label.new()
		label.text = id.replace("_"," ").to_upper()
		cell.add_child(label)
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation",12)
		cell.add_child(row)
		row.add_child(icon(original(id),64))
		row.add_child(icon(Icons.texture(id),64))
		row.add_child(icon(Icons.texture(id),26))
	for id in Icons.PATHS:
		var texture := Icons.texture(id)
		check(texture != null,"Registered badge icon loads: " + id)
		if texture != null:
			check(texture.get_width() == (128 if id == "archived_data" else 256),"High-density export size: " + id)
			check(texture.get_image().get_pixel(0,0).a == 0,"Transparent export gutter: " + id)
	for frame in range(5): await process_frame
	await RenderingServer.frame_post_draw
	check(grid.get_global_rect().end.y < 820,"Comparison fits viewport")
	check(viewport.get_texture().get_image().save_png("res://output/ui-badge-icons-2026-10-03/comparison.png") == OK,"Comparison saves")
	print("ICON DENSITY: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
