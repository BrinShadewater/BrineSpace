from pathlib import Path
P=Path(__file__).resolve().parent
# Installed player pixel/clock fixture through actual game loader.
s=(P.parent/'james-water-north-polish-v1/native-installed.gd').read_text().replace('james-water-north-polish-v1','james-west-water-death-polish-v1').replace('JAMES NORTH WATER POLISH INSTALLED','JAMES WEST WATER DEATH INSTALLED').replace('Vector2(128,128)','Vector2(128,224)').replace('36 slots','12 slots')
(P/'native-installed.gd').write_text(s)
base=(P.parent/'james-death-family-v1/native-installed-behaviour.gd').read_text().replace('const OUT := "res://character/james-death-family-v1/"','const OUT := "res://character/james-west-water-death-polish-v1/"')
base=base.replace('for d in ["east","south","west","north"]:', 'for d in ["west"]:').replace('for medium in ["dry","flooded"]:', 'for medium in ["flooded"]:')
base=base.replace('16 clear room-node cases,96 actual installed normal grid captures','2 West flooded clear room-node cases,12 actual normal grid captures')
for staged in [True,False]:
    s=base;name='native-staged-behaviour' if staged else 'native-installed-behaviour'
    if staged:s=s.replace('var player=game.grid_view.branforth_player','var player=game.grid_view.branforth_player\n\tplayer.load_manifest(OUT+"bare-manifest.json",true)\n\tcheck(player.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json"),"Staged West death helmets")')
    s=s.replace('installed-behaviour',name).replace('JAMES DEATH INSTALLED BEHAVIOUR:', 'JAMES WEST WATER DEATH '+('STAGED' if staged else 'INSTALLED')+' BEHAVIOUR:')
    s=s.replace('OUT+"clearance.json"','"res://character/james-death-family-v1/clearance.json"')
    (P/(name+'.gd')).write_text(s)
print('Prepared actual2-mode West flooded mortality fixture plus installed12-slot proof')
