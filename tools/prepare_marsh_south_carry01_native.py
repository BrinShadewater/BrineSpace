"""Stage a real workshop-carry actor on the validated furnished South route."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/review_marsh_south_run05_actor.gd').read_text()
source=source[:source.index('\tvar old_stride:')]
source=source.replace('south-run-actor-05','south-carry-actor-01').replace('marsh-south-run-material-v1/candidate-05','marsh-south-carry-material-v1/candidate-01')
source+='''\tvar old_stride:float=player.strides["carry-south"]
\tplayer.load_manifest(MANIFEST,true)
\tcheck(player.strides["carry-south"]==old_stride,"staged carry retains selected distance cadence")
\tcheck(is_equal_approx(player.cycle_seconds("carry-south"),.72),"four180ms carry loop retained")
\tfor slot in range(4):
\t\tvar used:Rect2i=player.frames["carry-south"][slot].get_image().get_used_rect()
\t\tcheck(used.end.y==172,"whole carry bbox anchored172; not anatomical contact proof")
\tgame.visual_time_seconds=100.0;player.current_key=""
\tawait capture("selected idle before cargo",-1)
\tactor.state="walk";actor.goal="curiosity";actor.stage="workshop_carry"
\tactor.activity="carrying recovered parts";actor.path=PackedVector2Array([route_start+Vector2(0,168)])
\tgame.paused=false
\tvar seen:Dictionary={};var previous_slot:=-1;var wraps:=0;var restores:=0
\tfor step in range(95):
\t\tvar before:Vector2=actor.foot
\t\tactor.move(.02)
\t\tgame.visual_time_seconds=100.02+step*.02
\t\tvar texture:Texture2D=game.grid_view._get_marsh_frame(game)
\t\tvar slot:int=player.frames["carry-south"].find(texture)
\t\tcheck(actor.animation_state()=="carry" and not actor.run_motion_active(),"actual workshop cargo selects carry and excludes running")
\t\tcheck(actor.direction=="south" and actor.foot.x==route_start.x,"actual carry keeps South heading/root axis")
\t\tcheck(actor.foot.y>before.y and actor.foot.y<=route_start.y+168,"normal controller progresses within cargo route")
\t\tcheck(slot>=0 and slot<4,"normal grid uses complete staged carry source")
\t\tcheck(absf(actor.foot.distance_to(before)-46.0*.02)<.001,"normal cargo moves46world/sec within coordinate precision")
\t\tif previous_slot==3 and slot==0:wraps+=1
\t\tif slot!=previous_slot and previous_slot>=0:check(slot==(previous_slot+1)%4,"distance cargo gait advances in phase order including wrap")
\t\tif not seen.has(slot):
\t\t\tseen[slot]=true
\t\t\tawait capture("actual South cargo pose%d"%slot,slot)
\t\t\tvar saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
\t\t\tcheck(Normal.valid_marsh_snapshot(saved),"moving actual workshop cargo snapshot validates")
\t\t\tvar restored=Normal.new();game.marsh_npc=restored
\t\t\tawait restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true)
\t\t\tplayer.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
\t\t\tcheck(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"cargo actor/player restore preserves root and whole source")
\t\t\tgame.paused=true;restored.update(game,.5)
\t\t\tcheck(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"pause freezes moving cargo actor and source")
\t\t\tgame.paused=false;actor=restored;restores+=1
\t\tprevious_slot=slot
\t\tsamples.append({"elapsed":(step+1)*.02,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"playerPhase":player.phase,"animationState":actor.animation_state(),"running":actor.run_motion_active()})
\t\tgame.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
\tcheck(seen.size()==4 and restores==4 and wraps>=2,"all four cargo phases restored and cycle wraps twice")
\tgame.paused=true
\tvar held:Dictionary=actor.snapshot();var held_texture:Texture2D=game.grid_view._get_marsh_frame(game)
\tactor.update(game,.5)
\tcheck(actor.snapshot()==held and game.grid_view._get_marsh_frame(game).get_image().get_data()==held_texture.get_image().get_data(),"final stationary cargo pause holds root and source")
\tawait capture("paused cargo after moving samples",previous_slot)
\tvar file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
\tfile.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"actorRestores":restores,"wraps":wraps,"strideDistanceCells":old_stride,"scope":"Actual normal Marsh.move/workshop_carry guard/rate, main/grid/player with staged whole carry manifest on clear168world furnished route;95 controlled20ms samples,four actor/player restores+pause holds,final cargo pause. Dedicated fixture selects normal cargo stage. No full RunSave/Title Continue, pickup/unload/turn joins, natural traffic or continuous contact acceptance."},"\\t"));file.close()
\tprint("MARSH SOUTH CARRY ACTOR: %dchecks,%dviews,%dfailures"%[checks,captures.size(),failures])
\tquit(1 if failures else 0)
'''
p=ROOT/'tools/review_marsh_south_carry01_actor.gd';assert not p.exists();p.write_text(source);p.with_suffix('.gd.uid').write_text('uid://cz7shcarry1v93\n')
publisher=(ROOT/'tools/publish_marsh_west_run02_actor.py').read_text()
publisher=publisher.replace('marsh-west-run-material-v1','marsh-south-carry-material-v1').replace('west-run-actor-02','south-carry-actor-01').replace('candidate-02','candidate-01').replace("report['actorRestores']==6","report['actorRestores']==4").replace("assert [c['slot'] for c in captures]==[-1,0,1,2,3,4,5,-2]","assert [c['slot'] for c in captures[:5]]==[-1,0,1,2,3] and len(captures)==6 and captures[-1]['slot'] in range(4)").replace("[ROOT/'character/marsh-v2/frames/bare/idle-west/000.png']","selected['idle-south']").replace("selected['walk-west']","selected['walk-south']").replace('crops[2:7]','crops[2:5]').replace('duration=[100]*6','duration=[180]*4').replace("'captures':8,'exactSources':8,'actorPlayerRestores':6","'captures':6,'exactSources':6,'actorPlayerRestores':4").replace('Six exact captured crops,100ms illustrative holds','Four exact captured crops,180ms illustrative holds').replace('West','South').replace('run02','carry01').replace('neutral147occupied','unobstructed neutral147occupied')
publisher=publisher.replace('six actor/player restores','four actor/player restores').replace('normal walk slowing','final stationary cargo pause').replace('side-to-side compression','cargo/head/body compression').replace('complete alternating stride study','complete supported cargo stride study')
publisher=publisher.replace('run staged actor review','carry staged actor review').replace('South run:','South carry:').replace('six100ms timing','four180ms timing').replace('Six exact captured crops','Four exact captured crops')
publisher=publisher.replace('allEightViewsInspected','allSixViewsInspected')
(ROOT/'tools/publish_marsh_south_carry01_actor.py').write_text(publisher)
print('Prepared actual workshop cargo move/render/restore fixture and paired UID; no normal selection.')
