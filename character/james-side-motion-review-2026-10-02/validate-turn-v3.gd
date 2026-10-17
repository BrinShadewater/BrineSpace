extends SceneTree
const OUT="res://character/james-side-motion-review-2026-10-02/"
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
class Board extends Node2D:
 var player
 var key:="carry-turn-east-north"
 var elapsed:=0.0
 func _draw():
  draw_rect(Rect2(0,0,1200,320),Color("303b40"))
  draw_string(ThemeDB.fallback_font,Vector2(12,24),"James staged East-connected turns / "+key,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
  for mode in range(2):
   var tex:Texture2D=player.frame_at_elapsed(key,elapsed,"" if mode==0 else "diving-helmet")
   for size_index in range(4):
    var heights:Array=[148.0,82.0,54.0,27.0];var factor:float=heights[size_index]/148.0
    var foot:=Vector2(100+size_index*150+mode*600,265)
    draw_texture_rect(tex,Rect2(foot-Vector2(128,224)*factor,tex.get_size()*factor),false)
func _initialize():call_deferred("run")
func run():
 if not "brine-james-native-" in OS.get_environment("APPDATA") or DisplayServer.get_name()=="headless":quit(3);return
 var player=load("res://scripts/crew_sprite_player.gd").new()
 player.load_manifest(OUT+"east-turn-v3-bare-manifest.json")
 check(player.load_equipment_manifest("diving-helmet",OUT+"east-turn-v3-helmet-manifest.json"),"Candidate paired helmet admission")
 for mode in ["bare","helmet"]:
  var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"east-turn-v3-"+mode+"-manifest.json"))
  var rows:Dictionary=player.frames if mode=="bare" else player.equipment_frames["diving-helmet"]
  for state in pack.states:
   var elapsed:=0.0
   for i in range(state.frameFiles.size()):
    var expected:=Image.load_from_file(OUT.path_join(state.frameFiles[i]).simplify_path())
    var tex:Texture2D=player.frame_at_elapsed(state.id,elapsed+.0001,"" if mode=="bare" else "diving-helmet")
    check(tex.get_image().get_data()==expected.get_data(),"Exact candidate source clock "+mode+state.id+str(i))
    check(tex.get_meta("crew_pivot")==Vector2(128,224),"Original pivot")
    check(tex.get_meta("crew_standing_height")==148.0,"Original ruler")
    elapsed+=state.frameDurationsMs[i]/1000.0
   var parts:Array=state.id.split("-")
   var reverse:String="carry-turn-"+parts[3]+"-"+parts[2]
   for i in range(state.frameFiles.size()):check(rows[state.id][i].get_image().get_data()==rows[reverse][state.frameFiles.size()-1-i].get_image().get_data(),"Exact paired reverse "+mode+state.id)

 var board:=Board.new();board.player=player;root.size=Vector2i(1200,320);root.content_scale_size=Vector2i.ZERO;root.add_child(board)
 DirAccess.make_dir_recursive_absolute(OUT+"turn-v3-native")
 var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"east-turn-v3-bare-manifest.json"));var captures:=0
 for state in pack.states:
  var elapsed:=0.0
  for i in range(state.frameFiles.size()):
   board.key=state.id;board.elapsed=elapsed+.0001;board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
   check(root.get_texture().get_image().save_png(OUT+"turn-v3-native/"+state.id+"-"+str(i).pad_zeros(3)+".png")==OK,"Native paired scale capture")
   captures+=1;elapsed+=state.frameDurationsMs[i]/1000.0
 var report:=FileAccess.open(OUT+"turn-v3-native-evidence.json",FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"scope":"Staged paired six-turn manifests through actual CrewSpritePlayer, exact92source-clock slots/pivot/ruler/reverse aliases and46native paired scale captures. No normal grid selection or actual actor/task/Continue admission."},"  "))
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  var file:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES TURN V3 NATIVE: ",checks,"checks; ",failures,"failures; ",captures,"captures")
 quit(1 if failures else 0)
