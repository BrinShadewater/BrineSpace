"""Build a synchronized retained-versus-selected Bill east action review."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
OLD = ROOT / "major-bill-v3/packs/helmet-184x184-p92-172"
STATES = ("interact-east", "kneel-east", "repair-east", "stand-east")


def main() -> None:
    old = {s["id"]: s for s in json.loads((OLD / "manifest.json").read_text(encoding="utf-8"))["states"]}
    new = {s["id"]: s for s in json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))["states"]}
    checks = json.loads((HERE / "checks.json").read_text(encoding="utf-8"))
    tracks = []
    for state in STATES:
        for label, source, manifest in (("Retained", OLD, old[state]), ("Shared helmet + matte", HERE, new[state])):
            files = ["../" + str((source / f).resolve().relative_to(ROOT.resolve())).replace("\\", "/") for f in manifest["frameFiles"]]
            if not all((HERE / f).is_file() for f in files):
                raise FileNotFoundError(state)
            anchors = [entry["template"] if label == "Retained" else entry["helmet"] for entry in checks[state]]
            tracks.append({"label": state + " · " + label, "files": files, "durations": manifest["frameDurationsMs"], "anchors": anchors})
    data = json.dumps(tracks, separators=(",", ":"))
    html = r'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bill east action helmet review</title><style>
body{margin:0;padding:18px;background:#152027;color:#e5eff1;font:16px system-ui}h1{font-size:24px}p{max-width:80ch;color:#bed0d3}.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(188px,1fr));gap:10px;max-width:1500px}.card{background:#22333c;border:1px solid #4b646a;border-radius:8px;padding:8px;text-align:center}canvas{display:block;margin:auto;max-width:100%}select,button{font:inherit;background:#253f47;color:white;padding:6px;border:1px solid #65838a;border-radius:5px}.head{background:#273841;border-radius:5px}small{color:#afc1c6}
</style></head><body><h1>Bill — east actions, idle-led interaction</h1><p>Bill's new interaction keeps his accepted idle body, head and helmet while the complete retained arm moves from the shoulder. The kneel, repair and stand poses use the matching bare suit beneath the helmet, removing the retired collar fragment, matched suit tone and darker matte east shell. All timing is unchanged. Compare the idle-to-reach transition and the collar during the bend at full height and gameplay size.</p><label>Character height <select id=size><option>155</option><option>82</option><option>54</option><option>27</option></select></label> <button id=play>Pause</button> <span id=status>Loading</span><div class=row id=row></div><script>
const tracks=TRACKS;let playing=true,time=0,last=performance.now();for(const t of tracks){const card=document.createElement('div');card.className='card';card.innerHTML='<strong>'+t.label+'</strong><canvas width=184 height=184></canvas><small>Pose-tracked head and collar</small><canvas class=head width=184 height=170></canvas>';document.querySelector('#row').append(card);t.full=card.querySelectorAll('canvas')[0];t.head=card.querySelectorAll('canvas')[1]}document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};Promise.all(tracks.map(async t=>{t.images=await Promise.all(t.files.map(f=>new Promise((yes,no)=>{const im=new Image;im.onload=()=>yes(im);im.onerror=()=>no(new Error(f));im.src=f+'?v=bill-east-action-v4'})));t.total=t.durations.reduce((a,b)=>a+b,0)})).then(()=>{document.querySelector('#status').textContent='All eight animations loaded';function draw(now){if(playing)time+=now-last;last=now;const scale=Number(document.querySelector('#size').value)/155;for(const t of tracks){let v=time%t.total,i=0;while(i<t.images.length-1&&v>=t.durations[i])v-=t.durations[i++];const im=t.images[i],a=t.full.getContext('2d'),b=t.head.getContext('2d');a.clearRect(0,0,184,184);b.clearRect(0,0,184,170);a.drawImage(im,92-92*scale,180-172*scale,184*scale,184*scale);b.imageSmoothingEnabled=false;const [x,y]=t.anchors[i];b.drawImage(im,x-10,y-7,56,56,8,0,168,168)}requestAnimationFrame(draw)}requestAnimationFrame(draw)}).catch(e=>document.querySelector('#status').textContent='Missing: '+e.message)
</script></body></html>'''.replace("TRACKS", data)
    (HERE / "index.html").write_text(html, encoding="utf-8")
    print(f"{len(tracks)} tracks, {sum(len(t['files']) for t in tracks)} frame references")


if __name__ == "__main__":
    main()

