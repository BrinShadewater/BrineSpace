"""Deterministic neutral-midtone correction; leave skin/blue and bright silver intact."""
import numpy as np
from PIL import Image
def match_graphite(image):
 a=np.asarray(image.convert('RGB')).astype(float)
 spread=np.ptp(a,axis=2);value=a.mean(axis=2)
 weight=np.clip((32-spread)/16,0,1)*np.clip((160-value)/45,0,1)*np.clip(value/25,0,1)
 target=a*np.array([78/95,77/94,77/93.5])
 return Image.fromarray(np.rint(a+(target-a)*weight[:,:,None]).clip(0,255).astype('uint8'))
if __name__=='__main__':
 from pathlib import Path
 p=Path(__file__).resolve().parent
 match_graphite(Image.open(p/'helmet-input.png')).save(p/'helmet-graphite-input.png')
