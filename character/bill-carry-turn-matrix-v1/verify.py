"""Validate matrix sources and exact midpoint joins; does not prove visual identity."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
def main():
 checks=0;packs={kind:json.loads((HERE/f'{kind}-manifest.json').read_text()) for kind in ['bare','helmet']};provenance=json.loads((HERE/'half-turn-provenance.json').read_text());hashes=json.loads((HERE/'frame-hashes.json').read_text())
 for kind,pack in packs.items():
  assert len(pack['states'])==12 and len(set(s['id'] for s in pack['states']))==12;checks+=1
  for state in pack['states']:
   is_half=kind+'/'+state['id'] in provenance
   assert len(state['frameFiles'])==(11 if is_half else 6) and len(state['facings'])==len(state['frameFiles']) and len(state['frameDurationsMs'])==len(state['frameFiles']);checks+=1
   assert not state['loop'] and not state['water'] and sum(state['frameDurationsMs'])==(1600 if is_half else 800);checks+=1
   for file in state['frameFiles']:
    im=Image.open(HERE/file);assert im.mode=='RGBA' and im.size==(256,256) and im.getchannel('A').getbbox()[3]<=225;checks+=1
   if is_half:
    for record in provenance[kind+'/'+state['id']]['frames']:
     dest=HERE/record['file'];assert dest.read_bytes()==(HERE/record['source']).read_bytes() and hashlib.sha256(dest.read_bytes()).hexdigest()==hashes[record['file']];checks+=1
    midpoint=HERE/state['frameFiles'][5];assert midpoint.read_bytes()==(HERE.parent/provenance[kind+'/'+state['id']]['mergedSource']).read_bytes();checks+=1
 bare={s['id']:s for s in packs['bare']['states']};helmet={s['id']:s for s in packs['helmet']['states']}
 assert bare.keys()==helmet.keys();checks+=1
 for key in bare:
  assert bare[key]['frameDurationsMs']==helmet[key]['frameDurationsMs'];checks+=1
 report={'passed':True,'checks':checks,'scope':'matrix coverage,source availability,frame profiles,paired timing,derived half pixels/hashes,exact neutral midpoint','visualAcceptance':False,'installed':False,'nativePlayback':False}
 (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(f'{checks} matrix checks PASS;timing integration and visual consistency pending')
if __name__=='__main__':main()
