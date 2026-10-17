from pathlib import Path
root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1';out=bank/'release-build-review-v365';out.mkdir(exist_ok=True)
source=(bank/'validate_release_v351.py').read_text().replace('james-release-closeout-v351','james-release-closeout-v365').replace('release-build-review-v351','release-build-review-v365')
source=source.replace("assert json.loads((o/'build-validation.json').read_text())['checks'][-1]['exitCode']==0", "assert json.loads((o/'build-validation.json').read_text())['exitCode']==0")
source=source.replace("fixture=p/'release_smoke.gd'", "fixture=r/'character/james-west-carry-walk-keys-v1/release-build-review-v351/release_smoke.gd'")
(bank/'validate_release_v365.py').write_text(source,encoding='utf8')
fixture=(bank/'north-unload-reused-rise-v363/native_playtest.gd').read_text()
start=fixture.index('    # Fixture-only resequencing');end=fixture.index('    var cases:Array=[]',start)
fixture=fixture[:start]+'''    for equipment in ["","diving-helmet"]:
        var selected_bank:Dictionary=player.frames if equipment.is_empty() else player.equipment_frames[equipment]
        var clocks:Dictionary=player.timing if equipment.is_empty() else player.equipment_timing[equipment]
        check(selected_bank["unload-north"].size()==7,"Normal packaged seven-pose unload")
        check(clocks["unload-north"].durations==[80.0,100.0,100.0,90.0,40.0,40.0,70.0],"Normal packaged rise timing")

'''+fixture[end:]
fixture=fixture.replace('unload363','unload365').replace('JAMES CANDIDATE UNLOAD','JAMES PACKAGED SEVEN POSE UNLOAD')
fixture=fixture.replace('Actual V351 Windows release','Actual V365 Windows release').replace('No normal selection, helmet candidate, autonomous goal choice','No autonomous goal choice')
fixture=fixture.replace('Fixture-only both-gear North unload resequencing of exact selected packaged texture objects; original mid-rise reused before standing,520ms.','Normal packaged seven-pose North unload, both gears,520ms; no fixture resequencing or artwork substitution.')
(out/'cargo_playtest.gd').write_text(fixture,encoding='utf8')
runner=(bank/'run_unload_native_v363.py').read_text().replace('north-unload-reused-rise-v363','release-build-review-v365').replace('native_playtest.gd','cargo_playtest.gd').replace('james-release-closeout-v351','james-release-closeout-v365').replace('james-unload-playtest-v363','james-unload-playtest-v365').replace('unload363','unload365')
(bank/'run_unload_native_v365.py').write_text(runner,encoding='utf8')
print('Prepared exact-package asset/startup checks and ordinary seven-pose workshop fixture')
