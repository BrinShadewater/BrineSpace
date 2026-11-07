extends RefCounted
## The sealed tablet Veld pod displays the selected idle-south frame zero only.
## Keep it with the grid, so title return releases its pixels with the session.
const SOURCE="res://character/crew-runtime-matte-v1/veld/frames/idle-south-breathing-v1/000.png"
const MANIFEST="res://character/crew-runtime-matte-v1/veld/manifest.json"
const CACHE_KEY="tablet_veld_pod_idle"
static func idle(grid:Node) -> Texture2D:
 if grid.has_meta(CACHE_KEY):return grid.get_meta(CACHE_KEY)
 var data:Variant=JSON.parse_string(FileAccess.get_file_as_string(MANIFEST))
 if not data is Dictionary:return null
 var image:=Image.new()
 if preload("res://scripts/safe_image.gd").load_png(image,SOURCE)!=OK:return null
 var shown:=CanvasTexture.new();shown.diffuse_texture=ImageTexture.create_from_image(image)
 shown.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR if data.get("textureFilter","nearest")=="linear" else CanvasItem.TEXTURE_FILTER_PARENT_NODE
 var pivot:Array=data.get("pivot",[46,86])
 shown.set_meta("crew_pivot",Vector2(float(pivot[0]),float(pivot[1])))
 shown.set_meta("crew_standing_height",float(data.get("standingHeight",74)))
 grid.set_meta(CACHE_KEY,shown)
 return shown
