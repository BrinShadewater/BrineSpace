from pathlib import Path
p=Path(__file__).resolve().parent
text=(p/'package-west-bridge-v3.gd').read_text()
text=text.replace('west-bridge-generated-v3.png','west-bridge-generated-v4.png').replace('frames-v3','frames-v4').replace('manifest-v3','manifest-v4').replace('package-v3-evidence','package-v4-evidence').replace('package-west-bridge-v3','package-west-bridge-v4').replace('BRIDGE V3','BRIDGE V4').replace('bridge v3','bridge v4')
text=text.replace('range(460,495)','range(463,498)').replace('217','215').replace('495','498').replace('350','353')
old='var frame:Image=original.duplicate();frame.blit_rect(sources[i],WINDOW,WINDOW.position)'
new='''var frame:Image=original.duplicate()
			if i<2:
				if frame.load(OUT+"frames-v3/"+mode+"/%03d.png"%i)!=OK:quit(2);return
				frame.convert(Image.FORMAT_RGBA8)
			else:frame.blit_rect(sources[i],WINDOW,WINDOW.position)'''
assert text.count(old)==1;text=text.replace(old,new)
old='files.append(file)'
new='''if i<2 and FileAccess.get_file_as_bytes(OUT+file)!=FileAccess.get_file_as_bytes(OUT+"frames-v3/"+mode+"/%03d.png"%i):push_error("Retained first pose bytes changed");quit(2);return
			files.append(file)'''
assert text.count(old)==1;text=text.replace(old,new)
(p/'package-west-bridge-v4.gd').write_text(text)
text=(p/'validate-west-bridge-v3.gd').read_text().replace('manifest-v3','manifest-v4').replace('frames-v3','frames-v4').replace('validate-west-bridge-v3','validate-west-bridge-v4').replace('native-v3-evidence','native-v4-evidence').replace('BRIDGE V3','BRIDGE V4')
(p/'validate-west-bridge-v4.gd').write_text(text)
print('Prepared final-pose-only native repair; first two poses retained byte-exact.')
