"""Preserve selected sleeping art; revise the shared visual breathing clock."""
from pathlib import Path
import json,copy,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
binding=P/'source-bindings.json'
if not binding.exists():
    inventory=json.loads((R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_text())
    frozen={group:{k:v for k,v in inventory[group].items() if k.startswith('sleep-')} for group in ['body','equipment']}
    assert all('james-sleep-cadence-v1' not in v['path'] for rows in frozen.values() for v in rows.values()), 'Freeze original source manifests, not this output override.'
    binding.write_text(json.dumps(frozen,indent=2)+'\n',encoding='utf-8')
coverage=json.loads(binding.read_text());records=[]
selection=json.loads((P/'selection.json').read_text()) if (P/'selection.json').exists() else {}
board=Image.new('RGB',(6*256,8*280),'#303b40');draw=ImageDraw.Draw(board);previews={};row=0
for mode,group in [('bare','body'),('helmet','equipment')]:
    pack=None
    for direction in ['north','south','east','west']:
        key='sleep-'+direction;source=R/coverage[group][key]['path'];original=json.loads(source.read_text());state=next(s for s in original['states'] if s['id']==key)
        if pack is None:
            pack={k:copy.deepcopy(v) for k,v in original.items() if k!='states'};pack.update(name='James shared restful breathing cadence '+mode,status=selection.get('status','staged_sleep_clock_review_pending'),states=[])
        assert original['pivot']==pack['pivot'] and original['frameWidth']==pack['frameWidth'] and original['frameHeight']==pack['frameHeight'] and original['standingHeight']==pack['standingHeight']
        new=copy.deepcopy(state);new['frameFiles']=[];ims=[]
        for i,f in enumerate(state['frameFiles']):
            path=R/f.removeprefix('res://') if f.startswith('res://') else (source.parent/f).resolve();im=Image.open(path).convert('RGBA');ims.append(im)
            new['frameFiles'].append('res://'+path.relative_to(R).as_posix());records.append({'mode':mode,'direction':direction,'index':i,'source':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
            board.paste(im,(i*256,row*280+24),im);draw.text((i*256+5,row*280+4),mode+' '+key+' '+str(i),fill='white')
        assert state['frameDurationsMs']==[160.0]*6
        new['frameDurationsMs']=[600]*6
        new['provenance']['sleepCadence']={'sourceManifest':source.relative_to(R).as_posix(),'originalMs':state['frameDurationsMs'],'newMs':new['frameDurationsMs'],'method':'Same six selected source poses, exact existing pixels/alpha/proportions/grade/contact/head anchors. One shared3600ms sleeping visual cycle in all four directions and gear modes; life fatigue/service timers unchanged.'}
        pack['states'].append(new);previews[(mode,direction)]=ims;row+=1
    (P/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
board.save(P/'all-source-poses.png')
for direction in ['north','south','east','west']:
    for label,ms in [('original',160),('revised',600)]:
        views=[]
        for i in range(6):
            v=Image.new('RGB',(920,340),'#303b40');d=ImageDraw.Draw(v);d.text((8,8),'James '+direction+' sleep / '+label+' '+str(ms*6)+'ms cycle / bare and shared helmet',fill='white')
            for j,mode in enumerate(['bare','helmet']):
                im=previews[(mode,direction)][i];v.paste(im,(j*230,65),im)
                for h,x in [(82,500),(54,725),(27,860)]:
                    sc=h/148;small=im.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR);v.paste(small,(x+j*(small.width+5),300-round(224*sc)),small)
            views.append(v)
        views[0].save(P/(direction+'-'+label+'.gif'),save_all=True,append_images=views[1:],duration=ms,loop=0)
(P/'source-evidence.json').write_text(json.dumps({'frames':len(records),'changedPixels':0,'originalCycleMs':960,'revisedCycleMs':3600,'simulationServiceTimersChanged':False,'sourceRecords':records,'productionInstalled':selection.get('runtimeInstalled',False)},indent=2)+'\n',encoding='utf-8')
label='Installed; native evidence and remaining scopes in selection.json.' if selection.get('runtimeInstalled',False) else 'Staged native checks pending.'
(P/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James rest breathing cadence study</h1><p>Exact selected sleeping source poses. Original960ms vs revised3600ms visual clock; fatigue/service timing unchanged. '+label+'</p><img src="north-original.gif"><img src="north-revised.gif"><img src="all-source-poses.png">',encoding='utf-8')
print('Eight sleeping states;48 exact source references;3600ms visual cycle, no art or simulation timer edits.')
