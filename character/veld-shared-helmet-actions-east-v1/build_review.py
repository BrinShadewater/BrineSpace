"""Create an old/new animation review for Veld's east action helmet fit."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
CATALOG = ROOT / "dr-veld-v2"
STATES = ("interact-east", "kneel-east", "repair-east", "stand-east")


def main() -> None:
    catalog = json.loads((CATALOG / "catalog.json").read_text(encoding="utf-8"))
    old = {}
    for rel in catalog["equipment"]:
        path = CATALOG / rel
        manifest = json.loads(path.read_text(encoding="utf-8"))
        for state in manifest["states"]:
            if state["id"] in STATES:
                old[state["id"]] = (path.parent, state)
    new = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    new_states = {s["id"]: s for s in new["states"]}
    checks = json.loads((HERE / "checks.json").read_text(encoding="utf-8"))
    tracks = []
    for key in STATES:
        for label, root, state in (("Previous", *old[key]), ("Shared shell", HERE, new_states[key])):
            files = ["../" + str((root / f).relative_to(ROOT)).replace("\\", "/") for f in state["frameFiles"]]
            if not all((HERE / f).is_file() for f in files):
                raise FileNotFoundError(key)
            if label == "Shared shell":
                anchors = [[round((p["helmet"][0] - 8 - 92) * 1.10 + 104), round((p["helmet"][1] - 7 - 172) * 1.06 + 172)] for p in checks[key]]
            else:
                anchors = [[p["template"][0] - 14, p["template"][1] - 9] for p in checks[key]]
            tracks.append({"label": f"{key} - {label}", "files": files, "durations": state["frameDurationsMs"], "anchors": anchors})
    data = json.dumps(tracks, separators=(",", ":"))
    html = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Veld east action helmet fit</title><style>body{margin:0;padding:18px;background:#152027;color:#e5eff1;font:16px system-ui}h1{font-size:24px}p{max-width:78ch;color:#bed0d3}.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(188px,1fr));gap:10px;max-width:1500px}.card{background:#22333c;border:1px solid #4b646a;border-radius:8px;padding:8px;text-align:center}canvas{display:block;margin:auto;max-width:100%}select,button{font:inherit;background:#253f47;color:white;padding:6px;border:1px solid #65838a;border-radius:5px}.head{background:#273841;border-radius:5px}small{color:#afc1c6}</style></head><body><h1>Veld - east action helmet fit</h1><p>Previous equipped action art beside the installed shared-shell version. Interact, kneel, repair and stand keep their existing poses, hand positions, floor contact and timing. The first and last standing poses match the installed idle exactly. The head close-up follows each pose.</p><label>Game height <select id=size><option>148</option><option>82</option><option>54</option><option>27</option></select></label> <button id=play>Pause</button> <span id=status>Loading</span><div class=row id=row></div><script>const tracks=TRACKS;let playing=true,time=0,last=performance.now();for(const t of tracks){const c=document.createElement('div');c.className='card';c.innerHTML='<strong>'+t.label+'</strong><canvas width=184 height=184></canvas><small>Pose-tracked head close-up</small><canvas class=head width=184 height=170></canvas>';document.querySelector('#row').append(c);t.full=c.querySelectorAll('canvas')[0];t.head=c.querySelectorAll('canvas')[1]}document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};Promise.all(tracks.map(async t=>{t.images=await Promise.all(t.files.map(f=>new Promise((yes,no)=>{const im=new Image;im.onload=()=>yes(im);im.onerror=()=>no(new Error(f));im.src=f})));t.total=t.durations.reduce((a,b)=>a+b,0)})).then(()=>{document.querySelector('#status').textContent='All eight animations loaded';function draw(now){if(playing)time+=now-last;last=now;const h=Number(document.querySelector('#size').value);for(const t of tracks){let v=time%t.total,i=0;while(i<t.images.length-1&&v>=t.durations[i])v-=t.durations[i++];const a=t.full.getContext('2d'),b=t.head.getContext('2d');a.clearRect(0,0,184,184);b.clearRect(0,0,184,170);a.drawImage(t.images[i],(184-h)/2,180-h,h,h);b.imageSmoothingEnabled=false;b.drawImage(t.images[i],t.anchors[i][0],t.anchors[i][1],48,52,14,0,156,170)}requestAnimationFrame(draw)}requestAnimationFrame(draw)}).catch(e=>document.querySelector('#status').textContent='Missing: '+e.message)</script></body></html>""".replace("TRACKS", data)
    html = html.replace("The head close-up follows each pose.</p>", "The head close-up follows each pose. The helmet tracks the suit collar through the forward lean, with a narrow graphite seal closing the rear-neck gap.</p>")
    html = html.replace("im.src=f}", "im.src=f+'?v=neck-seal-v1'}")
    (HERE / "index.html").write_text(html, encoding="utf-8")
    print(f"{len(tracks)} tracks, {sum(len(t['files']) for t in tracks)} frame references")


if __name__ == "__main__":
    main()
