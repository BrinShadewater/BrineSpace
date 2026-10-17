from pathlib import Path
root=Path(__file__).resolve().parent
out=root/'water-journey-review-v345'
out.mkdir(exist_ok=True)
source=(root/'water-native-review-v344/native_probe.gd').read_text()
start=source.index('\tvar old=game.grid_view')
end=source.index('\tvar npc=game.branforth_npc',start)
install=source[start:end].replace('\t','\t',1)
source=source[:start]+'\tinstall_player()\n\tvar player=game.grid_view.branforth_player\n'+source[end:]
source=source[:source.index('\tnpc.foot=foot')]+'''\tnpc.foot=foot
\tfor gear in ["","diving-helmet"]:
\t\tvar mode:String="bare" if gear.is_empty() else "helmet"
\t\tnpc=game.branforth_npc;npc.foot=foot;npc.helmet_equipped=not gear.is_empty();npc.movement_medium="flooded"
\t\tnpc.direction="west";npc.state="idle";npc.stage="";npc.goal="";npc.path.clear();npc.expedition.clear()
\t\tplayer=game.grid_view.branforth_player;game.visual_time_seconds=100.65;game.paused=true
\t\tplayer.restore_snapshot({"key":"swim-west","equipment":gear,"phase":0.0,"last_time":99.9,"started":99.0,"last_position":foot/384.0,"motion":{"state":"tread","direction":"west","clip":"swim-stop-phase-2-west","started":100.0}})
\t\tvar before:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\tnpc.direction="north";npc.state="walk"
\t\tvar entry:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\tcheck(same(before,entry),"Restart preserves moving route entry")
\t\tvar key:String=player.motion.clip
\t\tcheck(key.begins_with("swim-reorient-"),"Moving route starts authored bridge")
\t\tif not key.begins_with("swim-reorient-"):quit(2);return
\t\tvar destination:Vector2=foot+Vector2(0,-24)
\t\tvar extent:Array=player.clip_extent(key,gear)
\t\tcheck(npc.swim_segment_clear(foot,destination,"north","west",false,extent),"Complete prescribed segment fits full active bridge envelope")
\t\tif failures:quit(2);return
\t\tnpc.path=PackedVector2Array([destination]);npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
\t\tawait capture(mode+"-entry",npc)
\t\tvar resumed:=false;var ticks:=0;var travelled:=0.0
\t\twhile ticks<160:
\t\t\tvar previous:Vector2=npc.foot
\t\t\tif not npc.path.is_empty():npc.move(.01)
\t\t\tgame.visual_time_seconds+=.01;ticks+=1
\t\t\ttravelled+=npc.foot.distance_to(previous)
\t\t\tvar tex:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\t\tif not resumed and ticks==15:
\t\t\t\tawait capture(mode+"-before-resume",npc)
\t\t\t\tvar actor_before:Dictionary=npc.snapshot();var playback_before:Dictionary=player.snapshot();var pixels:PackedByteArray=tex.get_image().get_data();var visual:float=game.visual_time_seconds
\t\t\t\tvar save=preload("res://scripts/run_save.gd");var path:String="user://water345-"+mode+".loop"
\t\t\t\tvar data:Dictionary=save.capture(game);var problem:String=save.problem(data)
\t\t\t\tcheck(problem.is_empty(),"Full swimming checkpoint admitted: "+problem)
\t\t\t\tif not problem.is_empty():quit(2);return
\t\t\t\tcheck(save.write(game,path)==OK,"Actual disk checkpoint write");data=save.read(path)
\t\t\t\troot.remove_child(game);game.queue_free();await process_frame
\t\t\t\tgame=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://water345.meta";game.run_save_path=path
\t\t\t\troot.add_child(game);current_scene=game
\t\t\t\twhile not game.startup_complete:await process_frame
\t\t\t\tgame.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
\t\t\t\tinstall_player()
\t\t\t\tcheck(await save.restore_staged(game,data),"Fresh scene restores disk checkpoint with staged bank installed first")
\t\t\t\tgame.run_save_path=path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
\t\t\t\tnpc=game.branforth_npc;player=game.grid_view.branforth_player
\t\t\t\tcheck(npc.snapshot()==actor_before,"Full swimming actor exact after disk restore")
\t\t\t\tcheck(player.snapshot()==playback_before,"Swimming playback exact after disk restore")
\t\t\t\tcheck(game.paused and game.visual_time_seconds==visual,"Pause/clock preserved")
\t\t\t\tcheck(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Exact swimming pixels after fresh scene restore")
\t\t\t\tgame._process(.5);check(npc.snapshot()==actor_before and game.visual_time_seconds==visual,"Paused restored swimmer does not advance")
\t\t\t\tawait capture(mode+"-after-resume",npc);resumed=true
\t\t\tif ticks==45:await capture(mode+"-moving",npc)
\t\tcheck(resumed,"Whole-run fresh scene checkpoint exercised")
\t\tcheck(travelled>23.9 and npc.foot.distance_to(destination)<.01,"Actual movement reaches prescribed flooded route endpoint")
\t\tcheck(not str(player.motion.get("clip","")).begins_with("swim-reorient-"),"Finite bridge releases after movement and disk resume")
\t\tawait capture(mode+"-complete",npc)
\tFileAccess.open(OUT+"journey-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"scope":"Two prescribed 24-unit actual move() flooded routes; full bridge segment clearance; two fresh main-scene whole-run disk restores with staged bank installed before restoration. Not autonomous update()/goal dispatch, normal selection, exterior, blocked fallback or title UI Continue."},"\\t"))
\tprint("JAMES WATER JOURNEY checks=",checks," failures=",failures," captures=",captures.size());game.queue_free();await process_frame;quit(0 if failures==0 else 1)
func install_player()->void:
'''+install
source=source.replace('water-native-review-v344','water-journey-review-v345').replace('water344','water345')
source=source.replace('npc.swim_segment_clear(at,at,"west","west",false,','npc.swim_segment_clear(at,at+Vector2(0,-24),"north","west",false,')
(out/'journey_probe.gd').write_text(source)
print('Prepared V345 moving route and fresh-scene disk restoration probe')
