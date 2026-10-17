from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];P=R/'character/krusher-cargo-family-v3'
text=(R/'character/krusher-head-fit-v2/validate_cargo.py').read_text().replace('krusher-cargo-family-v2','krusher-cargo-family-v3').replace('krusher-cargo-settle-profile-v2','krusher-cargo-settle-profile-v3')
extra='''
from scipy.ndimage import binary_dilation,label
contacts=[];contact_errors=[]
for q in read(P/'revision.json')['records']:
 detail=q['details'];tag=q['output']
 if 'restoredShellMask' in detail:
  restored=np.array(Image.open(P/detail['restoredShellMask']))>0;original=rgba(R/detail['restoredOriginalShell'][6:]);assert np.array_equal(rgba(P/tag)[restored,:3],original[restored,:3]);checks+=1
 if 'headSource' not in detail:continue
 assert sha(R/detail['headSource'][6:])==detail['headHash'];checks+=1
 if q['gear']!='bare':continue
 b=rgba(P/tag);head=rgba(R/detail['headSource'][6:]);x,y=detail['paste'];layer=np.zeros_like(b);layer[y:y+head.shape[0],x:x+head.shape[1]]=head;opaque=layer[:,:,3]>180
 assert np.array_equal(b[opaque],layer[opaque]);checks+=1
 body=(b[:,:,3]>180)&~opaque;lower=opaque.copy();lower[:y+head.shape[0]*2//3]=False;edge=int((binary_dilation(lower)&body).sum());labs,n=label(b[:,:,3]>180);largest=np.bincount(labs.ravel())[1:].argmax()+1;joined=bool(np.all(labs[opaque]==largest));checks+=2
 contacts.append({'output':tag,'state':q['state'],'frame':q['frame'],'view':q['view'],'edge':edge,'joined':joined})
 if edge==0 or not joined:contact_errors.append(contacts[-1])
for g in ['bare','helmet']:assert (P/(g+'-manifest.json')).read_bytes()==(old/(g+'-manifest.json')).read_bytes();checks+=1
'''
text=text.replace("result={'checks':checks",extra+"\nresult={'contacts':contacts,'contactErrors':contact_errors,'checks':checks")
text=text.replace("'errors':[],'slots':slots", "'errors':contact_errors,'slots':slots")
text=text.replace("if k not in ['joins','scope']","if k not in ['joins','scope','contacts','contactErrors']")
text+="\nprint(json.dumps({'bareContacts':len(contacts),'contactErrors':contact_errors}));assert not contact_errors\n"
(P/'validate.py').write_text(text)
