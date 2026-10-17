from pathlib import Path
r=Path.cwd();base=r/'character/james-west-carry-walk-keys-v1';out=base/'water-install-review-v347'
source=(base/'water-journey-review-v345/journey_probe.gd').read_text()
source=source[:source.index('func install_player()->void:')]
source=source.replace('water-journey-review-v345','water-install-review-v347').replace('water345','water347')
source=source.replace('\tinstall_player()\n','').replace('\t\t\t\tinstall_player()\n','')
# The generic replacement above leaves leading indentation when nested; repair
# only the line adjacent to the actual restore call.
source=source.replace('\t\t\t\t\t\t\tcheck(await save.restore_staged','\t\t\t\tcheck(await save.restore_staged')
source=source.replace('journey-review.json','installed-native-review.json')
source=source.replace('staged bank installed first','normal runtime bank already loaded')
source=source.replace('with staged bank installed before restoration','using the normal runtime player and Grid, without fixture bank installation')
source=source.replace('Not autonomous update()/goal dispatch, normal selection, exterior, blocked fallback or title UI Continue.','Normal selected player/Grid and fresh scene bank loading exercised. Not autonomous update()/goal dispatch, exterior route, blocked fallback visual acceptance or title UI Continue.')
source=source.replace('var player=game.grid_view.branforth_player','var player=game.grid_view.branforth_player\n\tcheck(player.get_script().resource_path=="res://scripts/james_water_player.gd","Normal runtime water player selected")',1)
(out/'installed_native_probe.gd').write_text(source)
print('Prepared normal selected renderer/route/fresh-scene checkpoint review')
