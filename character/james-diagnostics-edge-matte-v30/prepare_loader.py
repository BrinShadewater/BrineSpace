from pathlib import Path
import json, hashlib

p = Path(__file__).resolve().parent
r = p.parents[1]
old = r / 'character/james-east-inspect-body-grade-v26'
src = (old / 'validate.gd').read_text(encoding='utf-8')
src = src.replace('james-east-inspect-body-grade-v26', p.name)
src = src.replace('/bare-manifest.json"', '/staged-bare-manifest.json"').replace('/helmet-manifest.json"', '/staged-helmet-manifest.json"')
src = src.replace('JAMES EAST SEPARATE TABLET', 'JAMES DIAGNOSTICS EDGE')
for mode in ['bare','helmet']:
    pack = json.loads((p/(mode+'-manifest.json')).read_bytes())
    pack['states'] = [s for s in pack['states'] if s['id'].startswith(('inspect-','interact-')) and not s['id'].endswith('-east')]
    assert len(pack['states'])==6
    (p/('staged-'+mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n')
src = src.replace('var manifests := [BODY,HELMET]', '''# The normal catalog loads the East correction after the combined continuity bank.
    # Reproduce that order when appending this combined candidate.
    player.load_manifest("res://character/james-east-inspect-body-grade-v26/bare-manifest.json",true)
    check(player.load_equipment_manifest("diving-helmet","res://character/james-east-inspect-body-grade-v26/helmet-manifest.json"),"Preserved later East correction")
    var manifests := [BODY,HELMET]''')
src = src.replace('for state in pack.states:\n            var row', 'for state in pack.states:\n            if String(state.id).ends_with("-east"): continue\n            var row')
src = src.replace('manifests[mode].get_base_dir().path_join(state.frameFiles[i]).simplify_path()', 'String(state.frameFiles[i]) if String(state.frameFiles[i]).begins_with("res://") else manifests[mode].get_base_dir().path_join(state.frameFiles[i]).simplify_path()')
src = src.replace('    for equipment in ["", "diving-helmet"]:', '''    # Check every later East source, including deliberate sealed meal aliases.
    for mode in range(2):
        var east_path: String = "res://character/james-east-inspect-body-grade-v26/"+("bare-manifest.json" if mode==0 else "helmet-manifest.json")
        var east: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(east_path))
        var rows: Dictionary = player.frames if mode==0 else player.equipment_frames["diving-helmet"]
        for state in east.states:
            check(rows[state.id].size()==state.frameFiles.size(),"East preserved count "+state.id)
            for i in range(rows[state.id].size()):
                var path: String = state.frameFiles[i]
                if not path.begins_with("res://"): path=east_path.get_base_dir().path_join(path).simplify_path()
                check(rows[state.id][i].get_image().get_data()==Image.load_from_file(ProjectSettings.globalize_path(path)).get_data(),"East preserved source "+state.id+" "+str(i))
    for equipment in ["", "diving-helmet"]:''')
src = src.replace('if not String(state.id).begins_with("inspect-"): continue', 'if not String(state.id).begins_with("inspect-") or String(state.id).ends_with("-east"): continue')
src = src.replace('Staged paired candidate appended to actual normal-loaded player, all East references/clocks/pivots sampled and native four-size captures. Other cardinal seams and sealed-meal semantics retained. Not normally installed, room/route/Continue or uninterrupted motion acceptance.', 'Staged South/North/West paired candidate on actual normal-loaded player; every inspect/interact and retained non-East sealed-meal alias source/clock/pivot checked. Later East sources protected by original load order. Twelve paired four-size native captures. Not normal adoption, room/route/Continue or uninterrupted motion acceptance.')
(p / 'validate.gd').write_text(src, encoding='utf-8')
boards = sorted(p.glob('*-cycle-*.png'))
assert len(boards)==18
review = dict(reviewedBoards=[dict(path=f.relative_to(r).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in boards],reviewedSourceFrames=864,sourceBoardsReviewComplete=True,continuousMotionReviewComplete=False,normalChanged=False,fullGoalComplete=False,findings=[
    'All eighteen chronological source boards viewed individually: South141, North137, West154, bare and helmet. No newly visible color flash, clipping, equipment loss or silhouette break from edge material correction.',
    'Matte interior suit shading and tablet/equipment details retained. South tablet back faces viewer; North screen glimpse and West near-vertical tablet face James. South wrench stays on belt; West far wrench remains naturally occluded.',
    'Head/helmet gaze movement remains inherited source movement. The edge-only correction does not certify or replace uninterrupted motion review.',
    'All864 source alpha/R/B and pixels outside the numeric green-edge selector exact; twelve standing endpoint sources exact. Selection and actual room/Continue verification remain pending.'
])
(p/'review-acceptance.json').write_text(json.dumps(review,indent=2)+'\n')
print(json.dumps(dict(reviewedBoards=18,reviewedSourceFrames=864,fixture='validate.gd',normalChanged=False)))
