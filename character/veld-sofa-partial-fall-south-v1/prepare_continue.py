from pathlib import Path
R=Path(__file__).resolve().parents[2]
P=Path(__file__).resolve().parent
source=(R/'tests/test_veld_sofa_partial_south_staged.gd').read_text(encoding='utf-8')
helpers=source[:source.index('func run():')]
helpers=helpers.replace('veld-sofa-partial-south-staged-v1','veld-sofa-partial-south-continue-v1')
# The source/native sequences have already been captured at every source boundary.
# This interval exercises ordinary world save/restore and every future actor tick;
# native before/after submission is still checked independently per case.
start=helpers.index('\t\tvar index:int=',helpers.index('func future_trace('))
end=helpers.index('\t\tprevious=sample.pixels;',start)
helpers=helpers[:start]+'''\t\tvar pose:int=preload("res://scripts/veld_death_motion.gd").sofa_pose(recipe.clip)
\t\tvar early:bool=pose<2
\t\tvar bounds:Array=[.18,.34,.52,.70,.92] if early else [.18,.36,.56,.78,1.02]
\t\tvar index:int=0
\t\tfor bound in bounds:
\t\t\tif elapsed>=float(bound):index+=1
\t\tvar expected:Texture2D=clips[recipe.entry_key][recipe.entry_index] if index==0 else clips[recipe.clip][index]
\t\tcheck(sample.pixels==pixels_hash(expected),"Independent partial source clock: "+name)
\t\tvar hold:float=.18 if early else .36
\t\tvar release:float=.16 if early else .42
\t\tvar amount:float=1 if elapsed<hold else clampf(1-(elapsed-hold)/release,0,1)
\t\tcheck(sample.offset.distance_to(Vector2(recipe.entry_position_offset)*amount)<.00001,"Independent fractional seat release")
\t\tvar at:Vector2=game.veld_npc.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+sample.offset
\t\tcheck(is_equal_approx(sample.depth,maxf(at.y,float(recipe.entry_sort_depth)) if elapsed<hold+release else at.y),"Independent partial seat/floor depth")
\t\tcheck(sample.foot==(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(recipe.sofa_motion.local_foot),"Navigation foot fixed")
'''+helpers[end:]
run=source[source.index('func run():'):]
cut=run.index('\t\t\t\tvar presentations:Array=')
run=run[:cut]
normal=(R/'tests/test_veld_sofa_selected_continue.gd').read_text(encoding='utf-8')
a=normal.index('\t\t\tvar save_elapsed:float=')
b=normal.index('\n\tcheck(records.size()==20',a)
tail=normal[a:b]
tail=tail.replace('expected_clip','clip').replace('"living":entry','"living":living_rendered')
tail=tail.replace('Fresh normal scene Continue','Fresh staged scene Continue')
tail=tail.replace('SOFA WORLD CONTINUE','SOFA PARTIAL CONTINUE')
tail='\n'.join('\t'+line if line else line for line in tail.splitlines())+'\n'
run+=tail+'''\tcheck(records.size()==24,"All6partial poses/both movements/both gears,24ordinary fresh disk restores")
\tvar f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\\t"));f.close()
\tprint("VELD SOFA PARTIAL CONTINUE: %d checks,%d failures;24 fresh disk restores"%[checks,failures]);quit(1 if failures else 0)
'''
run=run.replace('var records:Array=[];var deaths:=0;var restores:=0;var guards:=0','var records:Array=[]')
run=run.replace('veld-sofa-partial-south-staged-v1','veld-sofa-partial-south-continue-v1')
(R/'tests/test_veld_sofa_partial_south_continue.gd').write_text(helpers+run,encoding='utf-8')
(R/'tests/test_veld_sofa_partial_south_continue.gd.uid').write_text('uid://d0evssfprtc1\n',encoding='utf-8')
wrapper=(R/'tools/run_veld_sofa_partial_south_staged.py').read_text(encoding='utf-8')
wrapper=wrapper.replace('veld-sofa-partial-south-staged-v1','veld-sofa-partial-south-continue-v1').replace('test_veld_sofa_partial_south_staged.gd','test_veld_sofa_partial_south_continue.gd')
wrapper=wrapper.replace('helmet-rise-pose5-sample-15-room.png','helmet-rise-pose5-after-room.png').replace('0 failures;24 world deaths/96 actor-file restores','0 failures;24 fresh disk restores').replace('SOFA PARTIAL STAGED','SOFA PARTIAL CONTINUE')
(R/'tools/run_veld_sofa_partial_south_continue.py').write_text(wrapper,encoding='utf-8')
print('Prepared24 ordinary disk/fresh-main restores and7200 future actor ticks; paired candidate injection explicit')
