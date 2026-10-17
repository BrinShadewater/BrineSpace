extends Texture2D
## A single-colour drone effect sheet held as a lossless LA8 mask. The original PNG bytes
## loaded with it stay immutable, so the public image and the lazy fallback never reread disk.
var source:String
var original_png:=PackedByteArray()
var width:int
var height:int
var mask:ImageTexture
var original:ImageTexture
var base_bytes:int
var storage_changed:Callable
var upload_record:Callable
func _get_width()->int:return width
func _get_height()->int:return height
func _has_alpha()->bool:return true
func _get_image()->Image:
	var image:=Image.new()
	if original_png.is_empty():return null
	if image.load_png_from_buffer(original_png)!=OK:return null
	return image
func original_texture()->Texture2D:
	if original==null:
		var image:Image=_get_image()
		if image==null:push_error("Native effect and original artwork unavailable: "+source);return null
		var started:int=Time.get_ticks_usec()
		original=ImageTexture.create_from_image(image)
		if upload_record.is_valid():upload_record.call(image.get_data_size(),Time.get_ticks_usec()-started,started,image.get_size())
		if storage_changed.is_valid():storage_changed.call(base_bytes+image.get_data_size())
	return original
func _get_rid()->RID:
	var texture:Texture2D=original_texture()
	return texture.get_rid() if texture!=null else RID()
