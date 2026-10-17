from pathlib import Path
P=Path(__file__).resolve().parent;OLD=P.parent/'bill-land-water-north-v2'
s=(OLD/'build.py').read_text(encoding='utf-8')
s=s.replace("OLD=R/'bill-land-water-north-v1'", "OLD=R/'bill-land-water-north-v2'")
s=s.replace('lift-atlas-v2.png','reach-atlas-v3.png').replace('lift-prompt-v2.txt','reach-prompt-v3.txt')
s=s.replace('raw.crop((0,512,512,1024))','raw.crop((1024,0,1536,512))')
s=s.replace('(xx>245)&(xx<305)&(yy>65)&(yy<128)','(xx>204)&(xx<246)&(yy>65)&(yy<128)')
s=s.replace('264<=axis<=284 and 575<=top+512<=605','214<=axis<=234 and 70<=top<=100')
s=s.replace('169-round(top*.25)','145-round(top*.25)')
s=s.replace('old=frames[5];frames[5]=out', '''old=frames[4]
# Preserve original torso below articulated arms, belt/hips/legs/boots exactly.
pixels=np.array(out);previous=np.array(old);pixels[180:]=previous[180:];out=Image.fromarray(pixels)
assert np.array_equal(np.array(out)[180:],previous[180:])
frames[4]=out''')
s=s.replace('i!=5','i!=4').replace('axial lift','intermediate reach').replace('Axial lift','Intermediate reach')
s=s.replace('lift5','reach4').replace("['registrations'][4]","['registrations'][3]")
s=s.replace('sourceCell=[0,512,512,1024],headAnchor=[160,169],sourceHairCrown=[axis,top+512]','sourceCell=[1024,0,1536,512],headAnchor=[160,145],sourceHairCrown=[axis+1024,top]')
s=s.replace("'pose':5", "'pose':4").replace("'replacementPose':5", "'replacementPose':4")
s=s.replace('exec-923168a1-d880-4777-9f60-5c30e92d20ad','exec-19342959-9ddd-4f29-9e5c-d05e0d355ed0')
s=s.replace("'sourceHairCrown':[axis,top+512]", "'sourceHairCrown':[axis+1024,top]")
s=s.replace("'sourceCrown':[axis,top+512]", "'sourceCrown':[axis+1024,top]")
start=s.index("for col,(label,im) in enumerate(");end=s.index('\n    board.paste',start)
s=s[:start]+"for col,(label,im) in enumerate([('preceding deep crouch',frames[3]),('old full reach',old),('new bent-elbow reach',out),('next corrected lift',frames[5]),('selected idle/master ruler',frames[0])]):"+s[end:]
s=s.replace('lift-comparison.png','reach-comparison.png')
s=s.replace("text=(OLD/file).read_text(encoding='utf-8')", "text=(OLD/file).read_text(encoding='utf-8')\n    if file=='build_review.py':text=text.replace('Axial lift revision;', 'Bent-elbow reach revision;')")
(P/'build.py').write_text(s,encoding='utf-8')
print('Prepared pose4-only reach revision, fixed density and protected lower body.')
