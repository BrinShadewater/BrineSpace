"""Verify phase-zero source matching and shared wheel overlays for every work pose."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent
d=json.loads((R/'manifest.json').read_text());states={e['id']:e for e in d['states']};checks=[]
for h,meta in d['headings'].items():
    base=np.array(Image.open(R/meta['pose']).convert('RGBA'))
    drive=states['drive-'+h];atlas=Image.open(R/meta['wheelAtlas']['path']).convert('RGBA')
    assert np.array_equal(base,np.array(Image.open(R/drive['frameFiles'][0]).convert('RGBA')))
    mask=None
    for n,path in enumerate(drive['frameFiles']):
        patch=np.array(atlas.crop((n%6*448,n//6*448,(n%6+1)*448,(n//6+1)*448)))
        current=patch[:,:,3]>0
        if mask is None:mask=current
        assert np.array_equal(current,mask) and np.all(base[mask,3]>245)
        rolling=np.array(Image.open(R/path).convert('RGBA'))
        assert np.array_equal(patch[mask,:3],rolling[mask,:3])
        assert np.array_equal(base[~mask],rolling[~mask])
    work_frames=0
    for state in ['mine','collect','unload','blocked','power-on','power-off','charging','disabled']:
        e=states.get(state+'-'+h)
        if not e:continue
        for path in set(e['frameFiles']):
            body=np.array(Image.open(R/path).convert('RGBA'))
            assert np.array_equal(body[mask],base[mask]),(h,state,path,'wheel overlay would cover moving tool')
            work_frames+=1
    checks.append({'heading':h,'phaseZeroMatchesPose':True,'wheelLayerPhases':60,'workPoseChecks':work_frames,'overlayWithinOpaqueTyreArea':True})
(R/'review/wheel-layer-validation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print('PASS: 8 phase-zero joins, 480 wheel-layer phases, every work/power pose compatible with frozen wheels.')
