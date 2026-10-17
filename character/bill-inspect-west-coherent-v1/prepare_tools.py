from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
E=P.parent/'bill-inspect-east-coherent-v1'
sources=P/'sources';sources.mkdir(exist_ok=True)
prompt=(E/'sources/prompt-inspect.txt').read_text().replace('RIGHT/east','LEFT/west').replace('EAST','WEST').replace('east recovery','west recovery').replace('east idle','west idle')
prompt+=' Keep torso upright and head crown nearly fixed during the downward glance: use eye/chin movement, no large neck bow or shortened body.\n'
destination=sources/'prompt-inspect.txt'
if not destination.exists():destination.write_text(prompt)
for name in ['build.py','verify.py','build_review.py']:
    text=(E/name).read_text().replace('east','west').replace('(x>np.median(x))','(x<np.median(x))').replace('(bx>np.median(bx))','(bx<np.median(bx))').replace('dx=19-head.width/2','dx=20-head.width/2')
    if name=='build.py':
        text=text.replace("source=P/'sources/inspect-v1.png'","source=P/cfg.get('source','sources/inspect-v1.png')")
        text=text.replace('# The generated last neutral pose has a shorter projected body. Close with\n    # the exact first pose instead of introducing per-pose scaling.','# Preserve exact neutral loop closure at one fixed source scale.')
    if name=='verify.py':
        text=text.replace("check(sha(P.parent/r['idleAuthority'])==r['idleSha256'],'Selected matte master binding')","check(sha(P.parent/r['idleAuthority'])==r['idleSha256'],'Selected matte master binding')\n    check(max(row['headAxis'][1] for row in r['frames'])-min(row['headAxis'][1] for row in r['frames'])<=3,'Corrected upright crown amplitude within3native pixels')")
    (P/name).write_text(text)
test=(ROOT/'tests/test_bill_inspect_east_candidates.gd').read_text().replace('east','west').replace('EAST','WEST')
(ROOT/'tests/test_bill_inspect_west_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_inspect_west_candidates.gd.uid').write_text('uid://d7b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_inspect_east_candidate_validation.py').read_text().replace('east','west').replace('EAST','WEST').replace('BILL SEATED','BILL INSPECT WEST')
(ROOT/'tools/run_bill_inspect_west_candidate_validation.py').write_text(runner)
print('Prepared independent west inspection prompt and tools')
