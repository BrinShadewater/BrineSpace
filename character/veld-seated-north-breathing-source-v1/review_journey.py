"""Chronological source and real room captures of the naturally chosen seat."""
from pathlib import Path
import json,re,math,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-journey-v1'
v=json.loads((O/'validation.json').read_text());assert v['passed']
data=json.loads((O/'captures.json').read_text());reports=[];evidence=[]
def xy(text):return [float(s) for s in re.findall(r'-?\d+(?:\.\d+)?',text)]
for gear in ('bare','helmet'):
 records=[r for r in data['records'] if r['gear']==gear]
 board=Image.new('RGB',(1536,math.ceil(len(records)/6)*284),'#202a30');d=ImageDraw.Draw(board)
 room=Image.new('RGB',(1536,math.ceil(len(records)/6)*340),'#202a30');rd=ImageDraw.Draw(room)
 shown=[]
 for i,r in enumerate(records):
  x=(i%6)*256;y=(i//6)*284;im=Image.open(O/r['source']).convert('RGBA')
  assert im.size in [(184,184),(256,256)],('unknown source registration',im.size)
  # Selected standing/walk source pivot92/172; seated pivot128/224. Rebase
  # pixels onto a common canvas without resizing the figure or grading it.
  registered=Image.new('RGBA',(256,256));registered.alpha_composite(im,(36,52) if im.size==(184,184) else (0,0))
  board.paste(registered,(x,y+24),registered);d.text((x+4,y+4),f"{r['tick']/60:.2f}s {r['state']} {r['stage']}",fill='white')
  # Native room center and actual physical foot determine the room-local crop.
  # Existing seated offset is recorded rather than assuming furniture geometry.
  native=Image.open(O/r['screenshot']).convert('RGB')
  center=xy(r['roomCenter']);local=xy(r['localContact']);foot=xy(r['foot'])
  # Godot's global Control coordinates use the1920 design width; native
  # screenshot is1280px. At this fixture's zoom2 the room spans384 native px.
  ratio=native.width/1920
  cx=center[0]*ratio+(math.floor(foot[0]/384)-20)*384+local[0]
  cy=center[1]*ratio+(math.floor(foot[1]/384)-21)*384+local[1]-14.592
  crop=native.crop((round(cx-64),round(cy-115),round(cx+64),round(cy+55))).resize((256,340),Image.Resampling.NEAREST)
  room.paste(crop,(x,(i//6)*340));rd.text((x+4,(i//6)*340+4),f"{r['tick']/60:.2f}s {r['stage'] or r['state']}",fill='white')
  shown.append(registered);evidence.extend([O/r['source'],O/r['screenshot']])
 for suffix,b in [('source',board),('room',room)]:
  out=P/f'journey-{gear}-{suffix}.png';b.save(out);evidence.append(out)
 # Source-change playback only: approach sampling is capped, so exclude it.
 seated=[(r,im) for r,im in zip(records,shown) if r['stage'] in ['life_sit','life_seated','life_rise']]
 play=[];durations=[]
 for j,(r,im) in enumerate(seated):
  bg=Image.new('RGB',(256,256),'#202a30');bg.paste(im,mask=im.getchannel('A'));play.append(bg)
  next_tick=seated[j+1][0]['tick'] if j+1<len(seated) else r['tick']+1
  durations.append(max(20,round((next_tick-r['tick'])/60*1000/10)*10))
 if play:play[0].save(P/f'journey-{gear}-source.gif',save_all=True,append_images=play[1:],duration=durations,loop=0)
 reports.append({'gear':gear,'sourceChanges':len(records),'seatedSourceChanges':len(seated),'roomCrop':'global room center scaled nativeWidth/1920 design width;384native cell at zoom2; actual actor cell/local contact, main presentation offset14.592; full native context retained','playback':'source-change intervals from actual60Hz controller; capped approach excluded; not continuous native video'})
evidence += [O/n for n in ['captures.json','validation.json','native.log','profile-before.json','profile-after.json']]
evidence += [R/'tests/test_veld_seated_journey.gd',R/'tests/test_veld_seated_journey.gd.uid',R/'tools/run_veld_seated_journey.py']
bound={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in evidence}
(P/'journey-review.json').write_text(json.dumps({'reports':reports,'journeys':data['journeys'],'scope':data['scope'],'files':bound,'normalSelection':False},indent=2)+'\n')
print(json.dumps({'captures':len(data['records']),'reports':reports,'boundFiles':len(bound)}))
