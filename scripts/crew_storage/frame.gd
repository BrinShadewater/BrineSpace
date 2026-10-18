extends Texture2D
## Private experiment: immutable lossless pixels; decoding returns independent Images.
var packed:=PackedByteArray()
var raw_bytes:=0
var dimensions:=Vector2i.ZERO
var pixel_format:=Image.FORMAT_RGBA8
var mipmaps:=false
var mipmap_count:=0
var _checkpoint_packed_digest:=PackedByteArray()
var _checkpoint_layout:Array=[]
var _checkpoint_digest:=""
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

func checkpoint_rgba_sha256()->String:
	# Keep the existing checkpoint hash of hex-encoded image bytes. Never retain a
	# decoded Image. Exact compressed-byte and layout checks also catch tool edits.
	var layout:Array=[raw_bytes,dimensions,pixel_format,mipmaps]
	var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(packed)
	var packed_digest:=hash.finish()
	if not _checkpoint_digest.is_empty() and layout==_checkpoint_layout and packed_digest==_checkpoint_packed_digest:
		return _checkpoint_digest
	_checkpoint_digest=get_image().get_data().hex_encode().sha256_text()
	_checkpoint_layout=layout
	# Detect aliased in-place edits without retaining a second frame payload.
	_checkpoint_packed_digest=packed_digest
	return _checkpoint_digest
