"""Build normal-runtime fixture for four reverse quarters and three opposites."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_carry_turn_eastsouth01_actor.gd').read_text();s=s[:s.index('\tvar route_start:=')]
s=s.replace('carry-turn-east-south-01','carry-remaining-paths-01').replace('east-south-01-unselected/manifest.json','opposite-01-unselected/family-manifest.json')
s+='''\tvar player=game.grid_view.marsh_player
\tplayer.load_manifest("res://character/marsh-east-carry-material-v1/candidate-03/manifest.json",true)
\tplayer.load_manifest("res://character/marsh-west-carry-material-v1/candidate-03/manifest.json",true)
\tplayer.load_manifest("res://character/marsh-south-carry-material-v1/candidate-01/manifest.json",true)
\tplayer.load_manifest("res://character/marsh-north-carry-material-v1/candidate-01/manifest.json",true)
\tplayer.load_manifest(MANIFEST,true)
\tvar axes={"east":Vector2.RIGHT,"west":Vector2.LEFT,"north":Vector2.UP,"south":Vector2.DOWN}
\tvar cases:Array=[]
\tfor pair in [["south","east"],["south","west"],["north","east"],["north","west"],["west","east"],["north","south"],["south","north"]]:
\t\tvar origin:String=pair[0];var dest:String=pair[1];var key:String="carry-turn-"+origin+"-"+dest
\t\tvar phases:int=player.frames[key].size();check(phases in [5,9],"quarter5 or opposite9 frames loaded")
\t\tvar origin_axis:Vector2=axes[origin];var dest_axis:Vector2=axes[dest]
\t\tactor=Normal.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
\t\tvar route_start:=Vector2.INF;var route_probes:Array=[]
\t\tfor dy in range(-130,131,20):
\t\t\tfor dx in range(-120,121,20):
\t\t\t\tvar candidate:Vector2=desired+Vector2(dx,dy);var corner:Vector2=candidate+origin_axis*64
\t\t\t\tvar clear:bool=actor.segment_clear(candidate,corner) and actor.segment_clear(corner,corner+dest_axis*96)
\t\t\t\tvar blocked:=0
\t\t\t\tfor leg in range(2):
\t\t\t\t\tfor travel in range(0,65 if leg==0 else 97,4):
\t\t\t\t\t\tvar point:Vector2=candidate+origin_axis*travel if leg==0 else corner+dest_axis*travel
\t\t\t\t\t\tfor offset in [Vector2.ZERO,Vector2(-25,-45),Vector2(25,-45)]:
\t\t\t\t\t\t\tif not actor.can_stand(point+offset):clear=false;blocked+=1
\t\t\t\t\troute_probes.append({"candidate":[candidate.x,candidate.y],"blockedSamples":blocked,"clear":clear})
\t\t\t\tif clear:route_start=candidate;break
\t\t\tif route_start.is_finite():break
\t\tcheck(route_start.is_finite(),key+" actual clear route with body envelope")
\t\tif not route_start.is_finite():quit(1);return
\t\tactor.foot=route_start;actor.state="idle";actor.direction=origin;actor.goal="";actor.stage="";actor.path=PackedVector2Array()
\t\tcheck(is_equal_approx(player.cycle_seconds(key),.4 if phases==5 else .8),"exact quarter/opposite timing")
\t\tcheck(player.frames[key][0].get_image().get_data()==player.frames["carry-"+origin][0].get_image().get_data(),"exact loaded origin endpoint")
\t\tcheck(player.frames[key][phases-1].get_image().get_data()==player.frames["carry-"+dest][0].get_image().get_data(),"exact loaded destination endpoint")
\t\tfor slot in range(phases):check(player.frames[key][slot].get_image().get_data()==player.frames["carry-turn-"+dest+"-"+origin][phases-1-slot].get_image().get_data(),"reverse whole frame sequence exact")
\t\tgame.visual_time_seconds=100.0;player.current_key="";player.motion={};game.paused=true
\t\tvar first_capture:int=captures.size();var first_sample:int=samples.size()
\t\tawait capture(key+" selected origin idle",-1);captures.back()["expectedKey"]="idle-"+origin
\t\tactor.state="walk";actor.goal="curiosity";actor.stage="workshop_carry";actor.activity="carrying recovered parts"
\t\tactor.path=PackedVector2Array([route_start+origin_axis*64,route_start+origin_axis*64+dest_axis*96]);game.paused=false
\t\tvar turn_seen:Dictionary={};var dest_seen:Dictionary={};var origin_seen:=false;var returned:=false;var restores:=0;var last_key:="";var last_slot:=-1
\t\tvar steps:int=140 if phases==5 else 160
\t\tfor step in range(steps):
\t\t\tvar before:Vector2=actor.foot;actor.move(.02);game.visual_time_seconds=100.02+step*.02
\t\t\tvar texture:Texture2D=game.grid_view._get_marsh_frame(game);var actual_key:String=player.motion.get("clip","")
\t\t\tif actual_key.is_empty():actual_key="carry-"+actor.direction
\t\t\tvar slot:int=player.frames[actual_key].find(texture)
\t\t\tcheck(actor.animation_state()=="carry" and not actor.run_motion_active(),"actual cargo excludes running")
\t\t\tcheck(actor.direction in [origin,dest] and actor.foot.distance_to(before)>0 and actor.foot.distance_to(before)<=46.0*.02+.001,"actual route advances within normal46rate")
\t\t\tcheck(slot>=0,"normal renderer selects exact staged source")
\t\t\tif actor.direction==origin and not origin_seen:
\t\t\t\torigin_seen=true;check(actual_key=="carry-"+origin and slot==0,"origin cargo begins at0")
\t\t\t\tawait capture(key+" origin cargo",slot);captures.back()["expectedKey"]=actual_key
\t\t\tif actual_key==key and not turn_seen.has(slot):
\t\t\t\tcheck(slot==turn_seen.size(),"all turn phases advance in order")
\t\t\t\tturn_seen[slot]=true;await capture(key+" turn%d"%slot,slot);captures.back()["expectedKey"]=actual_key
\t\t\t\tvar saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
\t\t\t\tcheck(Normal.valid_marsh_snapshot(saved),"movingturn actor snapshot valid")
\t\t\t\tvar restored=Normal.new();game.marsh_npc=restored;await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true);player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
\t\t\t\tcheck(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"restore exact root/source")
\t\t\t\tgame.paused=true;restored.update(game,.5)
\t\t\t\tcheck(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"pause restored root/source")
\t\t\t\tgame.paused=false;actor=restored;restores+=1
\t\t\tif actual_key=="carry-"+dest and not dest_seen.has(slot):
\t\t\t\tif not returned:returned=true;check(turn_seen.size()==phases and slot==0,"exact destination0return after all turn phases")
\t\t\t\tdest_seen[slot]=true;await capture(key+" destination%d"%slot,slot);captures.back()["expectedKey"]=actual_key
\t\t\tlast_key=actual_key;last_slot=slot;samples.append({"case":key,"elapsed":(step+1)*.02,"key":actual_key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"playerPhase":player.phase,"animationState":actor.animation_state(),"running":actor.run_motion_active()})
\t\t\tgame.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
\t\tcheck(origin_seen and returned and turn_seen.size()==phases and dest_seen.size()==4 and restores==phases,"all real turn/destination phases and restores covered")
\t\tgame.paused=true;var held:Dictionary=actor.snapshot();var held_texture:Texture2D=game.grid_view._get_marsh_frame(game);actor.update(game,.5)
\t\tcheck(actor.snapshot()==held and game.grid_view._get_marsh_frame(game).get_image().get_data()==held_texture.get_image().get_data(),"final pause root/source")
\t\tawait capture(key+" finalpaused destination",last_slot);captures.back()["expectedKey"]=last_key
\t\tcases.append({"key":key,"origin":origin,"destination":dest,"phaseCount":phases,"samples":steps,"actorRestores":restores,"turnSlots":turn_seen.keys(),"destinationSlots":dest_seen.keys(),"captureStart":first_capture,"captureCount":captures.size()-first_capture,"sampleStart":first_sample,"routeProbes":route_probes})
\t\tprint("CASE DONE "+key+" phases="+str(phases)+" captures="+str(captures.size()-first_capture))
\tvar file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"samples":samples,"scope":"Seven actual normal Marsh.move workshop_carry paths:four reverse quarters400ms andthree opposites800ms,normalfactory/main/grid/player with stagedcardinals+family. Exact orderedturn phases,actor-player restores/pause,destination0return,all4destinationphases andfinalpause. Dedicatedfree furnished fixture,normalflagsfalse. NotfullRunSave/visibleTitleContinue/completepickup-unload/continuouscontact/fullsetacceptance."},"\\t"));file.close()
\tprint("MARSH REMAINING PATHS: %dchecks,%dviews,%dfailures"%[checks,captures.size(),failures]);quit(1 if failures else 0)
'''
p=ROOT/'tools/review_marsh_carry_remaining_paths01_actor.gd';assert not p.exists();p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://dj7rempath1v03\n')
print('Prepared7 actual remainingpaths fixture+UID;normalruntime unchanged.')
