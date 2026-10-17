from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-land-water-west-v8/build.py').read_text(encoding='utf-8')
changes={
"OLD=R/'bill-land-water-west-v7'":"OLD=R/'bill-land-water-west-v8'",
"raw=S/'lift-master-v2.png'":"raw=S/'lift-head-v4.png'",
"shift=(130-crown,150-top)":"shift=tuple(json.loads((OLD/'review.json').read_text(encoding='utf-8'))['translation'])",
"Bill West original-master levelling candidate":"Bill West levelling head and two-hand repair candidate",
"Pose4 newly authored from sole original directional master at148/956 source density, complete levelling-out articulation. Whole-figure crown translation only, no support fitting. Other six poses exactV7. Source candidate unselected.":"Pose4 head/two-hand edit ofV8 with original master identity reference. Same148/956 source density and preceding whole-source translation, no crown/height/limb fitting. Other six poses exactV8. Source candidate unselected.",
"('Repaired push-off',Image.open(OLD/gear/'frames/land-swim-west/003.png')":"('Repaired push-off',Image.open(OLD/gear/'frames/land-swim-west/003.png')",
"('Previous levelling'":"('V8 broad-head levelling'",
"('New master levelling'":"('Head/two-hand repair'",
"S/'lift-master-prompt-v2.txt'":"S/'lift-head-prompt-v4.txt'",
"Single original-master levelling repair; candidate only.":"Levelling head/two-hand repair; candidate only.",
}
for a,b in changes.items():
    assert a in s,a
    s=s.replace(a,b)
line=next(l for l in s.splitlines() if l.startswith('html='))
new="html=(OLD/'index.html').read_text(encoding='utf-8').replace('The first four poses remain unchanged. Bent elbows reduce excessive reach, but this candidate still needs a narrower master-matched head and clearer separation between the hands.','The first four poses remain unchanged. This candidate repairs the levelling head and two-hand anatomy; complete master, colour and motion review remains pending.');(P/'index.html').write_text(html,encoding='utf-8')"
s=s.replace(line,new)
line=next(l for l in s.splitlines() if l.startswith('inputs='))
s=s.replace(line,line.replace("inputs=[","inputs=[S/'master-head-reference.png',S/'lift-head-hands-v3.png',S/'lift-head-hands-prompt-v3.txt',OLD/'review.json',OLD/'sources/lift-master-v2.png',"))
(P/'build.py').write_text(s,encoding='utf-8')
print('Prepared head/hand builder retaining preceding whole-source translation.')
