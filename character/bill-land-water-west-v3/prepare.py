from pathlib import Path
P=Path(__file__).resolve().parent;OLD=P.parent/'bill-land-water-west-v2'
s=(OLD/'build.py').read_text(encoding='utf-8')
s=s.replace("('crouch',3,'exec-8b370156-7165-4781-8e72-8ade255a3b08'),('push',2,'exec-cd0be74a-4083-4b82-b17d-7049a30e2384')","('crouch',4,'exec-2c5760c3-9a86-44e2-83f3-ca31153cd4ed'),('push',3,'exec-23fd84d8-f757-4075-8d82-f3f87cd535f2')")
s=s.replace("S/'crouch-native-v3.png',S/'push-native-v2.png'","S/'crouch-native-v4.png',S/'push-native-v3.png'")
s=s.replace("OLD/f'bare/frames/land-swim-west/{i:03}.png'","P.parent/'bill-land-water-west-v2'/f'bare/frames/land-swim-west/{i:03}.png'")
s=s.replace('Five V1 poses exact; new independently authored compact crouch and push.','Five V2 poses exact; new original-master graphite quilting/badge detail crouch and push edits.')
s=s.replace("('V1 ' if row==0 else 'V2 ')","('V2 ' if row==0 else 'V3 ')")
s=s.replace('V1 above / V2 below','V2 above / V3 below').replace('Smaller crouch/push bodies; visual acceptance pending.','Crouch/push graphite texture and badge edits; complete material/identity acceptance pending.')
(P/'build.py').write_text(s,encoding='utf-8')
s=(OLD/'build_helmet.py').read_text(encoding='utf-8')
s=s.replace('HEADS=[(158,80),(147,114),(141,118),(130,150),(131,188)]','HEADS=[(158,80),(148,114),(140,117),(130,150),(131,188)]')
# Crown anchors were inspected at the common native ruler after both material edits.
(P/'build_helmet.py').write_text(s,encoding='utf-8')
print('Prepared sibling material/detail candidate. Historical source and native V2 proof unchanged.')
