from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];clips=json.loads((P/'selected-clips.json').read_bytes());images={}
for key,c in clips.items():
    parent=(R/c['manifest']).parent;images[key]=[Image.open(parent/rel).convert('RGBA') for rel in c['frames']]
def frame(key,t):
    durations=clips[key]['durations'];total=sum(durations)/1000
    t=t%total if clips[key]['loop'] else min(t,total-.000001)
    elapsed=0
    for index,duration in enumerate(durations):
        elapsed+=duration/1000
        if t<elapsed:return images[key][index],index
    return images[key][-1],len(durations)-1
frames=[];durations=[];signatures=[];last=None
for ms in range(0,12600,20):
    t=ms/1000
    action,elapsed=('lie-down',t) if t<.8 else (('sleep',t-.8) if t<11.2 else (('get-up',t-11.2) if t<12 else ('idle',0)))
    selected={};sig=[]
    for direction in ['north','east','south','west']:
        for mode in ['bare','helmet']:
            key=mode+'-'+('lie-down' if action=='idle' else action)+'-'+direction
            im,index=(images[key][0],0) if action=='idle' else frame(key,elapsed)
            selected[(mode,direction)]=im;sig.append((key,index))
    signature=(action,tuple(sig))
    if signature==last:durations[-1]+=20;continue
    last=signature;signatures.append({'atMs':ms,'action':action,'selected':sig})
    board=Image.new('RGB',(1024,1160),'#303b40');d=ImageDraw.Draw(board)
    for row,direction in enumerate(['north','east','south','west']):
        d.text((8,row*290+4),direction+' | '+action+' | constructed source-clock preview, no furniture translation',fill='white')
        for col,(mode,kind) in enumerate([('bare','master'),('bare','action'),('helmet','master'),('helmet','action')]):
            im=images[mode+'-lie-down-'+direction][0] if kind=='master' else selected[(mode,direction)]
            board.paste(im,(col*256,row*290+27),im);d.text((col*256+6,row*290+17),mode+' '+kind,fill='white')
    frames.append(board);durations.append(20)
frames[0].save(P/'selected-rest-master-comparison.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=False,disposal=2)
(P/'playback-evidence.json').write_text(json.dumps({'sourceOnly':True,'nominalStepMs':20,'durationMs':sum(durations),'distinctCombinedSamples':len(frames),'stageSeconds':[.8,10.4,.8,.6],'samples':signatures,'scope':'Constructed selected-source playback at fixed canonical pivot, showing exact entry masters and all four paired directional ordinary rest sources. Sleep uses 3600ms source loop for10.4s. Not actual native cadence or furniture/head translation.'},indent=2)+'\n')
print('Built paired all-cardinal12.6s source comparison;',len(frames),'distinct combined samples.')
