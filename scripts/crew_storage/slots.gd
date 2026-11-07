extends RefCounted
## Isolated experiment. begin_draw is called inside the owner's _draw, after
## Godot clears that canvas's old commands. Other canvases retain their leases.
var bank
const CpuFrame=preload("res://scripts/crew_storage/frame.gd")
var share_sources:=not OS.get_cmdline_user_args().has("--reference-crew-source-sharing")
var display_alias_limit:=8
var release_hidden_commands:=not OS.get_cmdline_user_args().has("--reference-hidden-crew-leases")
var hidden_command_retirements:=0
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
	var result:Dictionary={"source_sharing":share_sources,"display_alias_limit":display_alias_limit,"acquire_calls":acquire_calls,"cache_hits":cache_hits,"decoded_count":decoded_count,"decoded_bytes":decoded_bytes,"decode_total_usec":decode_total_usec,"decode_max_usec":decode_max_usec,"submit_total_usec":submit_total_usec,"submit_max_usec":submit_max_usec,"slot_count":slots.size(),"spill_count":spills.size(),"cache_bytes":cache_bytes,"cache_byte_limit":cache_byte_limit,"evictions":evictions}
	var hidden_owners:=0;var hidden_leases:=0;var inspected:=0
	for id in owners:
		if inspected>=512:break
		inspected+=1
		var owner:CanvasItem=owners[id].get_ref()
		if owner!=null and not owner.is_visible_in_tree():
			hidden_owners+=1;hidden_leases+=owner_slots.get(id,[]).size()+owner_spills.get(id,[]).size()
	result.merge({"hidden_owners":hidden_owners,"hidden_owner_leases":hidden_leases,"owner_scan_complete":inspected==owners.size()})
	result.merge({"capacity":capacity,"hidden_command_retirements":hidden_command_retirements,"visibility_retirement_enabled":release_hidden_commands,"uploads":uploads,"spill_allocations":spill_allocations,"spill_peak_source_bytes":spill_peak_bytes,"owner_count":owners.size()})
	if clear:
		acquire_calls=0;cache_hits=0;decoded_count=0;decoded_bytes=0
		decode_total_usec=0;decode_max_usec=0;submit_total_usec=0;submit_max_usec=0
	return result
func begin_draw(owner:CanvasItem):
	var id:int=owner.get_instance_id()
	if not owners.has(id):
		owners[id]=weakref(owner)
		owner.tree_exited.connect(release_owner.bind(id),CONNECT_ONE_SHOT)
		if release_hidden_commands:owner.visibility_changed.connect(retire_hidden_commands.bind(id))
	clear_leases(id)
func clear_leases(id:int):
	for index in owner_slots.get(id,[]):slots[index].holders.erase(id)
	owner_slots[id]=[]
	for key in owner_spills.get(id,[]):
		spills[key].holders.erase(id)
		# Reuse an immutable pose if another draw requests it before frame end.
	owner_spills[id]=[]
func retire_hidden_commands(id:int):
	var owner:CanvasItem=owners[id].get_ref() if owners.has(id) else null
	if owner==null or owner.is_visible_in_tree():return
	# Clear the retained commands before giving up their immutable images.
	# Queueing while hidden makes reveal rebuild them from the CPU source.
	RenderingServer.canvas_item_clear(owner.get_canvas_item())
	clear_leases(id)
	owner.queue_redraw()
	hidden_command_retirements+=1
func release_owner(id:int):
	var owner:CanvasItem=owners[id].get_ref() if owners.has(id) else null
	var callback:Callable=retire_hidden_commands.bind(id)
	if owner!=null and owner.visibility_changed.is_connected(callback):owner.visibility_changed.disconnect(callback)
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
	var source:Texture2D=frame.diffuse_texture if frame is CanvasTexture else frame
	var storage_key:Texture2D=source if share_sources and source is CpuFrame else frame
	var filter:int=frame.texture_filter if frame is CanvasTexture else CanvasItem.TEXTURE_FILTER_PARENT_NODE
	var index:int=-1
	for candidate in slots.size():
		if slots[candidate].get("source")==storage_key and slots[candidate].get("filter")==filter:index=candidate;break
	if index>=0:
		# Bound the small sampler/metadata aliases independently of pixel storage.
		if not slots[index].displays.has(frame.get_instance_id()):
			if slots[index].displays.size()>=display_alias_limit:return spill(owner,frame)
			var alias:=CanvasTexture.new();alias.diffuse_texture=slots[index].texture;alias.texture_filter=filter
			for meta in frame.get_meta_list():alias.set_meta(meta,frame.get_meta(meta))
			slots[index].displays[frame.get_instance_id()]=alias
		cache_hits+=1
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
		slots[index]={"texture":texture,"display":display,"frame":frame,"source":storage_key,"filter":filter,"displays":{frame.get_instance_id():display},"holders":{},"bytes":size_bytes,"last_used":0}
		cache_bytes+=size_bytes
	cache_clock+=1;slots[index].last_used=cache_clock
	slots[index].holders[id]=true
	if not owner_slots[id].has(index):owner_slots[id].append(index)
	return slots[index].displays[frame.get_instance_id()]
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
