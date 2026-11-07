"""North timer playback plus actual carry-arrive transition without facing override."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_cargo_east_action01_actor.gd').read_text()
s=s.replace('cargo-east-action-01-2026-10-02','cargo-north-action-01-2026-10-02')
s=s.replace('east-unload-01-unselected/manifest.json','north-unload-01-unselected/manifest.json')
s=s.replace('actor.direction="east"','actor.direction="north"').replace('action+"-east"','action+"-north"')
old='\t\tif action=="pickup":\n\t\t\tactor.update(game,.02)'
new='''		var arrival_samples:=0
		if action=="unload":
			var destination:Vector2=start+Vector2.UP*32
			check(actor.segment_clear(start,destination),"actual short North carry route clear")
			actor.stage="workshop_carry";actor.state="walk";actor.timer=0
			actor.path=PackedVector2Array([destination])
			for step in range(120):
				if actor.stage=="workshop_unload":break
				actor.update(game,.02);arrival_samples+=1;game.visual_time_seconds+=.02
				game.grid_view._get_marsh_frame(game)
				game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			check(actor.stage=="workshop_unload" and actor.direction=="north" and actor.path.is_empty() and is_equal_approx(actor.timer,2.0),"actual normal carry arrival forces North unload at2seconds")
		if action=="pickup":
			actor.update(game,.02)'''
assert old in s;s=s.replace(old,new)
s=s.replace('"exitDirection":actor.direction','"exitDirection":actor.direction,"actualArrivalSamples":arrival_samples')
s=s.replace('else:check(actor.stage!="workshop_unload" and actor.action_elapsed()<0,"normal unload timer exits action")','else:\n\t\t\tprint("UNLOAD EXIT stage="+actor.stage+" state="+actor.state+" pose="+actor.animation_state()+" elapsed="+str(actor.action_elapsed())+" direction="+actor.direction)\n\t\t\tcheck(actor.stage!="workshop_unload" and actor.animation_state()!="unload","normal unload timer exits unload, allowing subsequent route action")')
s=s.replace('"exitState":actor.state','"exitState":actor.state,"exitPose":actor.animation_state(),"exitElapsed":actor.action_elapsed()')
s=s.replace('Normal Marsh.update/main/grid/player staged East workshop pickup entered from work timer; East unload seeded valid action.','Normal Marsh.update/main/grid/player staged North pickup entered from work timer; actual short North carry route reaches arrive() and forces North unload.')
s=s.replace('NOT actual workshop arrival (it forcesNorth),expedition/fullsave','Actual arrival covered,NOT complete pickup-to-carry-to-unload delivery,expedition/fullsave')
s=s.replace('MARSH EAST ACTION','MARSH NORTH ACTION')
(ROOT/'tools/review_marsh_cargo_north_action01_actor.gd').write_text(s)
(ROOT/'tools/review_marsh_cargo_north_action01_actor.gd.uid').write_text('uid://dn1cargoact1v06\n')
finger=(ROOT/'tools/fingerprint_marsh_cargo_east_action01.py').read_text().replace('cargo_east_action01','cargo_north_action01').replace('cargo_east_unload01','cargo_north_unload01').replace('east-unload-01-unselected','north-unload-01-unselected')
finger=finger.replace("'character/marsh-east-carry-material-v1/candidate-03'","'character/marsh-east-carry-material-v1/candidate-03','character/marsh-north-carry-material-v1/candidate-01'")
(ROOT/'tools/fingerprint_marsh_cargo_north_action01.py').write_text(finger)
pub=(ROOT/'tools/publish_marsh_cargo_east_action01.py').read_text().replace('East','North').replace('east','north')
pub=pub.replace('North unload seeded valid timed action, not actual workshop arrival which forces North.','Actual short carry route enters North unload; not complete pickup-to-delivery route.')
(ROOT/'tools/publish_marsh_cargo_north_action01.py').write_text(pub)
print('North actual-arrival/timer fixture + paired review helpers prepared')
