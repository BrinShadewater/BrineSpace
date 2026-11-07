"""Publish bounded staged-source evidence; never selects normal artwork."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-collapse-material-v1'
AUDIT=ROOT/'output/marsh-animation-audit/south-collapse-material-native-01-2026-10-02'

def main():
    report=json.loads((AUDIT/'report.json').read_text())
    assert report['checks']==217 and report['failures']==0 and len(report['captures'])==6
    assert (AUDIT/'native-exit.txt').read_text().strip()=='0'
    log=(AUDIT/'native.log').read_text();assert 'ERROR:' not in log and 'SCRIPT ERROR:' not in log
    stable={}
    for name in ['inputs','owner']:
        before=json.loads((AUDIT/f'{name}-before.json').read_text())
        after=json.loads((AUDIT/f'{name}-after.json').read_text())
        assert before==after,f'{name} drift'
        stable[name]=len(before)
    frames=[Image.open(BASE/f'candidate-01/{i:03d}.png').convert('RGBA') for i in range(6)]
    for i,capture in enumerate(report['captures']):
        assert capture['slot']==i
        captured=Image.open(AUDIT/capture['sourceFile']).convert('RGBA')
        assert captured.size==(184,184) and np.array_equal(np.array(captured),np.array(frames[i]))
        assert set(np.unique(np.array(frames[i])[:,:,3])).issubset({0,255})
    apng=Image.open(BASE/'candidate-01/source-motion.apng')
    assert apng.n_frames==6 and apng.info['loop']==1
    for i in range(6):
        apng.seek(i)
        assert apng.info['duration']==180
        assert np.array_equal(np.array(apng.convert('RGBA')),np.array(frames[i]))
    review=BASE/'native-review-v1';review.mkdir(exist_ok=True)
    for capture in report['captures']:
        for key in ['file','sourceFile']:shutil.copy2(AUDIT/capture[key],review/capture[key])
    evidence={'status':'unselected staged dry source; art assessment pending','normalAdmission':False,'nativeChecks':217,'failures':0,'exitCode':0,'engineErrors':0,'sourceNativePairs':6,'exactSourcePairs':6,'decodedApngFrames':6,'apngPlays':1,'stableBoundedInputs':stable['inputs'],'unchangedOwnerNonLogFiles':stable['owner'],'nativeVisualReview':False,'sourceSheetVisualReview':True,'scope':report['scope'],'limits':'Not live actor collapse contact, injury liquid/recovery, full save/Continue, whole-family master acceptance or browser motion review. Bounded fingerprint does not freeze every normal catalog-loaded artwork.'}
    assessment_path=review/'visual-assessment.json'
    if assessment_path.exists():
        assessment=json.loads(assessment_path.read_text())
        assert assessment['reviewedNativeSlots']==list(range(6)) and not assessment['normalAdmission']
        evidence['nativeVisualReview']=True
        evidence['visualAssessment']='visual-assessment.json'
    (review/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    images='\n'.join(f'<figure><img src="{c["file"]}" alt="collapse slot {c["slot"]}"><figcaption>slot{c["slot"]} at {c["elapsed"]:.2f}s / staged source-player capture</figcaption></figure>' for c in report['captures'])
    html='''<!doctype html><meta charset="utf-8"><title>Marsh South dry collapse source study</title><style>body{background:#182b30;color:#dae8e2;font:16px system-ui;max-width:1500px;margin:25px auto}img{max-width:100%;image-rendering:pixelated}figure{margin:28px 0}</style><h1>Marsh South dry collapse: unselected material source01</h1><p>Six whole poses at fixed148/65.28 declared standing density, p92/172; 180ms each, settled source held. Exact selected idle first pose. New warm ivory boots and suit are closer to selected idle; torso/head, prone foreshortening and moving joins remain provisional.</p><p>217 source-player checks; six exact source pairs; six decoded APNG holds, one play. 32 bounded inputs and2931 owner non-log files unchanged. No real actor contact, normal admission, injury/recovery or browser-motion acceptance.</p><p><a href="../candidate-01/comparison.png">Old/new full source sheet</a> · <a href="../candidate-01/source-motion.apng">Finite source APNG</a> · <a href="verification.json">Verification scope</a></p>'''+images
    (review/'index.html').write_text(html,encoding='utf-8')
    print(json.dumps(evidence))
if __name__=='__main__':main()
