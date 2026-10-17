from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
E=P.parent/'bill-reading-entry-east-v1'
sources=P/'sources';sources.mkdir(exist_ok=True)
prompt=(E/'sources/prompt-entry.txt').read_text().replace('RIGHT/east','LEFT/west').replace('EAST','WEST').replace('east reading','west reading')
destination=sources/'prompt-entry.txt'
if not destination.exists():destination.write_text(prompt)
for name in ['verify.py','build_review.py']:(P/name).write_text((E/name).read_text().replace('east','west'))
test=(ROOT/'tests/test_bill_reading_entry_east_candidates.gd').read_text().replace('east','west')
(ROOT/'tests/test_bill_reading_entry_west_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_reading_entry_west_candidates.gd.uid').write_text('uid://z6b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_reading_entry_east_candidate_validation.py').read_text().replace('east','west')
(ROOT/'tools/run_bill_reading_entry_west_candidate_validation.py').write_text(runner)
builder=(E/'build.py').read_text().replace('east','west').replace('(x>np.median(x))','(x<np.median(x))').replace('(bx>np.median(bx))','(bx<np.median(bx))').replace('(hx-19,hy-4)','(hx-20,hy-4)')
builder=builder.replace('heads=[(248,48),(762,47),(1293,48),(251,540),(763,540),(1291,540)]',"rulers=json.loads((P/'source-rulers.json').read_text());heads=rulers['heads']")
builder=builder.replace('module.prepare(source,heads,6,1.1);sx,sy=.235,.263',"module.prepare(source,heads,6,rulers['density']);sx,sy=rulers['fixedRuler']")
builder=builder.replace("'density':1.1","'density':rulers['density']").replace("'exec-70d56942-f3f2-4c43-8b18-243981209ed4'","rulers['generation']")
(P/'build.py').write_text(builder)
verify=(P/'verify.py').read_text().replace("r['fixedRuler']==[.235,.263]","r['fixedRuler']==json.loads((P/'source-rulers.json').read_text())['fixedRuler']")
(P/'verify.py').write_text(verify)
print('Prepared west tablet transition prompt/tools;source ruler requires inspection')
