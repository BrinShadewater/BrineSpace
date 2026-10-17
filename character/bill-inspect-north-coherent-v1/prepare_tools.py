from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
E=P.parent/'bill-inspect-east-coherent-v1'
for name in ['build.py','verify.py','build_review.py']:
    text=(E/name).read_text().replace('east','north')
    if name=='build.py':
        text=text.replace("B/'grade.py'","B/'build.py'").replace('dx=19-head.width/2;dy=4-head.height/2','dx=17-head.width/2;dy=6-head.height/2')
        text=text.replace("source=P/'sources/inspect-v1.png'","source=P/cfg.get('source','sources/inspect-v1.png')")
        text=text.replace('# The generated last neutral pose has a shorter projected body. Close with\n    # the exact first pose instead of introducing per-pose scaling.','# Preserve exact neutral loop closure at one fixed source scale.')
    if name=='verify.py':
        text=text.replace('y.max()==223',"y.max()==r['frames'][0]['targetFrontBoot'][1]")
    if name=='build_review.py':
        text=text.replace('Standing diagnostic-reader inspection, with a small button press and glance.','Rear standing inspection. The reader and working gloves are naturally occluded in front of the torso; bent elbows remain connected.').replace('native north helmet','native rear helmet')
    (P/name).write_text(text)
test=(ROOT/'tests/test_bill_inspect_east_candidates.gd').read_text().replace('east','north').replace('EAST','NORTH')
(ROOT/'tests/test_bill_inspect_north_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_inspect_north_candidates.gd.uid').write_text('uid://e7b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_inspect_east_candidate_validation.py').read_text().replace('east','north').replace('EAST','NORTH').replace('BILL SEATED','BILL INSPECT NORTH')
(ROOT/'tools/run_bill_inspect_north_candidate_validation.py').write_text(runner)
print('Prepared rear grade/native helmet and isolated inspection fixture')
