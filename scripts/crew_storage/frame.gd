extends Texture2D
## Private experiment: immutable lossless pixels; decoding returns independent Images.
var packed:=PackedByteArray()
var raw_bytes:=0
var dimensions:=Vector2i.ZERO
var pixel_format:=Image.FORMAT_RGBA8
var mipmaps:=false
var mipmap_count:=0
var source:Image:
	get:
		var pixels:=packed.decompress(raw_bytes,FileAccess.COMPRESSION_ZSTD)
		assert(pixels.size()==raw_bytes)
		return Image.create_from_data(dimensions.x,dimensions.y,mipmaps,pixel_format,pixels)
	set(image):
		assert(packed.is_empty(),"Compressed source pixels are immutable")
		dimensions=image.get_size();pixel_format=image.get_format()
		mipmaps=image.has_mipmaps();mipmap_count=image.get_mipmap_count()
		var pixels:=image.get_data();raw_bytes=pixels.size()
		packed=pixels.compress(FileAccess.COMPRESSION_ZSTD)
func _get_width()->int:return dimensions.x
func _get_height()->int:return dimensions.y
func _get_format()->int:return pixel_format
func _has_mipmaps()->bool:return mipmaps
func _get_mipmap_count()->int:return mipmap_count
func _get_image()->Image:return source
