"""Compare named normal motion fields independently of revised sprite art."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT/'output/marsh-animation-audit/south-run-actor-04-v2-2026-10-02';NEW=ROOT/'output/marsh-animation-audit/south-run-actor-05-2026-10-02'
def main():
    old=json.loads((OLD/'report.json').read_text());new=json.loads((NEW/'report.json').read_text());assert old['failures']==new['failures']==0
    assert len(old['samples'])==len(new['samples'])==95
    fields=['elapsed','slot','running','foot','playerPhase'];comparisons=0
    for a,b in zip(old['samples'],new['samples']):
        for key in fields:assert a[key]==b[key],(key,a,b);comparisons+=1
    sources=[]
    for a,b in zip(old['captures'],new['captures']):
        assert a['slot']==b['slot'] and a['foot']==b['foot'] and a['position']==b['position']
        same=np.array_equal(np.array(Image.open(OLD/a['sourceFile']).convert('RGBA')),np.array(Image.open(NEW/b['sourceFile']).convert('RGBA')))
        assert same==(b['slot'] in [-1,2,5,-2]),(b['slot'],same)
        sources.append({'slot':b['slot'],'sameCompleteSource':same,'expectedChange':'whole contact translation' if b['slot'] in [0,1,3] else 'complete new passing08' if b['slot']==4 else 'unchanged'})
    result={'namedMotionComparisons':comparisons,'samples':95,'fields':fields,'captureRootComparisons':8,'sourceChanges':sources,'interpretation':'Art-only change: all named controller/player motion fields and eight capture roots equal previous04-v2 interval. No whole-framebuffer or real-time contact equality inferred.'}
    (NEW/'compare-preceding.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'samples':95,'namedMotionComparisons':comparisons,'captureRoots':8,'expectedSourceChanges':4}))
if __name__=='__main__':main()
