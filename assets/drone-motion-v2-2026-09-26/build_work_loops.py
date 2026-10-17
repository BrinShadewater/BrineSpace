"""Animate authored work contacts with local arm rigs and separate effect layers."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw,ImageChops,ImageFont
from build_rotor_review import spin

ROOT=Path(__file__).resolve().parent
SIZE=256;N=102;FPS=30
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)

def articulated(im,poly,pivot,angle=0,dy=0):
    mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
    part=im.copy();part.putalpha(ImageChops.multiply(im.getchannel('A'),mask))
    base=im.copy();base.putalpha(ImageChops.multiply(im.getchannel('A'),ImageChops.invert(mask)))
    part=part.rotate(angle,resample=Image.Resampling.BICUBIC,center=pivot)
    if dy:part=part.transform(part.size,Image.Transform.AFFINE,(1,0,0,0,1,-dy),Image.Resampling.BICUBIC)
    base.alpha_composite(part)
    return base

def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)

def work_frame(name,source,n):
    t=n/FPS;phase=n/N
    # Continuous local motion at an authored work contact, no whole-body shaking.
    envelope=smooth(phase/.16)*(1-smooth((phase-.80)/.20))
    im=source.copy();fx=Image.new('RGBA',im.size);d=ImageDraw.Draw(fx)
    hub_y=138 if name in ['mine','collect'] else 132
    for center,sign in [((44,hub_y),1),((215,hub_y),-1)]:
        im,_=spin(im,{'center':center,'u':(9,-sign),'v':(sign*3,15),'sign':sign},n/51,1)
    if name=='mine':
        angle=math.sin(t*math.tau*6)*1.8*envelope
        im=articulated(im,[(180,205),(223,205),(228,255),(190,255)],(197,207),angle)
        for j in range(12):
            p=(t*.9+j/12)%1
            x=207+math.sin(j*12.7)*p*15;y=239-p*18
            if envelope>.2:d.ellipse((x-1,y-1,x+1,y+1),fill=(136,130,104,round(130*(1-p)*envelope)))
    elif name=='collect':
        lift=-7*math.sin(math.pi*phase)**2
        im=articulated(im,[(36,182),(100,182),(108,252),(30,252)],(72,182),dy=lift)
    elif name=='weld':
        angle=math.sin(t*math.tau/3.4)*2.3*envelope
        im=articulated(im,[(158,173),(205,177),(185,227),(126,230)],(180,177),angle)
        a=-math.radians(angle);px,py=180,177;dx,dy=143-px,217-py
        x=px+dx*math.cos(a)-dy*math.sin(a);y=py+dx*math.sin(a)+dy*math.cos(a)
        if envelope>.03:
            pulse=(.6+.4*math.sin(t*83)**2)*envelope
            d.ellipse((x-5,y-5,x+5,y+5),fill=(55,157,236,round(85*pulse)))
            d.ellipse((x-2,y-2,x+2,y+2),fill=(216,243,255,round(250*pulse)))
            for j in range(5):
                p=(t*1.4+j/5)%1
                bx=x+math.sin(j*4.1)*p*10;by=y-p*18
                d.ellipse((bx-1,by-1,bx+1,by+1),outline=(162,210,225,round((1-p)*150*envelope)))
    else:
        angle=math.sin(t*math.tau*2)*1.2*envelope
        im=articulated(im,[(148,175),(210,178),(185,227),(113,227)],(181,177),angle)
        if envelope>.2 and math.sin(t*math.tau*2)>.5:
            d.ellipse((109,206,113,210),fill=(151,214,227,round(150*envelope)))
    return im,fx

def lamp_layer(t,color=(48,155,255),center=(128,128)):
    fx=Image.new('RGBA',(SIZE,SIZE))
    lamp=Image.open(ROOT/'sources/drone-status-light.png').convert('RGBA')
    lamp=lamp.crop(lamp.getchannel('A').point(lambda a:255 if a>64 else 0).getbbox()).resize((10,10),Image.Resampling.LANCZOS)
    pulse=.18+.82*(.5+.5*math.cos(t*math.tau/.85))
    bright=lamp.convert('L').point(lambda v:max(0,min(255,(v-90)*3)))
    dark=Image.new('RGBA',lamp.size,(9,20,29,255))
    dark.putalpha(ImageChops.multiply(bright,lamp.getchannel('A')))
    lamp.alpha_composite(dark)
    light=Image.new('RGBA',lamp.size,color+(255,))
    light.putalpha(ImageChops.multiply(bright,lamp.getchannel('A')).point(lambda v:round(v*pulse)))
    lamp.alpha_composite(light);fx.alpha_composite(lamp,(center[0]-5,center[1]-5))
    return fx

def main():
    data=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    data['states']=[s for s in data['states'] if not s['id'].startswith('work-')]
    clips={};checks=[]
    for name in ['mine','collect','weld','repair']:
        source=Image.open(ROOT/data['actions'][name]['pose']).convert('RGBA')
        body_dir=ROOT/'frames'/f'work-{name}-south';body_dir.mkdir(parents=True,exist_ok=True)
        effect_dir=ROOT/'effects'/name;effect_dir.mkdir(parents=True,exist_ok=True)
        bodies=[];effects=[];clips[name]=[]
        for n in range(N):
            im,fx=work_frame(name,source,n)
            path=body_dir/f'{n:03}.png';im.save(path);bodies.append(path.relative_to(ROOT).as_posix())
            path=effect_dir/f'{n:03}.png';fx.save(path);effects.append(path.relative_to(ROOT).as_posix())
            bbox=im.getbbox();assert bbox and min(bbox[:2])>0 and max(bbox[2:])<SIZE
            composed=im.copy();composed.alpha_composite(fx);composed.alpha_composite(lamp_layer(n/FPS,center=(128,121)))
            clips[name].append(composed)
        data['states'].append({'id':f'work-{name}-south','frameFiles':bodies,'effectFiles':effects,'frameCount':N,'fps':FPS,'loop':True,'statusLayer':'independent',
                               'method':'authored work contact; local raster articulation and separate operation effects'})
        data['actions'][name]['phaseChain']=['work contact','tool activity','settle']
        data['actions'][name]['limits']='South-facing work loop; full approach/reach/release transition clips still needed.'
        checks.append({'action':name,'bodyFrames':N,'effectFrames':N,'borders':'pass'})
    data['statusClips']={}
    for name,color in [('operational',(48,155,255)),('stopped',(255,48,46)),('charging',(255,205,45))]:
        folder=ROOT/'status'/name;folder.mkdir(parents=True,exist_ok=True);paths=[]
        for n in range(51):
            path=folder/f'{n:03}.png';lamp_layer(n/FPS,color).save(path);paths.append(path.relative_to(ROOT).as_posix())
        data['statusClips'][name]={'frameFiles':paths,'frameCount':51,'fps':30,'anchor':[128,128],'loop':True}
    frames=[]
    for n in range(N):
        canvas=Image.new('RGB',(1080,490),'#18272f');d=ImageDraw.Draw(canvas)
        d.text((20,16),'WORK LOOPS / independent top status pulse and operation effects',font=FONT,fill='#dfeaf0')
        for i,name in enumerate(clips):
            im=clips[name][n];canvas.paste(im,(i*270+7,58),im)
            d.text((i*270+20,43),name.upper(),font=FONT,fill='#cadce5')
            small=im.resize((87,87),Image.Resampling.LANCZOS);canvas.paste(small,(i*270+92,342),small)
        d.text((20,456),'Contact-loop studies. Work actions face south; eight headings are available for travel.',font=FONT,fill='#abc0ca')
        frames.append(canvas)
    frames[0].save(ROOT/'review/work-loops.gif',save_all=True,append_images=frames[1:],duration=[33,33,34]*34,loop=0,optimize=False)
    for n in [0,15,35,60,90]:frames[n].save(ROOT/'review'/f'work-phase-{n:02}.png')
    (ROOT/'manifest.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    (ROOT/'review/work-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    print(json.dumps(checks))

if __name__=='__main__':main()
