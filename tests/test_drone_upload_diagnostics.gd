extends SceneTree
const Motion=preload("res://scripts/drone_animation.gd")
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(value:bool,label:String):
 checks+=1
 if not value:failures+=1;push_error(label)
func run():
 if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
 var initial:Dictionary=Motion.frame_upload_diagnostics()
 check(initial.uploads==0 and initial.bytes==0 and initial.events.is_empty(),"No uploads initially")
 var image:=Image.create(16,16,false,Image.FORMAT_RGBA8);image.fill(Color.WHITE)
 Motion.cache_image("fixture://large",image)
 var small:=Image.create(2,2,false,Image.FORMAT_RGBA8);small.fill(Color.WHITE)
 for i in range(11):Motion.cache_image("fixture://small/%d"%i,small)
 var report:Dictionary=Motion.frame_upload_diagnostics()
 var uploaded_frame:int=report.frame
 check(report.events[0].end_usec-report.events[0].start_usec==report.events[0].usec,"Upload interval matches measured duration")
 check(report.events[0].start_usec>0 and report.events[0].end_usec<=Time.get_ticks_usec(),"Upload interval uses the shared monotonic clock")
 check(report.uploads==12,"Counts all same-frame uploads")
 check(report.bytes==1024+11*16 and report.largest_bytes==1024,"Large upload survives subsequent small layers")
 check(report.events.size()==8 and not report.events_complete,"Detailed history bounded; totals complete")
 check(report.usec==Motion.texture_upload_usec and report.max_usec<=report.usec,"Timing totals include every upload")
 check(report.events[0].path=="fixture://large" and Motion.last_texture_upload.path=="fixture://small/10","First and legacy last event preserved")
 var identities:Dictionary=Motion.textures.duplicate()
 var total:=Motion.cached_bytes
 report.events[0].path="changed";report.events.clear()
 check(Motion.frame_upload_diagnostics().events[0].path=="fixture://large","Returned snapshot cannot mutate recorder")
 var diagnostics:=Motion.cache_diagnostics()
 check(diagnostics.frame_uploads.uploads==12,"Existing cache report contains additive frame diagnostics")
 check(Motion.cached_bytes==total and Motion.textures==identities,"Reporting does not evict or alter storage")
 check(diagnostics.observed_live_decoded_bytes==total and diagnostics.observed_live_unique_images==12,"Live weak storage counts unique images and exact decoded bytes")
 check(diagnostics.observed_uncached_live_decoded_bytes==0 and diagnostics.live_lookup_scan_complete and diagnostics.live_details_complete,"Bounded ownership report is complete for this fixture")
 Motion.textures.erase("fixture://large");Motion.texture_order.erase("fixture://large");Motion.texture_bytes.erase("fixture://large");Motion.cached_bytes-=1024
 var retained_report:=Motion.cache_diagnostics()
 check(retained_report.observed_live_decoded_bytes==total and retained_report.observed_uncached_live_decoded_bytes==1024,"Externally retained image remains visible after cache ownership drops")
 check(Motion.restore_live("fixture://large") and Motion.cached_bytes==total,"Report leaves weak restoration and accounting intact")
 check(retained_report.observed_live_details.size()==12,"Report returns bounded metadata details")

 await process_frame;await process_frame
 var next:Dictionary=Motion.frame_upload_diagnostics()
 check(Motion.frame_upload_diagnostics(uploaded_frame).uploads==12,"Explicit completed frame preserves uploads after process counter advances")
 check(next.uploads==0 and next.bytes==0 and next.events.is_empty() and next.events_complete,"Next frame does not report stale uploads")
 check(Motion.cache_diagnostics().latest_upload_frame.uploads==12 and Motion.cache_diagnostics().latest_upload_frame.frame<Engine.get_process_frames(),"Completed upload frame remains explicitly timestamped")
 check(Motion.texture_uploads==12 and Motion.last_texture_upload.path=="fixture://small/10","Lifetime counters and historical metadata unchanged")
 Motion.cache_image("fixture://next",small)
 check(Motion.frame_upload_diagnostics().uploads==1 and Motion.frame_upload_diagnostics().bytes==16,"Next frame begins independent collection")
 Motion.textures.clear();Motion.texture_order.clear();Motion.texture_bytes.clear();Motion.last_used.clear();Motion.cached_bytes=0
 FileAccess.open("user://results.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
 print("UPLOAD_DIAGNOSTICS ",checks," checks ",failures," failures");quit(1 if failures else 0)
