from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_sofa_partial_south_continue.gd').read_text(encoding='utf-8')
helpers=s[:s.index('func run():')]
run=s[s.index('func run():'):s.index('\t\t\t\tvar save_elapsed:float=')]
run+='''\t\t\t\tvar motion_started:float=actor.water_death_motion.started
\t\t\t\tvar foot:Vector2=actor.foot
\t\t\t\tfor tick in 49:
\t\t\t\t\tif tick>0:actor.update(game,1.0/30)
\t\t\t\t\tgame.visual_time_seconds=motion_started+tick/30.0
\t\t\t\t\tvar texture:Texture2D=game.grid_view._get_veld_frame_source(game)
\t\t\t\t\tvar rendered=await capture_bunk(game,CELL,name+"-tick-%02d"%tick,texture)
\t\t\t\t\tcheck(actor.foot==foot and actor.valid_veld_snapshot(actor.snapshot()),"Physical foot/strict snapshot through every motion presentation")
\t\t\t\t\trecords.append({"name":name,"tick":tick,"elapsed":tick/30.0,"pixels":pixels_hash(texture),"rendered":rendered})
\t\t\t\tprint("SOFA PARTIAL MOTION ",name," records=",records.size()," failures=",failures)
\tcheck(records.size()==1176,"24paired partial movements at30fps")
\tvar f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\\t"));f.close()
\tprint("VELD SOFA PARTIAL MOTION: %d checks,%d failures;1176 native motion captures"%[checks,failures]);quit(1 if failures else 0)
'''
(R/'tests/test_veld_sofa_partial_south_motion.gd').write_text((helpers+run).replace('veld-sofa-partial-south-continue-v1','veld-sofa-partial-south-motion-v1'),encoding='utf-8')
(R/'tests/test_veld_sofa_partial_south_motion.gd.uid').write_text('uid://d0evssfprtm1\n',encoding='utf-8')
r=(R/'tools/run_veld_sofa_partial_south_continue.py').read_text(encoding='utf-8').replace('veld-sofa-partial-south-continue-v1','veld-sofa-partial-south-motion-v1').replace('test_veld_sofa_partial_south_continue.gd','test_veld_sofa_partial_south_motion.gd')
r=r.replace('helmet-rise-pose5-after-room.png','helmet-rise-pose5-tick-48-room.png').replace('0 failures;24 fresh disk restores','0 failures;1176 native motion captures').replace('SOFA PARTIAL CONTINUE','SOFA PARTIAL MOTION')
(R/'tools/run_veld_sofa_partial_south_motion.py').write_text(r,encoding='utf-8')
print('Prepared all24 native30fps sequences; no change to current running Continue inputs')
