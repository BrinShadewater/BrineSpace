from pathlib import Path
import json,sys,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/"tools"))
from rebuild_bill_art import HelmetRebaker,tilted
from build_bill_west_style_actions import solid
SRC=Path(__file__).resolve().parent;OUT=ROOT/"output/bill-south-endpoint-review-2026-09-21/candidate";OUT.mkdir(exist_ok=True)
spec=json.loads((SRC/"registration.json").read_text());raw=solid(Image.open(SRC/"lowering-source.png"));scale=146/(spec["boxes"][0][3]-spec["boxes"][0][1]);kneel=[];placements=[]
for i,box in enumerate(spec["boxes"]):
    crop=raw.crop(box);crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
    pose=Image.new("RGBA",(256,256));paste=[128-crop.width//2,224-crop.height];pose.alpha_composite(crop,paste)
    a=np.array(pose)[:,:,3];yy,xx=np.indices(a.shape);contact=np.where((a>127)&(yy>=218)&(xx>=128))[1];dx=135-int(contact.min())
    pose=Image.new("RGBA",(256,256));paste[0]+=dx;pose.alpha_composite(crop,paste);kneel.append(pose);placements.append({"box":box,"paste":paste})
for variant in ["bare","helmet"]:
    ref=Image.open(SRC/f"{variant}-idle-reference.png").convert("RGBA");canvas=Image.new("RGBA",(256,256));canvas.alpha_composite(ref,(36,52))
    if variant=="bare":kneel[0]=canvas
    else:helmet_idle=canvas
# Fixed cell registration keeps original source timing/poses; only the hands change.
raw=solid(Image.open(SRC/"work-source.png"));width=raw.width//6;box=raw.crop((0,0,width,raw.height)).getbbox();target=kneel[-1].getbbox();workscale=(target[3]-target[1])/(box[3]-box[1]);paste=[128-round((box[0]+box[2])/2*workscale)-2,224-round(box[3]*workscale)]
mask=Image.new("L",(256,256));poly=[[108,170],[143,170],[148,179],[145,189],[111,189],[105,180]];ImageDraw.Draw(mask).polygon([tuple(v) for v in poly],fill=255)
work=[]
for i in range(6):
    pose=kneel[-1].copy()
    if i not in (0,5):
        crop=raw.crop((width*i,0,width*(i+1),raw.height));crop=crop.resize((round(crop.width*workscale),round(crop.height*workscale)),Image.Resampling.NEAREST);registered=Image.new("RGBA",(256,256));registered.alpha_composite(crop,paste);pose.paste(registered,(0,0),mask)
    work.append(pose)
heads=[]
for im in kneel:
    b=im.getbbox();heads.append([128,b[1]+16])
heads[3][0]+=1;heads[4][0]-=3;heads[5][0]-=2
bare={"kneel-south":kneel,"repair-south":work,"stand-south":list(reversed(kneel))};geared={};overlay=HelmetRebaker(None).overlay("front",(48,56))
for action,frames in bare.items():
    anchors=heads if action.startswith("kneel") else list(reversed(heads)) if action.startswith("stand") else [heads[-1]]*6
    geared[action]=[tilted(im,overlay,np.array(h)-[23,25],0,[h[0]-14,h[1]-20,28,34],"south") for im,h in zip(frames,anchors)]
geared["kneel-south"][0]=helmet_idle;geared["stand-south"][-1]=helmet_idle.copy()
timings={}
for file in (ROOT/"character/major-bill-v3/packs").glob("bare-*/manifest.json"):
    for entry in json.loads(file.read_text())["states"]:
        if entry["id"] in bare:timings[entry["id"]]=entry
for variant,collection in [("bare",bare),("helmet",geared)]:
    m={"name":"bill-south-style-"+variant,"frameWidth":256,"frameHeight":256,"pivot":[128,224],"standingHeight":148,"precomposed":True,"states":[]}
    for action,frames in collection.items():
        names=[]
        for i,im in enumerate(frames):
            name=f"{variant}-{action}-{i:03}.png";im.save(OUT/name);names.append(name)
        m["states"].append({"id":action,"frameFiles":names,"frameDurationsMs":timings[action]["frameDurationsMs"],"loop":timings[action]["loop"]})
    (OUT/f"{variant}-manifest.json").write_text(json.dumps(m,indent=2)+"\n")
sheet=Image.new("RGB",(1536,768),"#25313a");d=ImageDraw.Draw(sheet)
for row,frames in enumerate([kneel,work,geared["kneel-south"]]):
    for i,im in enumerate(frames):sheet.paste(im,(i*256,row*256),im);d.text((i*256+4,row*256+4),str(i),fill="white")
sheet.save(OUT/"review.png")
metadata={"status":"candidate, not installed","lowering":{"scale":scale,"frames":placements},"work":{"scale":workscale,"cell_width":width,"paste":paste,"replacement_polygon":poly},"head_anchors":heads,"overlay_size":[48,56],"overlay_anchor_offset":[23,25],"source_hashes":{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in SRC.glob("*.png")}}
(SRC/"candidate-registration.json").write_text(json.dumps(metadata,indent=2)+"\n")
print("36 review frames staged; exact standing endpoints; live durations preserved")
