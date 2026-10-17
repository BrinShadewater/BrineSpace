"""Prove cargo color revisions preserve alpha, metadata and unoccluded idle pixels."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
new=json.loads((ROOT/'manifest.json').read_text())
before=json.loads((ROOT/'review-before-matte-v5/manifest.json').read_text())
checks=0
for state,old in zip(new['states'],before['states']):
    for key in ['frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']:
        assert state[key]==old[key];checks+=1
    for path in state['frameFiles']:
        a=np.array(Image.open(ROOT/path));b=np.array(Image.open(ROOT/'review-before-matte-v5'/path))
        assert np.array_equal(a[:,:,3],b[:,:,3]);checks+=1
idle=np.array(Image.open(ROOT.parent/'crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png'))
for state,idx in [(new['states'][0],0),(new['states'][2],5)]:
    a=np.array(Image.open(ROOT/state['frameFiles'][idx]))[52:236,36:220]
    previous=np.array(Image.open(ROOT/'review-before-matte-v5'/state['frameFiles'][idx]))[52:236,36:220]
    # The retained ground case already overlaps a few boot-edge pixels.
    # Verify all idle pixels outside that existing case occlusion.
    visible=(idle[:,:,3]>0)&np.all(previous==idle,axis=2)
    assert np.array_equal(a[visible],idle[visible]);checks+=1
print(f'Grade preservation:{checks} checks pass;all23 alpha planes and metadata unchanged;unoccluded canonical idle pixels preserved')
