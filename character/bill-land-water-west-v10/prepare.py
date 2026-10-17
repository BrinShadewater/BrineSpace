from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-land-water-west-v9/build.py').read_text(encoding='utf-8')
changes={
"OLD=R/'bill-land-water-west-v8'":"OLD=R/'bill-land-water-west-v9'",
"raw=S/'lift-head-v4.png'":"raw=S/'prone-flat-v3.png'",
"shift=tuple(json.loads((OLD/'review.json').read_text(encoding='utf-8'))['translation'])":"target=next(f['bareCrown'] for f in json.loads((OLD/'helmet-registration.json').read_text(encoding='utf-8'))['frames'] if f['pose']==5);shift=(target[0]-crown,target[1]-top)",
"frames[4]=out":"frames[5]=out",
"unchanged=[0,1,2,3,5,6]":"unchanged=[0,1,2,3,4,6]",
"Bill West levelling head and two-hand repair candidate":"Bill West original-master near-prone candidate",
"Pose4 head/two-hand edit ofV8 with original master identity reference. Same148/956 source density and preceding whole-source translation, no crown/height/limb fitting. Other six poses exactV8. Source candidate unselected.":"Pose5 independently authored from original West master, then original-head reference repair. Same148/956 source density; whole-figure crown translation to prior pose5 registration, no support/height/limb fitting. Other six poses exactV9. Source candidate unselected.",
"('Repaired push-off',Image.open(OLD/gear/'frames/land-swim-west/003.png')":"('Repaired levelling',Image.open(OLD/gear/'frames/land-swim-west/004.png')",
"('V8 broad-head levelling',Image.open(OLD/gear/'frames/land-swim-west/004.png')":"('Previous near-prone',Image.open(OLD/gear/'frames/land-swim-west/005.png')",
"('Head/two-hand repair',Image.open(P/gear/'frames/land-swim-west/004.png')":"('New master near-prone',Image.open(P/gear/'frames/land-swim-west/005.png')",
"S/'master-head-reference.png',S/'lift-head-hands-v3.png',S/'lift-head-hands-prompt-v3.txt',OLD/'review.json',OLD/'sources/lift-master-v2.png'":"OLD/'sources/master-head-reference.png',S/'prone-master-v1.png',S/'prone-master-prompt-v1.txt',OLD/'review.json',OLD/'helmet-registration.json'",
"S/'lift-head-prompt-v4.txt'":"S/'prone-flat-prompt-v3.txt',S/'prone-head-v2.png',S/'prone-head-prompt-v2.txt'",
"Levelling head/two-hand repair; candidate only.":"Original-master near-prone repair; candidate only.",
"registeredCrown=crowns[3]":"registeredCrown=crowns[4]",
}
for a,b in changes.items():
    assert a in s,a
    s=s.replace(a,b)
line=next(l for l in s.splitlines() if l.startswith('html='))
s=s.replace(line,"html=(OLD/'index.html').read_text(encoding='utf-8').replace('West levelling study','West near-prone study').replace('The first four poses remain unchanged. This candidate repairs the levelling head and two-hand anatomy; complete master, colour and motion review remains pending.','The first five poses remain unchanged. This candidate restores the near-prone pose from the original master; complete proportions, colour and moving review remain pending.');(P/'index.html').write_text(html,encoding='utf-8')")
(P/'build.py').write_text(s,encoding='utf-8')
print('Prepared pose5 builder with original drawing density and preceding crown registration.')
