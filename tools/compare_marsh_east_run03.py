"""Exact controller-field comparison scoped to prior staged02 interval."""
from pathlib import Path
import json,numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT/'output/marsh-animation-audit/east-run-actor-02-2026-10-02';NEW=ROOT/'output/marsh-animation-audit/east-run-actor-03-2026-10-02'
def main():
    old=json.loads((OLD/'report.json').read_text());new=json.loads((NEW/'report.json').read_text());assert old['failures']==new['failures']==0 and len(old['samples'])==len(new['samples'])==95
    fields=['elapsed','slot','running','foot','playerPhase'];count=0
    for a,b in zip(old['samples'],new['samples']):
        for key in fields:assert a[key]==b[key],key;count+=1
    records=[]
    for a,b in zip(old['captures'],new['captures']):
        assert a['slot']==b['slot'] and a['foot']==b['foot'] and a['position']==b['position'];same=np.array_equal(np.array(Image.open(OLD/a['sourceFile']).convert('RGBA')),np.array(Image.open(NEW/b['sourceFile']).convert('RGBA')));assert same==(b['slot'] not in [0,1,2]);records.append({'slot':b['slot'],'sameCompleteSource':same})
    result={'namedMotionComparisons':count,'samples':95,'fields':fields,'captureRootsEqual':8,'sourceChanges':records,'scope':'Named controller/player motion and roots exact vs02. Only first3 whole sources change. No framebuffer equality, real-time film or articulated contact claim.'};(NEW/'compare-preceding.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'namedComparisons':count,'captureRootsEqual':8,'expectedChangedWholeSources':3}))
if __name__=='__main__':main()
