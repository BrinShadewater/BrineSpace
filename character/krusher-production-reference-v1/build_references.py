from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont

P=Path(__file__).resolve().parent; R=P.parent.parent
MOVE=P.parent/'krusher-moving-equipment-test-v2'; ACTION=P.parent/'krusher-terminal-gear-pair-v1'; HEAD=P.parent/'krusher-bill-base-test-v2'
P.mkdir(exist_ok=True); BG='#272b2e'; FG='#e7eef0'; CYAN='#527c80'
regular=R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'; bold=R/'assets/fonts/BarlowSemiCondensed-SemiBold.ttf'
font=lambda n,b=False:ImageFont.truetype(str(bold if b else regular),n)
hashes={};tiles=[];sheets=[]
def read(path):
    hashes[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    return Image.open(path).convert('RGBA')
def board(name,size,title,subtitle):
    im=Image.new('RGBA',size,BG);d=ImageDraw.Draw(im);d.text((30,18),title,font=font(38,True),fill=FG);d.text((30,66),subtitle,font=font(25),fill='#b8c9cd');sheets.append((name,im));return im,d
def tile(im,path,xy,scale=1):
    art=read(path);size=(round(art.width*scale),round(art.height*scale));art=art.resize(size,Image.Resampling.NEAREST if scale>=1 else Image.Resampling.LANCZOS)
    im.alpha_composite(art,xy);tiles.append({'sheet':sheets[-1][0],'source':path.relative_to(R).as_posix(),'xy':list(xy),'size':list(size),'filter':'nearest' if scale>=1 else 'lanczos'})
directions=['south','east','north','west']
im,d=board('character-sheet.png',(1600,1190),'KRUSHER DOM  /  SYSTEM ADMINISTRATOR','AI & Robotics  |  Bill body reuse candidate  |  matte muted cyan  #527C80')
for row,gear in enumerate(['bare','helmet']):
    for col,direction in enumerate(directions):
        x=col*400+16;y=105+row*440
        d.text((x+22,y),direction.upper()+' / '+gear.upper(),font=font(24,True),fill=FG)
        tile(im,MOVE/f'frames/{gear}/idle-{direction}/000.png',(x,y+30),2)
for col,direction in enumerate(directions):
    tile(im,MOVE/f'frames/bare/idle-{direction}/000.png',(col*400+145,1000),.5)
d.text((30,1100),'Source canvas 184 x 184  |  foot pivot (92,172)  |  standing ruler 148 px',font=font(25),fill=FG)
d.text((30,1135),'Large views: 2x nearest. Small views: 92 px display references. Preserve original body gait and timing.',font=font(23),fill='#b8c9cd')

registration=json.loads((HEAD/'verification.json').read_text())
im,d=board('head-registration-sheet.png',(1600,640),'KRUSHER DOM  /  HEAD AND COLOUR REFERENCE','Four independent direction sources  |  swept brown hair, short beard, blue-grey eyes')
head_specs={}
for col,direction in enumerate(directions):
    path=HEAD/f'sources/{direction}-head-native.png';art=read(path)
    tile(im,path,(col*400+90,130),8)
    rec=next(r for r in registration['records'] if r['variant']=='bare' and r['state']=='idle-'+direction and r['frame']==0)
    spec={'size':list(art.size),'idlePaste':rec['headPaste'],'idleAxis':rec['headAxis'],'idleBottom':rec['headBottom'],'source':path.relative_to(R).as_posix()};head_specs[direction]=spec
    x=col*400+30
    d.text((x,395),direction.upper()+f'  {art.width} x {art.height} px',font=font(26,True),fill=FG)
    d.text((x,435),f"Idle paste {tuple(rec['headPaste'])}",font=font(23),fill=FG)
    d.text((x,470),f"Axis {rec['headAxis']} / neck bottom {rec['headBottom']}",font=font(23),fill=FG)
d.rectangle((30,535,90,595),fill=CYAN);d.text((110,535),'Matte cyan target: #527C80 / RGB 82,124,128',font=font(26),fill=FG)
d.text((110,573),'Shade by source luminance. Idle anchors are references; moving heads retain their frame registration.',font=font(23),fill='#b8c9cd')

manifest=json.loads((ACTION/'bare-manifest.json').read_text())
im,d=board('terminal-key-pose-sheet.png',(1600,1040),'KRUSHER DOM  /  TERMINAL ACTION KEYS','West action candidate  |  reuse the same pose body beneath the compatible helmet')
for row,state in enumerate(manifest['states']):
    y=110+row*285;count=len(state['frameFiles']);width=1600//count
    d.text((30,y),state['id'].upper()+f"  /  {sum(state['frameDurationsMs'])} ms",font=font(27,True),fill=FG)
    for col,path in enumerate(state['frameFiles']):
        x=col*width+(width-184)//2;tile(im,ACTION/path,(x,y+35))
        d.text((x,y+222),f"{col+1:02}  /  {state['frameDurationsMs'][col]} ms",font=font(23),fill=FG)
d.text((30,970),'Raise -> type loop -> lower -> exact idle. West bare/helmet body compatibility proved below source row 62.',font=font(23),fill=FG)
d.text((30,1004),'Keys reuse authored poses; repeated typing frames and reversed retrieval pose are derived reuse, not new inbetweens.',font=font(21),fill='#b8c9cd')

equipment=P.parent/'krusher-equipment-study-v1'
fit=json.loads((equipment/'manifest.json').read_text())['fit']
im,d=board('equipment-reference-sheet.png',(1600,1060),'KRUSHER DOM  /  EQUIPMENT REFERENCE','Native accessory pixels enlarged 8x nearest  |  independent views, consistent source density')
for row,group in enumerate(['closed-terminal','open-terminal','data-cartridges']):
    y=110+row*270;d.text((30,y),group.upper().replace('-',' '),font=font(27,True),fill=FG)
    for col,direction in enumerate(directions):
        path=equipment/f'parts/native/{group}-{direction}.png';art=read(path);x=col*400+80
        tile(im,path,(x,y+45),8)
        d.text((col*400+30,y+210),f'{direction.upper()} / {art.width} x {art.height} px',font=font(23),fill=FG)
for col,entry in enumerate(fit):
    x=col*400+30;attachment_text=' / '.join(f"{name.split('-')[0]} {tuple(pos)}" for name,pos in entry['attachments'])
    d.text((x,940),attachment_text,font=font(21),fill=FG)
d.text((30,986),'Fit coordinates are idle reference anchors; walking applies the recorded integer torso offset and glove foreground mask.',font=font(22),fill='#b8c9cd')
d.text((30,1020),'Terminal is hidden on the far side in East; cartridges are hidden on the far side in West. Do not mirror opposite views.',font=font(22),fill='#b8c9cd')
for name,im in sheets:im.convert('RGB').save(P/name)
metadata={'identity':{'name':'Krusher Dom','title':'System Administrator','department':'AI & Robotics','markings':'Matte muted grey-cyan','accentTarget':'#527C80'},'scope':'Production reference sheets assembled from existing sprites; unselected candidate, not owner acceptance or station integration.','canvas':[184,184],'pivot':[92,172],'standingRuler':148,'baseFamily':'Bill','headRegistration':head_specs,'sourceHashes':hashes,'tiles':tiles,'sheets':[name for name,_ in sheets],'sources':{'locomotion':MOVE.relative_to(R).as_posix(),'terminal':ACTION.relative_to(R).as_posix(),'head':HEAD.relative_to(R).as_posix()},'remaining':['Continuous artistic motion signoff','Expression and turn inbetween sources if required by consumer','Compatibility tests for other base families before reuse']}
metadata['equipmentIdleFits']=[{'direction':entry['direction'],'attachments':entry['attachments']} for entry in fit]
(P/'reference-manifest.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps({'sheets':len(sheets),'tiles':len(tiles),'sources':len(hashes)}))
