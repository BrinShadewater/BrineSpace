extends RefCounted
## Interface fonts (owner playtest, Sept 17: the monospace interface read as too blocky). Menus,
## the HUD and cards use Barlow Semi Condensed, bundled under the SIL Open Font License
## (assets/fonts/OFL.txt). The station log and other terminal readouts keep a monospace face, so
## numbers stay aligned and BRINE still sounds like a machine. Missing files fall back to the
## system fonts the game used before.

const REGULAR := "res://assets/fonts/BarlowSemiCondensed-Regular.ttf"
const MEDIUM := "res://assets/fonts/BarlowSemiCondensed-Medium.ttf"
const SEMIBOLD := "res://assets/fonts/BarlowSemiCondensed-SemiBold.ttf"
# Windows faces first, then macOS (Menlo, SF Mono), then the generic family so any system keeps columns aligned.
const MONO_NAMES := ["Cascadia Mono", "Consolas", "Lucida Console", "Menlo", "SF Mono", "monospace"]

static var _cache := {}
static var _card_theme: Theme

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

# Cards rotate and grow on hover. Keep a separate cached distance-field face so
# their transforms do not resample small bitmap glyphs or alter the rest of the UI.
static func card_theme() -> Theme:
	if _card_theme != null: return _card_theme
	_card_theme = apply(Theme.new())
	var regular := _card_font(interface_font())
	_card_theme.default_font = regular
	_card_theme.set_font("normal_font", "RichTextLabel", regular)
	_card_theme.set_font("bold_font", "RichTextLabel", _card_font(interface_bold()))
	_card_theme.set_font("font", "Button", _card_font(interface_medium()))
	return _card_theme

static func _card_font(source: Font) -> Font:
	if not source is FontFile: return source
	var font: FontFile = source.duplicate()
	font.multichannel_signed_distance_field = true
	font.msdf_size = 48
	return font
