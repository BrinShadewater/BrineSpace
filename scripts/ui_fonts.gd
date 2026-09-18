extends RefCounted
## Interface fonts (owner playtest, Sept 17: the monospace interface read as too blocky). Menus,
## the HUD and cards use Barlow Semi Condensed, bundled under the SIL Open Font License
## (assets/fonts/OFL.txt). The station log and other terminal readouts keep a monospace face, so
## numbers stay aligned and BRINE still sounds like a machine. Missing files fall back to the
## system fonts the game used before.

const REGULAR := "res://assets/fonts/BarlowSemiCondensed-Regular.ttf"
const MEDIUM := "res://assets/fonts/BarlowSemiCondensed-Medium.ttf"
const SEMIBOLD := "res://assets/fonts/BarlowSemiCondensed-SemiBold.ttf"
const MONO_NAMES := ["Cascadia Mono", "Consolas", "Lucida Console"]

static var _cache := {}

static func _load(path: String) -> Font:
	if _cache.has(path): return _cache[path]
	var font: Font = null
	if ResourceLoader.exists(path): font = load(path)
	if font == null:
		var fallback := SystemFont.new()
		fallback.font_names = PackedStringArray(["Segoe UI", "Arial", "sans-serif"])
		font = fallback
	_cache[path] = font
	return font

static func interface_font() -> Font: return _load(REGULAR)
static func interface_medium() -> Font: return _load(MEDIUM)
static func interface_bold() -> Font: return _load(SEMIBOLD)

static func mono_font() -> Font:
	if _cache.has("mono"): return _cache["mono"]
	var font := SystemFont.new()
	font.font_names = PackedStringArray(MONO_NAMES)
	_cache["mono"] = font
	return font

# Fills a theme's default font and the bold/italic slots rich text uses.
static func apply(theme: Theme, size := 17) -> Theme:
	theme.default_font = interface_font()
	theme.default_font_size = size
	theme.set_font("bold_font", "RichTextLabel", interface_bold())
	theme.set_font("normal_font", "RichTextLabel", interface_font())
	theme.set_font("mono_font", "RichTextLabel", mono_font())
	theme.set_font("font", "Button", interface_medium())
	return theme
