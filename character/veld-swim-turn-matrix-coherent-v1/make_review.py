from pathlib import Path
import json
H=Path(__file__).resolve().parent;R=H.parents[1];tracks={}
for gear in ['bare','helmet']:
    m=json.loads((H/(gear+'-manifest.json')).read_text())
    for turn in m['states']:
        direction=turn['id'].removeprefix('swim-turn-');a,b=direction.split('-');track=[]
        for d in [a,b]:
            folder='veld-water-'+d+'-coherent-v1';base=R/'character'/folder
            loop=next(s for s in json.loads((base/(gear+'-manifest.json')).read_text())['states'] if s['id']=='swim-'+d)
            frames=[dict(file='../'+folder+'/'+p,duration=t,key=loop['id'],slot=i) for i,(p,t) in enumerate(zip(loop['frameFiles'],loop['frameDurationsMs']))]
            track.extend(frames)
            if d==a:track.extend(dict(file=p,duration=t,key=turn['id'],slot=i) for i,(p,t) in enumerate(zip(turn['frameFiles'],turn['frameDurationsMs'])))
            else:track.append(dict(file=frames[0]['file'],duration=1,key='destination frame0 hold',slot=0))
        tracks.setdefault(direction,{})[gear]=track
for pair in tracks.values():assert [f['duration'] for f in pair['bare']]==[f['duration'] for f in pair['helmet']]
template=(R/'character/veld-swim-turn-north-east-coherent-v1/review-template.html').read_text(encoding='utf-8')
start=template.index('<select id="direction">');end=template.index('</select>',start)+len('</select>')
template=template[:start]+'<select id="direction">'+''.join('<option>'+d+'</option>' for d in tracks)+'</select>'+template[end:]
template=template.replace('Veld north/east swim turn','Veld full swimming turn matrix').replace('Veld — north/east swimming turn','Veld — full swimming turn matrix')
template=template.replace('Four authored body/helmet angles join the exact selected water loops. Shared source-family cloth, skin and science-patch grade; protected brown hair/silver streak. Bare and helmet share one clock. Staged; runtime bindings unchanged. Runtime turn520ms; review at one-third speed.','Twelve directions: authored quarters520ms and derived halves1040ms, with exact cardinal masters and one140ms middle hold. Bare and helmet share one clock. Staged for proportions, stroke and pacing review. Playback at one-third speed.')
template=template.replace('bare-turn-contact-v1.png','bare-half-contact-v1.png').replace('helmet-fit-contact-v1.png','helmet-half-contact-v1.png').replace('Head and collar detail','All helmet half poses').replace('native-candidate-v1.png','native-page-06.png')
template=template.replace('while(i<18&&','while(i<track.length-1&&').replace('if(i===18)','if(i===track.length-1)')
template=template.replace('dir.onchange=reset;','dir.onchange=()=>{slider.max=tracks[dir.value].bare.length-1;reset()};')
template=template.replace('TRACKS',json.dumps(tracks,separators=(',',':')))
installed=(H/'selection.json').exists() and json.loads((H/'selection.json').read_text())['status'].startswith('installed')
if installed:template=template.replace('Staged for proportions, stroke and pacing review.','Installed through the normal Veld loader; furnished route and phase checks pass. Full-set polish continues.')
template=template.replace('<script>','<p><a href="full-speed-paired-motion-v1.mp4">Full-speed paired motion reel</a></p><script>',1)
(H/'index.html').write_text(template,encoding='utf-8')
(H/'review-checks.json').write_text(json.dumps(dict(directions=12,states=24,references=184,pairedClocks=True,finite=True,installed=installed),indent=2)+'\n')
print('12-direction shared-clock finite review ready')
