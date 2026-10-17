"""Reuse verified single-pose packaging, with explicit push-off substitutions."""
from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-land-water-west-v6/build.py').read_text(encoding='utf-8')
changes={
"OLD=R/'bill-land-water-west-v5'":"OLD=R/'bill-land-water-west-v6'",
"raw=S/'crouch-master-v2.png'":"raw=S/'push-off-master-v1.png'",
"shift=(148-crown,224-sole)":"shift=(140-crown,117-top)",
"frames[2]=out":"frames[3]=out",
"unchanged=[0,1,3,4,5,6]":"unchanged=[0,1,2,4,5,6]",
"Bill West original-master crouch candidate":"Bill West original-master push-off candidate",
"Pose2 newly authored from sole original directional master at148/956 source density, complete anatomy articulated at knees/hips/shoulders. Whole-figure registration only. Other six poses exactV5. Source candidate unselected.":"Pose3 newly authored from sole original directional master at148/956 source density, complete airborne push-off articulation. Whole-figure crown translation only, no support fitting. Other six poses exactV6. Source candidate unselected.",
"('Repaired arm-ready',Image.open(OLD/gear/'frames/land-swim-west/001.png')":"('Repaired crouch',Image.open(OLD/gear/'frames/land-swim-west/002.png')",
"('Previous crouch',Image.open(OLD/gear/'frames/land-swim-west/002.png')":"('Previous push-off',Image.open(OLD/gear/'frames/land-swim-west/003.png')",
"('New master crouch',Image.open(P/gear/'frames/land-swim-west/002.png')":"('New master push-off',Image.open(P/gear/'frames/land-swim-west/003.png')",
"master-crouch-comparison.png":"master-push-comparison.png",
"S/'crouch-master-prompt-v2.txt'":"S/'push-off-master-prompt-v1.txt'",
"Single original-master crouch repair; candidate only.":"Single original-master push-off repair; candidate only.",
"registeredCrown=crowns[1],opaqueSupportAfter=224":"registeredCrown=crowns[2],opaqueSupportAfter=sole+shift[1]",
}
for a,b in changes.items():
    assert a in s,a
    s=s.replace(a,b)
line=next(l for l in s.splitlines() if l.startswith('html='))
new="html=(OLD/'index.html').read_text(encoding='utf-8').replace('Standing and arm-ready remain unchanged. The new crouch follows the original master’s anatomy and drawing scale. Remaining poses still need consistency review.','Standing, arm-ready and crouch remain unchanged. The new push-off follows the original master’s anatomy and drawing scale. Materials and moving joins still need consistency review.').replace('Original master and preceding crouch','Original master and preceding push-off').replace('master-crouch-comparison.png','master-push-comparison.png').replace('Master and preceding crouch comparison','Master and preceding push-off comparison');(P/'index.html').write_text(html,encoding='utf-8')"
s=s.replace(line,new)
(P/'build.py').write_text(s,encoding='utf-8')
print('Prepared single-pose push-off builder; source still needed before building.')
