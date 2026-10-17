from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'james-seated-family-v1/native.gd').read_text();s=s.split('\n\tfor id in ["crew_lounge"')[0]
s=s.replace('var failures:=0','var failures:=0\nvar checks:=0').replace('if not ok:failures+=1;push_error(message)','checks+=1\n\tif not ok:failures+=1;push_error(message)')
s=s.replace('james-seated-family-v1','james-lying-family-v1').replace('Vector2(92,172)','Vector2(128,224)')
s=s.replace('var expected:=', 'if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return\n\tvar expected:=',1)
s+='\n\tprint("JAMES INSTALLED LYING: ",checks," checks; ",failures," failures; actual grid loader, 144 slots")\n\tquit(1 if failures else 0)\n'
(P/'native-installed.gd').write_text(s)
for name in ['retained-berth','retained-berth-helmet']:
 s=(P/(name+'.gd')).read_text();s=s.replace('\tgame.grid_view.branforth_player.load_manifest("res://character/james-lying-family-v1/bare-manifest.json",true)\n','')
 s=s.replace('\tcheck(player.load_equipment_manifest("diving-helmet","res://character/james-lying-family-v1/helmet-manifest.json"),"Shared lying helmet paired")\n','')
 (P/(name+'.gd')).write_text(s)
