from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
recovery=(P.parent/'bill-recover-air-east-coherent-v1/build.py').read_text()
imports=recovery[:recovery.index('P=Path')]
grade=recovery.split('def main():\n',1)[1].split(' by,bx=np.where',1)[0]
grade=grade.replace('SOURCE','source').replace('HEADS','heads').replace('[-6:]','[-count:]')
grade=grade.replace('43)','43*density)').replace('hy+40)','hy+40*density)').replace('hx+45)','hx+45*density)').replace('hy+23)','hy+23*density)').replace('hy+75)','hy+75*density)').replace('hx-90)','hx-90*density)').replace('hx-5)','hx-5*density)').replace('hy+65)','hy+65*density)').replace('hy+160)','hy+160*density)')
grade=grade.replace('ids=sorted(', 'ids=sorted(')
grade+=' return raw,labs,ids,grade,{"neutralInput":src.tolist(),"neutralOutput":dst.tolist(),"gains":gains}\n'
(P/'grade.py').write_text(imports+"IDLE=Path(__file__).resolve().parent.parent/'crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png'\ndef prepare(source,heads,count,density=1):\n"+grade)
test=(ROOT/'tests/test_bill_seated_south_candidates.gd').read_text().replace('south','east')
(ROOT/'tests/test_bill_seated_east_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_seated_east_candidates.gd.uid').write_text('uid://t6b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_seated_south_candidate_validation.py').read_text().replace('south','east')
(ROOT/'tools/run_bill_seated_east_candidate_validation.py').write_text(runner)
print('Prepared east material authority and isolated native fixture')
