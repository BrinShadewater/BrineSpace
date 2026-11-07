extends Texture2D
## A drone cargo sheet held as cropped frames: only the area the cargo uses, with a one-pixel
## transparent border. Each frame becomes its own small texture the first time it is drawn.
## The original PNG bytes loaded with it stay immutable for the public image and the fallback.
var source:String
var original_png:=PackedByteArray()
var width:int
var height:int
var cropped:Image
# Tablet CPU storage is lossless and independently decodable per frame. Never
# decompress a whole atlas or upload it just to display one animation pose.
var packed_frames:Array[PackedByteArray]=[]
var packed_format:int=Image.FORMAT_RGBA8
var packed_frame_bytes:int=0
static func pack_image(image:Image,frame_size:Vector2i,columns:int)->Image:
	var carrier:=Image.create(1,1,false,Image.FORMAT_RGBA8)
	var invisible:=image.is_invisible()
	carrier.fill(Color(0,0,0,0) if invisible else Color.WHITE)
	for key in image.get_meta_list():carrier.set_meta(key,image.get_meta(key))
	if invisible:return carrier
	var packed:Array[PackedByteArray]=[]
	var bytes:=0
	for row in range(image.get_height()/frame_size.y):
		for column in columns:
			var frame:Image=image.get_region(Rect2i(Vector2i(column,row)*frame_size,frame_size))
			var pixels:PackedByteArray=frame.get_data().compress(FileAccess.COMPRESSION_ZSTD)
			packed.append(pixels);bytes+=pixels.size()
	carrier.set_meta("drone_packed_frames",packed)
	carrier.set_meta("drone_packed_format",image.get_format())
	carrier.set_meta("drone_packed_frame_bytes",image.get_region(Rect2i(Vector2i.ZERO,frame_size)).get_data_size())
	carrier.set_meta("drone_packed_bytes",bytes)
	return carrier
## Kept area inside one frame, border included.
var box:Rect2i
var cell:Vector2i
var columns:int
var frames:Dictionary={}
var frame_cache_limit:=0 # Desktop retains its existing policy.
var frame_order:Array[int]=[]
var frame_bytes:=0
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
func frame(index:int)->Texture2D:
	if frames.has(index):
		if frame_cache_limit>0:frame_order.erase(index);frame_order.append(index)
		return frames[index]
	if index<0 or columns<=0:return null
	if cropped==null and index>=packed_frames.size():return null
	var at:=Vector2i(index%columns,index/columns)*box.size
	if cropped!=null and at.y+box.size.y>cropped.get_height():return null
	var started:int=Time.get_ticks_usec()
	var image:Image
	if cropped!=null:image=cropped.get_region(Rect2i(at,box.size))
	else:
		var byte_count:int=packed_frame_bytes
		var pixels:PackedByteArray=packed_frames[index].decompress(byte_count,FileAccess.COMPRESSION_ZSTD)
		if pixels.size()!=byte_count:push_error("Invalid packed drone frame: "+source);return null
		image=Image.create_from_data(box.size.x,box.size.y,false,packed_format,pixels)
	frames[index]=ImageTexture.create_from_image(image)
	if frame_cache_limit>0:
		frame_order.append(index);frame_bytes+=image.get_data_size()
		while frame_order.size()>frame_cache_limit:
			var oldest:int=frame_order.pop_front()
			var retired:Texture2D=frames[oldest]
			frame_bytes-=retired.get_width()*retired.get_height()*4
			frames.erase(oldest)
		if storage_changed.is_valid():storage_changed.call(base_bytes+frame_bytes+(width*height*4 if original!=null else 0))
	if upload_record.is_valid():upload_record.call(image.get_data_size(),Time.get_ticks_usec()-started,started,image.get_size(),"frame")
	return frames[index]
func original_texture()->Texture2D:
	if original==null:
		var image:Image=_get_image()
		if image==null:push_error("Cargo storage and original artwork unavailable: "+source);return null
		var started:int=Time.get_ticks_usec()
		original=ImageTexture.create_from_image(image)
		if upload_record.is_valid():upload_record.call(image.get_data_size(),Time.get_ticks_usec()-started,started,image.get_size(),"original")
		if storage_changed.is_valid():storage_changed.call(base_bytes+image.get_data_size()+frame_bytes)
	return original
func _get_rid()->RID:
	var texture:Texture2D=original_texture()
	return texture.get_rid() if texture!=null else RID()
