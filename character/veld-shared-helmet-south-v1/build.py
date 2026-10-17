"""Rebuild Veld's south helmet study from the preserved generated cutout."""

import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "shared-helmet-standard-v1" / "veld-south-reference.png"
BASE = ROOT / "crew-runtime-matte-v1" / "veld"
OUT = Path(__file__).resolve().parent


def helmet() -> Image.Image:
    src = Image.open(SOURCE).convert("RGBA")
    bounds = src.getchannel("A").point(lambda a: 255 if a > 24 else 0).getbbox()
    if bounds is None:
        raise ValueError("Helmet source has no opaque content")
    src = src.crop(bounds).resize((35, 39), Image.Resampling.LANCZOS)
    a = np.asarray(src, dtype=np.uint8).copy()
    rgb = a[:, :, :3].astype(np.float32)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    # Bring generated skin and reflective trim back into the installed matte range.
    skin = (r > g * 1.17) & (g > b * 1.12) & (r > 110)
    rgb[skin] *= np.array([0.83, 0.83, 0.85])
    neutral = (np.max(rgb, axis=2) - np.min(rgb, axis=2) < 38) & (rgb.mean(axis=2) > 145)
    neutral[:12, 13:22] = False  # keep the lamp white
    rgb[neutral] *= 0.86
    a[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def main() -> None:
    helm = helmet()
    helm.save(OUT / "fitted-helmet.png")
    manifest = json.loads((BASE / "manifest.json").read_text(encoding="utf-8"))
    checks = {"source": str(SOURCE.relative_to(ROOT)), "helmetSize": [35, 39], "states": {}, "installed": True}
    tracks = []
    for state in manifest["states"]:
        if state["id"] not in {"idle-south", "walk-south"}:
            continue
        key = "idle" if state["id"].startswith("idle") else "walk"
        folder = OUT / key
        folder.mkdir(parents=True, exist_ok=True)
        for i, rel in enumerate(state["frameFiles"]):
            bare = Image.open(BASE / rel).convert("RGBA")
            equipped = bare.copy()
            equipped.alpha_composite(helm, (76, 12 if key == "walk" else 17))
            if bare.crop((0, 57, 184, 184)).tobytes() != equipped.crop((0, 57, 184, 184)).tobytes():
                raise AssertionError("Body changed below helmet")
            equipped.save(folder / f"{i:03d}.png")
        checks["states"][key] = {"frames": len(state["frameFiles"]), "durationMs": sum(state["frameDurationsMs"]), "bodyBelow57Exact": True}
        tracks.extend([
            {"label": f"Bare south {key}", "files": ["../crew-runtime-matte-v1/veld/" + rel.replace("\\", "/") for rel in state["frameFiles"]], "durations": state["frameDurationsMs"]},
            {"label": f"Helmet south {key} - study", "files": [f"{key}/{i:03d}.png" for i in range(len(state["frameFiles"]))], "durations": state["frameDurationsMs"]},
        ])
    (OUT / "checks.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")
    data = json.dumps(tracks, separators=(",", ":"))
    html = """<!doctype html><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Veld south helmet study</title><style>body{margin:0;padding:18px;background:#152027;color:#e5eff1;font:16px system-ui}h1{font-size:24px}p{max-width:72ch;color:#bed0d3}.row{display:flex;gap:12px;flex-wrap:wrap}.card{background:#22333c;border:1px solid #4b646a;border-radius:8px;padding:10px;text-align:center;width:190px}canvas{display:block}select,button{font:inherit;background:#253f47;color:white;padding:6px;border:1px solid #65838a;border-radius:5px}</style><h1>Veld - south helmet study</h1><p>New compact shared-shell front view with Veld's own face. Compare bare and equipped idle/walk at 148, 82, 54 or 27 pixel height. This front fit is installed in Veld's four-direction idle/walk helmet profile.</p><label>Game height <select id=size><option>148</option><option>82</option><option>54</option><option>27</option></select></label> <button id=play>Pause</button> <span id=status>Loading</span><div class=row id=row></div><script>const tracks=TRACKS;let playing=true,time=0,last=performance.now();for(const t of tracks){const c=document.createElement('div');c.className='card';c.innerHTML='<strong>'+t.label+'</strong><canvas width=184 height=184></canvas><small>Head close-up</small><canvas width=184 height=170></canvas>';document.querySelector('#row').append(c);t.full=c.querySelectorAll('canvas')[0];t.head=c.querySelectorAll('canvas')[1]}document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};Promise.all(tracks.map(async t=>{t.images=await Promise.all(t.files.map(f=>new Promise((yes,no)=>{const im=new Image;im.onload=()=>yes(im);im.onerror=()=>no(new Error(f));im.src=f})));t.total=t.durations.reduce((a,b)=>a+b,0)})).then(()=>{document.querySelector('#status').textContent='All four animations loaded';function draw(now){if(playing)time+=now-last;last=now;const h=Number(document.querySelector('#size').value);for(const t of tracks){let v=time%t.total,i=0;while(i<t.images.length-1&&v>=t.durations[i])v-=t.durations[i++];const a=t.full.getContext('2d'),b=t.head.getContext('2d');a.clearRect(0,0,184,184);b.clearRect(0,0,184,170);a.drawImage(t.images[i],(184-h)/2,180-h,h,h);b.imageSmoothingEnabled=false;b.drawImage(t.images[i],70,10,48,53,14,0,156,170)}requestAnimationFrame(draw)}requestAnimationFrame(draw)}).catch(e=>document.querySelector('#status').textContent='Missing: '+e.message)</script>""".replace("TRACKS", data)
    (OUT / "index.html").write_text(html, encoding="utf-8")
    print(json.dumps(checks))


if __name__ == "__main__":
    main()
