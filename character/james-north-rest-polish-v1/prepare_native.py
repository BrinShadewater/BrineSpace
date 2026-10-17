from pathlib import Path
import sys,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];old=R/'character/james-lying-family-v1'
installed='--installed' in sys.argv
label='installed' if installed else 'staged'
source=(old/'native-installed.gd').read_text().replace('james-lying-family-v1','james-north-rest-polish-v1')
inject='\n\tplayer.load_manifest("res://character/james-north-rest-polish-v1/bare-manifest.json",true)\n\tcheck(player.load_equipment_manifest("diving-helmet","res://character/james-north-rest-polish-v1/helmet-manifest.json"),"North rest candidate equipment matches")'
if not installed:source=source.replace('var player=game.grid_view.branforth_player','var player=game.grid_view.branforth_player'+inject)
source=source.replace('JAMES INSTALLED LYING:','JAMES NORTH REST '+label.upper()+':').replace('144 slots','36 slots')
(P/('native-'+label+'.gd')).write_text(source)
for mode in ['bare','helmet']:
    source=(old/('retained-berth'+('-helmet' if mode=='helmet' else '')+'.gd')).read_text().replace('james-lying-family-v1','james-north-rest-polish-v1')
    if not installed:source=source.replace('var player=game.grid_view.veld_player if actor=="veld" else game.grid_view.branforth_player','var player=game.grid_view.veld_player if actor=="veld" else game.grid_view.branforth_player'+inject)
    source=source.replace('JAMES RETAINED BERTH:','JAMES NORTH REST '+label.upper()+' BERTH:')
    (P/('native-'+label+'-berth-'+mode+'.gd')).write_text(source)
if (old/'no-layout-overrides.json').exists():shutil.copy2(old/'no-layout-overrides.json',P/'no-layout-overrides.json')
print('Prepared',label,'player and paired actual retained-berth fixtures')
