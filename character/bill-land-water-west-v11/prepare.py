from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-land-water-west-v10/build.py').read_text(encoding='utf-8')
changes={
"OLD=R/'bill-land-water-west-v9'":"OLD=R/'bill-land-water-west-v10'",
"raw=S/'prone-flat-v3.png'":"raw=S/'prone-legs-v4.png'",
"Bill West original-master near-prone candidate":"Bill West original-master near-prone leg revision",
"Pose5 independently authored from original West master, then original-head reference repair. Same148/956 source density; whole-figure crown translation to prior pose5 registration, no support/height/limb fitting. Other six poses exactV9. Source candidate unselected.":"Pose5 source anatomical thigh/shin revision against original West master. Same148/956 source density; whole-figure crown translation to prior pose5 registration, no occupied-height/width or limb transforms. Other six poses exactV10. Source candidate unselected.",
}
for a,b in changes.items():
    assert a in s,a
    s=s.replace(a,b)
line=next(l for l in s.splitlines() if l.startswith('inputs='))
s=s.replace(line,"inputs=[OLD/'sources/prone-flat-v3.png',OLD/'review.json',OLD/'helmet-registration.json',R/'crew-side-masters-v1/bill-side-master-01.png',raw,S/'prone-legs-prompt-v4.txt',OLD/'bare/manifest.json',OLD/'helmet/manifest.json',R/'bill-cargo-helmet-west-v1/sources/canonical-head.png']+[OLD/g/f'frames/land-swim-west/{i:03}.png' for g in ['bare','helmet'] for i in range(7)]")
line=next(l for l in s.splitlines() if l.startswith('html='))
s=s.replace(line,"html=(OLD/'index.html').read_text(encoding='utf-8').replace('West near-prone study','West near-prone leg study').replace('This candidate restores the near-prone pose from the original master; complete proportions, colour and moving review remain pending.','This candidate revises near-prone thigh and shin proportions against the original master. Full body and swimming endpoint consistency remain pending.');(P/'index.html').write_text(html,encoding='utf-8')")
(P/'build.py').write_text(s,encoding='utf-8')
print('Prepared master limb revision at fixed physical source density.')
