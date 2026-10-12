extends RefCounted
const MAX_JOBS:=2
const MAX_BYTES:=16*1024*1024
static var enabled:=not OS.get_cmdline_user_args().has("--reference-hand-image-preparation")
static var jobs:Dictionary={}
static var reserved_bytes:=0
static var submitted:=0
static var hits:=0
static var unused:=0
static var peak_bytes:=0
static var failures:=0
static func maintain(wanted:Array) -> void:
	for path in jobs.keys():
		if path not in wanted and WorkerThreadPool.is_task_completed(jobs[path].task):discard(path)
	if not enabled:return
	for path in wanted:
		if jobs.has(path) or jobs.size()>=MAX_JOBS:continue
		var file:=FileAccess.open(path,FileAccess.READ)
		if file==null:continue
		var bytes:int=estimated_bytes(file.get_buffer(33),file.get_length())
		if bytes<=0 or bytes>MAX_BYTES-reserved_bytes:continue
		var result:Dictionary={}
		var task:int=WorkerThreadPool.add_task(func():
			var image:=Image.new()
			if image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK:result.image=image)
		jobs[path]={"task":task,"result":result,"bytes":bytes}
		reserved_bytes+=bytes;submitted+=1;peak_bytes=maxi(peak_bytes,reserved_bytes)
static func take(path:String) -> Image:
	if not enabled or not jobs.has(path) or not WorkerThreadPool.is_task_completed(jobs[path].task):return null
	var job:Dictionary=jobs[path]
	WorkerThreadPool.wait_for_task_completion(job.task)
	jobs.erase(path);reserved_bytes-=int(job.bytes)
	var image:Image=job.result.get("image")
	if image==null:failures+=1
	else:hits+=1
	return image
static func discard(path:String) -> void:
	var job:Dictionary=jobs[path]
	WorkerThreadPool.wait_for_task_completion(job.task)
	jobs.erase(path);reserved_bytes-=int(job.bytes);unused+=1
static func clear() -> void:
	for path in jobs.keys():discard(path)
static func stats() -> Dictionary:
	return {"submitted":submitted,"hits":hits,"unused":unused,"failures":failures,"pending":jobs.size(),"reserved_bytes":reserved_bytes,"peak_reserved_bytes":peak_bytes}

static func estimated_bytes(header:PackedByteArray,encoded_bytes:int) -> int:
	if encoded_bytes<33 or encoded_bytes>MAX_BYTES or header.size()!=33:return 0
	if header.slice(0,8)!=PackedByteArray([137,80,78,71,13,10,26,10]):return 0
	if header.slice(8,16)!=PackedByteArray([0,0,0,13,73,72,68,82]):return 0
	if header[24] not in [1,2,4,8] or header[25] not in [0,2,3,4,6]:return 0
	if header[25] in [2,4,6] and header[24]!=8:return 0
	if header[26]!=0 or header[27]!=0 or header[28]>1:return 0
	var width:int=(int(header[16])<<24)|(int(header[17])<<16)|(int(header[18])<<8)|int(header[19])
	var height:int=(int(header[20])<<24)|(int(header[21])<<16)|(int(header[22])<<8)|int(header[23])
	# Bound each factor before multiplying: crafted dimensions must not overflow.
	if width<=0 or height<=0 or width>MAX_BYTES/4 or height>MAX_BYTES/4:return 0
	var estimate:int=width*height*4
	return estimate if estimate<=MAX_BYTES else 0
