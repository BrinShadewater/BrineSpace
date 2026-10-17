from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-land-water-west-v7/build.py').read_text(encoding='utf-8')
changes={
"OLD=R/'bill-land-water-west-v6'":"OLD=R/'bill-land-water-west-v7'",
"raw=S/'push-off-master-v1.png'":"raw=S/'lift-master-v2.png'",
"shift=(140-crown,117-top)":"shift=(130-crown,150-top)",
"frames[3]=out":"frames[4]=out",
"unchanged=[0,1,2,4,5,6]":"unchanged=[0,1,2,3,5,6]",
"Bill West original-master push-off candidate":"Bill West original-master levelling candidate",
"Pose3 newly authored from sole original directional master at148/956 source density, complete airborne push-off articulation. Whole-figure crown translation only, no support fitting. Other six poses exactV6. Source candidate unselected.":"Pose4 newly authored from sole original directional master at148/956 source density, complete levelling-out articulation. Whole-figure crown translation only, no support fitting. Other six poses exactV7. Source candidate unselected.",
"('Repaired crouch',Image.open(OLD/gear/'frames/land-swim-west/002.png')":"('Repaired push-off',Image.open(OLD/gear/'frames/land-swim-west/003.png')",
"('Previous push-off',Image.open(OLD/gear/'frames/land-swim-west/003.png')":"('Previous levelling',Image.open(OLD/gear/'frames/land-swim-west/004.png')",
"('New master push-off',Image.open(P/gear/'frames/land-swim-west/003.png')":"('New master levelling',Image.open(P/gear/'frames/land-swim-west/004.png')",
"master-push-comparison.png":"master-lift-comparison.png",
"S/'push-off-master-prompt-v1.txt'":"S/'lift-master-prompt-v2.txt'",
"Single original-master push-off repair; candidate only.":"Single original-master levelling repair; candidate only.",
"registeredCrown=crowns[2]":"registeredCrown=crowns[3]",
}
for a,b in changes.items():
    assert a in s,a
    s=s.replace(a,b)
line=next(l for l in s.splitlines() if l.startswith('html='))
new="html=(OLD/'index.html').read_text(encoding='utf-8').replace('Standing, arm-ready and crouch remain unchanged. The new push-off follows the original master’s anatomy and drawing scale. Materials and moving joins still need consistency review.','The first four poses remain unchanged. Bent elbows reduce excessive reach, but this candidate still needs a narrower master-matched head and clearer separation between the hands.').replace('Original master and preceding push-off','Original master and preceding levelling pose').replace('master-push-comparison.png','master-lift-comparison.png').replace('Master and preceding push-off comparison','Master and preceding levelling comparison');(P/'index.html').write_text(html,encoding='utf-8')"
s=s.replace(line,new)
(P/'build.py').write_text(s,encoding='utf-8')
print('Prepared single-pose levelling builder; awaits selected raw.')
