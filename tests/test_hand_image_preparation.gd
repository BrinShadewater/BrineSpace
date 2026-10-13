extends SceneTree
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(value:bool,label:String):
	checks+=1
	if not value:failures+=1;push_error(label)
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var queue=load("res://scripts/hand_image_preparation.gd")
	var file:=FileAccess.open("res://assets/department-floors-v1/habitation-composite.png",FileAccess.READ)
	var header:PackedByteArray=file.get_buffer(33)
	check(queue.estimated_bytes(header,file.get_length())>0,"Valid source rejected")
	for mutation in ["zero","huge","16bit","chunk","compression","oversized-file","short"]:
		var altered:PackedByteArray=header.duplicate();var length:int=file.get_length()
		match mutation:
			"zero":altered[16]=0;altered[17]=0;altered[18]=0;altered[19]=0
			"huge":for i in range(16,24):altered[i]=255
			"16bit":altered[24]=16
			"chunk":altered[12]=0
			"compression":altered[26]=1
			"oversized-file":length=queue.MAX_BYTES+1
			"short":altered.resize(24)
		check(queue.estimated_bytes(altered,length)==0,"Header guard failed: "+mutation)
	var floor:="res://assets/department-floors-v1/habitation-composite.png"
	var wall:="res://assets/room-risers-v4/masters/galley.png"
	var third:="res://legacy/default/assets/galley-directional-v1/serving-south.png"
	queue.maintain([floor,wall,third])
	check(queue.jobs.size()==2,"More than two jobs or expected jobs missing")
	check(queue.reserved_bytes<=queue.MAX_BYTES,"Reservation limit exceeded")
	var started:=Time.get_ticks_msec()
	while queue.jobs.values().any(func(job):return not WorkerThreadPool.is_task_completed(job.task)):
		if Time.get_ticks_msec()-started>10000:push_error("Decode timeout");queue.clear();quit(3);return
		await process_frame
	for path in [floor,wall]:
		var actual:Image=queue.take(path)
		var reference:=Image.new()
		check(reference.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK,"Reference source failed")
		check(actual!=null and actual.get_data()==reference.get_data() and actual.get_format()==reference.get_format() and actual.get_size()==reference.get_size() and actual.has_mipmaps()==reference.has_mipmaps(),"Prepared image differs from original decoded storage")
	check(queue.jobs.is_empty() and queue.reserved_bytes==0,"Consumed images remain retained")
	queue.maintain([floor,wall]);queue.maintain([])
	started=Time.get_ticks_msec()
	while not queue.jobs.is_empty():
		queue.maintain([])
		if Time.get_ticks_msec()-started>10000:queue.clear();quit(3);return
		await process_frame
	check(queue.reserved_bytes==0 and queue.unused==2,"Unused images not discarded after hand change")
	queue.maintain([floor,wall]);queue.clear()
	check(queue.jobs.is_empty() and queue.reserved_bytes==0,"Scene exit retains outstanding work")
	check(queue.take(floor)==null,"Absent preparation changes synchronous fallback")
	for i in range(100):
		queue.maintain([floor,wall] if i%3==0 else [third] if i%3==1 else [])
		check(queue.jobs.size()<=queue.MAX_JOBS,"Rapid hand switch exceeds task count")
		check(queue.reserved_bytes>=0 and queue.reserved_bytes<=queue.MAX_BYTES,"Rapid hand switch breaks reservation")
		await process_frame
	queue.maintain([])
	started=Time.get_ticks_msec()
	while not queue.jobs.is_empty():
		queue.maintain([])
		if Time.get_ticks_msec()-started>10000:queue.clear();quit(3);return
		await process_frame
	check(queue.reserved_bytes==0,"Rapid switches leave decoded storage")
	queue.enabled=false;queue.maintain([floor,wall]);check(queue.jobs.is_empty(),"Reference mode submits work")
	FileAccess.open("user://queue-results.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"stats":queue.stats()},"\t"))
	print("HAND IMAGE QUEUE ",checks," checks; ",failures," failures")
	quit(0 if failures==0 else 1)
