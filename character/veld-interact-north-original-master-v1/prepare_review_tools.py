from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
code=(R/'character/veld-idle-west-original-master-v1/review_source.py').read_text()
code=code.replace("P/'original-idle-master.png'","P/'prepared-idle-master.png'")
code=code.replace('character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png','character/veld-helmet-original-turntable-v1/v3-study/shells/000.png').replace('==(33,39)','==(34,36)').replace('(117,76,150,103)','(115,77,143,103)').replace('(116,65)','(112,68)').replace('[65:104,116:150]','[68:104,112:146]')
code=code.replace('source-idle-west','source-interact-north').replace("['west']","['north']").replace("['idle']","['interact']").replace('Veld original West idle','Veld original-guided North scanner').replace('character/veld-idle-west-original-master-v1/frames/','character/veld-interact-north-original-master-v1/frames/')
code=code.replace('position=[116,65],clear=[117,76,150,103]','position=[112,68],clear=[115,77,143,103]')
# Keep the exact prepared control and unmodified legacy original distinct.
code=code.replace("ims=[master,control]+[frames[i] for i in [0,35,71,106,len(frames)-1]]","ims=[Image.open(P/'original-idle-master.png').convert('RGBA'),master,control]+[frames[i] for i in [0,35,71,106,len(frames)-1]]")
code=code.replace('(1792,560)','(2048,560)').replace("['Master','Input control','Source0','Source35','Source71','Source106','Source last']","['Original','Prepared master','Input control','Source0','Source35','Source71','Source106','Source last']")
code=code.replace("P/'prepared-idle-master.png',shell_path","P/'prepared-idle-master.png',P/'original-idle-master.png',P/'INPUTS.json',shell_path")
(P/'review_source.py').write_text(code)
print('Frozen whole North source extraction/reference comparison tools prepared')
