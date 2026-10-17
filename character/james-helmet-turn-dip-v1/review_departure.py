from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'cadence';data=json.loads((o/'evidence.json').read_bytes())
audit=json.loads((r/'character/james-selected-turn-master-audit-v1/review.json').read_bytes());results=[]
for case in data['cases']:
    if not case['key'].endswith('-west'):continue
    last=max((s for s in case['samples'] if s['elapsed']<case['duration'] and 'capture' in s),key=lambda s:s['elapsed'])
    first=min((s for s in case['samples'] if s['elapsed']>=case['duration'] and 'capture' in s),key=lambda s:s['elapsed'])
    board=Image.new('RGB',(1200,2*320+290),'#303b40');d=ImageDraw.Draw(board)
    for i,(label,s) in enumerate([('last planted turn',last),('first walking carry',first)]):
        im=Image.open(o/s['capture']).convert('RGB');board.paste(im,(0,i*320))
        for gear,x in enumerate([100,700]):
            box=(x-40,95,x+45,160)
            board.paste(im.crop(box).resize((340,260),Image.Resampling.NEAREST),(i*600+gear*260,660))
        d.text((i*600+4,642),label,fill='white')
    name=case['key']+'-departure-detail.png';board.save(o/name)
    aliases=[]
    for mode,gear in [('bare',0),('helmet',1)]:
        folder=r/'character/james-cargo-material-joined-v1';m=json.loads((folder/(mode+'-manifest.json')).read_bytes())
        paths=[folder/next(s for s in m['states'] if s['id']==key)['frameFiles'][0] for key in ['carry-west','unload-west']]
        rgba=[Image.open(path).convert('RGBA').tobytes() for path in paths]
        assert rgba[0]==rgba[1]
        assert hashlib.sha256(rgba[0]).hexdigest()==first['rgbaSha256'][gear]
        source=r/audit['states'][mode+'/'+case['key']]['frames'][-1]
        assert hashlib.sha256(Image.open(source).convert('RGBA').tobytes()).hexdigest()==last['rgbaSha256'][gear]
        aliases.append({'gear':mode,'carry0EqualsUnload0':True,'departureLoadedRGBAboundToSource':True,'turnEndpoint':source.relative_to(r).as_posix(),'carry0':paths[0].relative_to(r).as_posix(),'unload0':paths[1].relative_to(r).as_posix()})
    results.append({'key':case['key'],'lastElapsed':last['elapsed'],'firstElapsed':first['elapsed'],'board':name,'sourceAliases':aliases})
(o/'departure-review.json').write_text(json.dumps({'visualReviewPending':True,'cases':results,'scope':'Actual normal player prescribed-clock West departures with exact source-bound carry0/unload0 aliases. No actor scheduling/full world/cadence acceptance.'},indent=2)+'\n')
print(json.dumps(results))
