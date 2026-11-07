extends SceneTree
const NPC=preload("res://scripts/companion_npc.gd")
const Art=preload("res://scripts/margot_cryo_art.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func pixels(actor,boot:float,started:bool,recovered:bool,reduced:bool)->PackedByteArray:
 Art.cache.clear()
 return Art.texture(actor,boot,started,recovered,Vector2(0,28),reduced).get_image().get_data()
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 root.set_meta("tablet_controls",true)
 var candidate=NPC.new("margot")
 var still=pixels(candidate,0.0,false,false,false)
 check(not candidate.art_loaded,"Frozen tablet pod must not load all companion animation banks")
 check(candidate._player.frames.is_empty() and candidate._poses.frames.is_empty(),"Ordinary companion banks stay absent until needed")
 check(candidate.pod_player.frames.is_empty() and candidate.pod_poses.frames.keys()==["nap-south"],"Only the frozen pod clip is resident")
 var reference=NPC.new("margot");reference._load_art()
 check(still==pixels(reference,0.0,false,false,false),"Frozen pod pixels exact")
 for reduced in [false,true]:
  for boot in [0.0,0.6,1.99,2.0,2.8,3.79,3.8,4.2,4.79,4.8,5.4,6.59,6.6,7.8,8.0]:
   check(pixels(candidate,boot,true,false,reduced)==pixels(reference,boot,true,false,reduced),"Thaw pixels exact "+str([boot,reduced]))
 check(not candidate.art_loaded,"Pod thaw does not load unrelated water/action banks")
 check(pixels(candidate,8.0,true,true,false)==pixels(reference,8.0,true,true,false),"Recovered pod pixels exact")
 check(candidate.pod_player.frames.keys()==["idle-south","walk-south"] and candidate.pod_poses.frames.keys()==["nap-south","nap-exit-south"],"Only demanded thaw clips resident")
 candidate._load_art()
 check(candidate.pod_player.frames.is_empty() and candidate.pod_poses.frames.is_empty(),"Full loading releases pod aliases")
 for pair in [[candidate.player,reference.player],[candidate.poses,reference.poses]]:
  check(pair[0].timing==pair[1].timing and pair[0].strides==pair[1].strides,"Later full companion clocks/stride unchanged")
  check(pair[0].frames.keys()==pair[1].frames.keys(),"Later full companion clips unchanged")
  for key in pair[0].frames:
   check(pair[0].frames[key].size()==pair[1].frames[key].size(),"Frame slots unchanged "+key)
   for i in pair[0].frames[key].size():
    var a:Texture2D=pair[0].frames[key][i];var b:Texture2D=pair[1].frames[key][i]
    check(a.get_image().get_data()==b.get_image().get_data(),"Full companion source pixels exact "+key+str(i))
    for meta in b.get_meta_list():check(a.get_meta(meta)==b.get_meta(meta),"Frame metadata exact "+str(meta))
 root.set_meta("tablet_controls",false)
 var desktop=NPC.new("margot");pixels(desktop,0.0,false,false,false);check(desktop.art_loaded,"Desktop keeps full loading")
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"Pod source art available")
 print("TABLET COMPANION POD STORAGE failures=",failures);quit(1 if failures else 0)
