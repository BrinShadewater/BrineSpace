"""Rebuild one heading without touching other movement/work/status frames."""
import argparse,hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw
from build_motion_pack import ROOT,SOURCE,SIZE,FONT,views,cell,centered,transformed
from build_rotor_review import spin

parser=argparse.ArgumentParser();parser.add_argument('heading');args=parser.parse_args()
views.update(json.loads((ROOT/'additional-views.json').read_text(encoding='utf-8')))
spec=views[args.heading];metadata=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
base=centered(cell(spec['file'],spec.get('cell')),spec['anchor'],spec['scale'])
base.save(ROOT/'poses'/f'{args.heading}.png')
rigs=[transformed(r,spec['anchor'],spec['scale']) for r in spec['rotors']]
metadata['headings'][args.heading].update({'source':spec,'rotors':rigs})
for state,turns in [('idle',1),('move',6)]:
    entry=next(s for s in metadata['states'] if s['id']==f'{state}-{args.heading}')
    atlas=Image.new('RGBA',(8*SIZE,7*SIZE))
    for n,path in enumerate(entry['frameFiles']):
        frame=base.copy();combined=np.zeros((SIZE,SIZE),bool)
        for r in rigs:
            frame,mask=spin(frame,r,n/51,turns);combined|=mask>0
        assert not np.any(np.any(np.asarray(base)!=np.asarray(frame),axis=2)&~combined)
        frame.save(ROOT/path);atlas.paste(frame,((n%8)*SIZE,(n//8)*SIZE))
    atlas.save(ROOT/entry['atlas']['path'])
metadata['sourceFiles']=[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(SOURCE.glob('*.png'))]
(ROOT/'manifest.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
review=Image.new('RGB',(1024,600),'#17272e');d=ImageDraw.Draw(review)
for i,name in enumerate(['north','northeast','east','southeast','south','southwest','west','northwest']):
    item=metadata['headings'][name];im=Image.open(ROOT/item['pose']);x=(i%4)*256;y=(i//4)*300
    review.paste(im,(x,y+30),im);d.text((x+15,y+8),name.upper(),font=FONT,fill='#cadce5')
    for r in item['rotors']:
        cx,cy=r['center'];d.ellipse((x+cx-2,y+30+cy-2,x+cx+2,y+30+cy+2),fill='#ee6e58')
review.save(ROOT/'review/direction-registration.png')
print('Rebuilt',args.heading,': 102 frames and two atlases; other clips untouched')
