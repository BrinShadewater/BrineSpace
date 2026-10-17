from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;E=P.parent/'bill-inspect-entry-east-v1'
for name in ['build.py','verify.py','build_review.py']:
    text=(E/name).read_text().replace('east','south')
    if name=='build.py':
        text=text.replace("B/'grade.py'","P.parent/'bill-seated-loops-south-v1/build.py'")
        text=text.replace("module.prepare(P/spec['source'],spec['heads'],spec['count'],spec['density'])","module.prepare(P/spec['source'],spec['heads'],spec['density'])")
        text=text.replace(" donors={'bare'"," for key,data in prepared.items():\n  count=cfg['sources'][key]['count']\n  if len(data[2])!=count:\n   raw,labs,ids,grade,curve=data;n=np.bincount(labs.ravel());n[0]=0;ids=sorted(np.argsort(n)[-count:],key=lambda k:(np.median(np.where(labs==k)[0])//512,np.where(labs==k)[1].min()));prepared[key]=(raw,labs,ids,grade,curve)\n donors={'bare'")
        text=text.replace('(hx-19,hy-4)','(hx-18,hy-8)').replace('hy+31','hy+35')
    if not (P/name).exists():(P/name).write_text(text)
test=(ROOT/'tests/test_bill_inspect_entry_east_candidates.gd').read_text().replace('east','south').replace('EAST','SOUTH')
(ROOT/'tests/test_bill_inspect_entry_south_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_inspect_entry_south_candidates.gd.uid').write_text('uid://j7b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_inspect_entry_east_candidate_validation.py').read_text().replace('east','south').replace('EAST','SOUTH')
(ROOT/'tools/run_bill_inspect_entry_south_candidate_validation.py').write_text(runner)
print('Prepared front grade/native helmet and finite reader transition fixture')
