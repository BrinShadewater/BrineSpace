from pathlib import Path
P=Path(__file__).resolve().parent
base=(P.parent/'james-water-family-v1/native-installed-routes.gd').read_text()
base=base.replace('const OUT := "res://character/james-water-family-v1/"','const OUT := "res://character/james-water-north-polish-v1/"')
base=base.replace('OUT+"clearance.json"','"res://character/james-water-family-v1/clearance.json"')
base=base.replace('for d in ["east","south","west","north"]:', 'for d in ["north"]:')
# The active life profile now includes later distress/death/cargo families.
# Check ordinary water keys actually exercised, rather than historical whole-profile equality.
base=base.replace('check(selected==expected_clearance[field],"Actual NPC lazy selected "+field+" clearance")',
'''for mode in ["bare","helmet"]:
			var key: String="transition-north" if field=="actions" else "north"
			check(selected[mode][key]==expected_clearance[field][mode][key],"Actual NPC selected ordinary North "+field+" clearance")''')
for staged in [True,False]:
    s=base
    if staged:
        s=s.replace('var player=game.grid_view.branforth_player','var player=game.grid_view.branforth_player\n\tplayer.load_manifest(OUT+"bare-manifest.json",true)\n\tcheck(player.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json"),"Staged North helmets")')
    name='native-staged-routes' if staged else 'native-installed-routes'
    s=s.replace('installed-route-captures',name+'-captures').replace('installed-route-evidence.json',name+'-evidence.json')
    s=s.replace('JAMES WATER INSTALLED ROUTES:', 'JAMES NORTH WATER '+('STAGED' if staged else 'INSTALLED')+' ROUTES:')
    s=s.replace('Installed candidates on real James furnished five-room navigation',('Staged overrides' if staged else 'Normal installed selection')+' on real James furnished five-room navigation')
    (P/(name+'.gd')).write_text(s)
print('Prepared two-mode actual North routes, selected ordinary clearance keys only')
