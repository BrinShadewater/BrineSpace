extends RefCounted
## Isolated experiment. begin_draw is called inside the owner's _draw, after
## Godot clears that canvas's old commands. Other canvases retain their leases.
var bank
var capacity:=128
var cache_byte_limit:int=64*1024*1024
var cache_bytes:int=0
var cache_clock:int=0
var evictions:int=0
var slots:Array=[]
var owners:Dictionary={}
var owner_slots:Dictionary={}
var spills:Dictionary={}
var owner_spills:Dictionary={}
var spill_allocations:=0
var spill_peak_bytes:=0
var uploads:=0
var replacements:=0
var rejected:=0
# Bounded aggregate diagnostics. Durations are CPU wall intervals, not GPU execution.
var decode_total_usec:int=0
var decode_max_usec:int=0
var submit_total_usec:int=0
var submit_max_usec:int=0
var acquire_calls:int=0
var cache_hits:int=0
var decoded_count:int=0
var decoded_bytes:int=0
func decode_image(frame:Texture2D)->Image:
	var started:int=Time.get_ticks_usec()
	var image:Image=bank.source_image(frame)
	var duration:int=Time.get_ticks_usec()-started
	decode_total_usec+=duration;decode_max_usec=maxi(decode_max_usec,duration)
	decoded_count+=1;decoded_bytes+=image.get_data_size()
	return image
func record_submit(duration:int):
	submit_total_usec+=duration;submit_max_usec=maxi(submit_max_usec,duration)
func diagnostics_snapshot(clear:bool=false)->Dictionary:
	var result:Dictionary={"acquire_calls":acquire_calls,"cache_hits":cache_hits,"decoded_count":decoded_count,"decoded_bytes":decoded_bytes,"decode_total_usec":decode_total_usec,"decode_max_usec":decode_max_usec,"submit_total_usec":submit_total_usec,"submit_max_usec":submit_max_usec,"slot_count":slots.size(),"spill_count":spills.size(),"cache_bytes":cache_bytes,"cache_byte_limit":cache_byte_limit,"evictions":evictions}
	result.merge({"capacity":capacity,"uploads":uploads,"spill_allocations":spill_allocations,"spill_peak_source_bytes":spill_peak_bytes,"owner_count":owners.size()})
	if clear:
		acquire_calls=0;cache_hits=0;decoded_count=0;decoded_bytes=0
		decode_total_usec=0;decode_max_usec=0;submit_total_usec=0;submit_max_usec=0
	return result
func begin_draw(owner:CanvasItem):
	var id:int=owner.get_instance_id()
	if not owners.has(id):
		owners[id]=weakref(owner)
		owner.tree_exited.connect(release_owner.bind(id),CONNECT_ONE_SHOT)
	clear_leases(id)
func clear_leases(id:int):
	for index in owner_slots.get(id,[]):slots[index].holders.erase(id)
	owner_slots[id]=[]
	for key in owner_spills.get(id,[]):
		spills[key].holders.erase(id)
		# Reuse an immutable pose if another draw requests it before frame end.
	owner_spills[id]=[]
func release_owner(id:int):
	clear_leases(id);owner_slots.erase(id);owner_spills.erase(id);owners.erase(id)
	if owners.is_empty():slots.clear();spills.clear();cache_bytes=0
func oldest_free_slot()->int:
	var selected:int=-1
	for index in slots.size():
		if slots[index].frame==null or not slots[index].holders.is_empty():continue
		if selected<0 or slots[index].last_used<slots[selected].last_used:selected=index
	return selected
func drop_slot(index:int):
	assert(slots[index].holders.is_empty())
	cache_bytes-=int(slots[index].bytes);evictions+=1
	slots[index]={"texture":null,"display":null,"frame":null,"holders":{},"bytes":0,"last_used":0}
func empty_slot()->int:
	for index in slots.size():
		if slots[index].frame==null:return index
	return -1
func acquire(owner:CanvasItem,frame:Texture2D)->Texture2D:
	acquire_calls+=1
	var id:int=owner.get_instance_id()
	assert(owner_slots.has(id))
	if spills.has(frame.get_instance_id()):return spill(owner,frame)
	var index:int=-1
	for candidate in slots.size():
		if slots[candidate].frame==frame:index=candidate;cache_hits+=1;break
	if index<0:
		var image:Image=decode_image(frame)
		var size_bytes:int=image.get_data_size()
		if size_bytes>cache_byte_limit:return spill_image(owner,frame,image)
		while cache_bytes+size_bytes>cache_byte_limit:
			var old:int=oldest_free_slot()
			if old<0:return spill_image(owner,frame,image)
			drop_slot(old)
		index=empty_slot()
		if index<0 and slots.size()>=capacity:
			index=oldest_free_slot()
			if index<0:return spill_image(owner,frame,image)
			drop_slot(index)
		if index<0:
			index=slots.size();slots.append({})
		# Never overwrite pixels in a previously submitted GPU texture. Cache
		# eviction releases only unleased entries; held canvas commands stay valid.
		var started:int=Time.get_ticks_usec()
		var texture:=ImageTexture.create_from_image(image)
		var display:=CanvasTexture.new();display.diffuse_texture=texture
		record_submit(Time.get_ticks_usec()-started);uploads+=1
		for key in frame.get_meta_list():display.set_meta(key,frame.get_meta(key))
		display.texture_filter=frame.texture_filter if frame is CanvasTexture else CanvasItem.TEXTURE_FILTER_PARENT_NODE
		slots[index]={"texture":texture,"display":display,"frame":frame,"holders":{},"bytes":size_bytes,"last_used":0}
		cache_bytes+=size_bytes
	cache_clock+=1;slots[index].last_used=cache_clock
	slots[index].holders[id]=true
	if not owner_slots[id].has(index):owner_slots[id].append(index)
	return slots[index].display
func spill(owner:CanvasItem,frame:Texture2D)->Texture2D:
	return spill_image(owner,frame,null)
func spill_image(owner:CanvasItem,frame:Texture2D,supplied:Image)->Texture2D:
	# The reusable pool is bounded. Excess visible poses receive immutable
	# temporary images, held only by their current canvas commands, never evicted.
	var key:int=frame.get_instance_id();var id:int=owner.get_instance_id()
	if not spills.has(key):
		var image:Image=supplied if supplied!=null else decode_image(frame);var started:=Time.get_ticks_usec()
		var texture:=ImageTexture.create_from_image(image);var display:=CanvasTexture.new()
		display.diffuse_texture=texture
		for meta in frame.get_meta_list():display.set_meta(meta,frame.get_meta(meta))
		display.texture_filter=frame.texture_filter if frame is CanvasTexture else CanvasItem.TEXTURE_FILTER_PARENT_NODE
		record_submit(Time.get_ticks_usec()-started);uploads+=1;spill_allocations+=1
		spills[key]={"texture":texture,"display":display,"holders":{},"bytes":image.get_data_size()}
		var live_bytes:=0
		for item in spills.values():live_bytes+=int(item.bytes)
		spill_peak_bytes=maxi(spill_peak_bytes,live_bytes)
	spills[key].holders[id]=true
	if not owner_spills[id].has(key):owner_spills[id].append(key)
	return spills[key].display

func finish_frame():
	# All canvas draws are submitted. Images still held by retained commands stay.
	for key in spills.keys():
		if spills[key].holders.is_empty():spills.erase(key)
