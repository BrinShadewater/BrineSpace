"""Verify repair against the frozen pre-edit runtime, including shared artwork."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from prepare_marsh_master_repair import visual
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-master-repair-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 old=json.loads((BASE/'baseline-contract.json').read_text())['states'];sel=json.loads((BASE/'selection.json').read_text())['states'];installation=json.loads((BASE/'installation.json').read_text());shared={};checks=0
 assert set(old)==set(sel) and len(old)==204 and sum(map(len,sel.values()))==1058
 for key,s in old.items():
  assert len(sel[key])==len(s['files'])
  for original,new,h in zip(s['files'],sel[key],s['hashes']):
   assert sha(ROOT/original)==h,(key,'baseline modified')
   a=np.array(Image.open(ROOT/original).convert('RGBA'));b=np.array(Image.open(ROOT/new).convert('RGBA'));assert a.shape==b.shape and np.array_equal(a[:,:,3],b[:,:,3]),(key,'geometry')
   if key.startswith('injury-'):
    white=(a[:,:,:3].min(2)>=210)&(np.ptp(a[:,:,:3].astype(int),axis=2)<30)&(a[:,:,3]>0);assert np.array_equal(a[white],b[white]),(key,'fluid')
   if key.split('-')[0] in ('interact','repair','inspect','salvage','kneel','stand'):assert np.array_equal(a[:58],b[:58]) and np.array_equal(a[145:],b[145:]),(key,'diagnostic identity')
   v=visual(Image.fromarray(a));nv=visual(Image.fromarray(b));assert shared.setdefault(v,nv)==nv,(key,'shared pose mismatch')
   if key.startswith(('idle-','walk-','crew-chat-','weld-','torch-')):assert np.array_equal(a,b),(key,'accepted anchor changed')
   if new in installation['frames']:
    record=installation['frames'][new];assert sha(ROOT/new)==record['sha256'];assert sha(ROOT/record['editedSheet'])==record['editedSheetSha256']
   checks+=1
 entries=json.loads((BASE/'original-state-entries.json').read_text())
 for path in json.loads((BASE/'manifest-list.json').read_text()):
  m=json.loads((ROOT/'character/marsh-v2'/path).read_text())
  for s in m['states']:
   assert {k:v for k,v in s.items() if k!='frameFiles'}=={k:v for k,v in entries[s['id']].items() if k!='frameFiles'}
   assert m['pivot']==old[s['id']]['pivot'] and m['standingHeight']==old[s['id']]['standingHeight']
 print(f'{checks} slots verified: original geometry, timing, anchors, diagnostic head/boots, white fluid, shared poses and source hashes')
 runtime=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
 if all(runtime[k]['files']==sel[k] for k in sel):
  for k in sel:
   for f,h in zip(runtime[k]['files'],runtime[k]['hashes']):assert sha(ROOT/f)==h
  print('Installed current runtime contract matches all 204 repaired selections')
 (BASE/'audit.json').write_text(json.dumps({'slots':checks,'states':204,'failures':0,'scope':'Geometry/metadata/identity anchors/shared-pose equality/white fluid/provenance; visual acceptance is separate.'},indent=2)+'\n')
if __name__=='__main__':main()
