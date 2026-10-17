from pathlib import Path
P=Path(__file__).resolve().parent
path=P/'build.py';text=path.read_text()
text=text.replace('[(281,9),(764,9),(1251,12),(280,525),(764,525),(1252,525)]','[(272,17),(768,17),(1264,17),(272,534),(768,535),(1264,535)]')
text=text.replace("raw,labs,ids,grade,curve=module.prepare(source,heads,6,1.4);sx,sy=.214,.251", "primary=module.prepare(source,heads,6,1.4);corrected=module.prepare(P/'sources/entry-right-arm-v2.png',heads,6,1.4);sx,sy=.214,.251")
text=text.replace('for i in [1,2,3,4]:\n  mask=', 'for i in [1,2,3,4]:\n  raw,labs,ids,grade,curve=corrected if i==1 else primary\n  mask=')
text=text.replace("'generation':'exec-0704b3ba-df13-49a6-ab8c-7c079ad29f01'", "'generation':'exec-a6999412-1ee7-47c1-a98e-41476adfece3','correctedSourceSha256':sha(P/'sources/entry-right-arm-v2.png'),'correctedPose':1")
text=text.replace("'grade':curve", "'grade':{'primary':primary[-1],'corrected':corrected[-1]}")
path.write_text(text)
print('Builder uses corrected right-arm pose only; remaining authored interiors from primary')
