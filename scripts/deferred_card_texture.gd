extends Texture2D
## Immutable card pixels, including authored mip levels. CPU reads stay independent;
## the first actual display owns one ordinary ImageTexture for the session.
var uploaded_texture:ImageTexture
var _packed:=PackedByteArray()
var _raw_bytes:=0
var _dimensions:=Vector2i.ZERO
var _format:=Image.FORMAT_RGBA8
var _mipmaps:=false
var _mipmap_count:=0
var _alpha:=true
func configure(image:Image) -> void:
	if _raw_bytes!=0:
		push_error("Card pixels are already configured")
		return
	_dimensions=image.get_size();_format=image.get_format()
	_mipmaps=image.has_mipmaps();_mipmap_count=image.get_mipmap_count()
	_alpha=image.detect_alpha()!=Image.ALPHA_NONE
	var bytes:=image.get_data()
	_raw_bytes=bytes.size();_packed=bytes.compress(FileAccess.COMPRESSION_ZSTD)
func cpu_storage_bytes() -> int:return _packed.size()
func pixel_storage_bytes() -> int:return _raw_bytes
func _get_width() -> int:return _dimensions.x
func _get_height() -> int:return _dimensions.y
func _has_alpha() -> bool:return _alpha
func _has_mipmaps() -> bool:return _mipmaps
func _get_mipmap_count() -> int:return _mipmap_count
func _get_image() -> Image:
	if uploaded_texture!=null:return uploaded_texture.get_image()
	var pixels:=_packed.decompress(_raw_bytes,FileAccess.COMPRESSION_ZSTD)
	if pixels.size()!=_raw_bytes:
		push_error("Invalid retained card pixels")
		return null
	return Image.create_from_data(_dimensions.x,_dimensions.y,_mipmaps,_format,pixels)
func _get_rid() -> RID:
	if uploaded_texture==null:
		var image:=_get_image()
		if image==null:return RID()
		uploaded_texture=ImageTexture.create_from_image(image)
		# GPU-backed cards keep the original ImageTexture public-image path.
		# Retaining both compressed staging and that texture would raise the
		# eventual all-cards-shown working set above the previous policy.
		_packed=PackedByteArray()
	return uploaded_texture.get_rid()
