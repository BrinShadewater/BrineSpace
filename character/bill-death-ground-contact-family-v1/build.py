from pathlib import Path
import json,copy,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];checks=[];bindings={}
for gear in ['bare','helmet']:
 root=json.loads((P.parent/'bill-death-ground-family-v1'/('manifest.json' if gear=='bare' else 'helmet-manifest.json')).read_text())
 root['name']='Bill contact-aware dry-collapse '+gear+' candidate family';root['deathContactMode']='terminal-projection-v1'
 for d in ['north','south']:
  folder=P.parent/f'bill-death-ground-{"helmet-" if gear=="helmet" else ""}{d}-lateral-v1'
  m=json.loads((folder/'manifest.json').read_text());s=copy.deepcopy(m['states'][0]);s['id']='death-ground-lateral-'+d;s['deathContactVariant']='lateral'
  s['frameFiles']=['res://'+(folder/f).relative_to(R).as_posix() for f in s['frameFiles']]
  assert m['pivot']==root['pivot'] and m['standingHeight']==root['standingHeight'] and s['frameDurationsMs']==[250,300,350,400,400,300]
  root['states'].append(s)
 for s in root['states']:
  assert not s['loop'] and s['terminalFrame']==5 and len(s['frameFiles'])==6
  for f in s['frameFiles']:
   assert f.startswith('res://') and (R/f[6:]).is_file();bindings[f]=hashlib.sha256((R/f[6:]).read_bytes()).hexdigest()
 (P/('manifest.json' if gear=='bare' else 'helmet-manifest.json')).write_text(json.dumps(root,indent=2)+'\n',encoding='utf-8')
(P/'verification.json').write_text(json.dumps({'passed':True,'states':12,'frameReferences':len(bindings),'sha256':bindings,'scope':'original four headings and axial lateral options, paired; explicit candidate selection only'},indent=2)+'\n',encoding='utf-8')
print('Built12 paired contact states/72 literal frame references; unchanged authored pixels')
