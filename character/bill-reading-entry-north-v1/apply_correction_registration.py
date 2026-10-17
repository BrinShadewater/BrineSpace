from pathlib import Path
P=Path(__file__).resolve().parent
path=P/'build.py';text=path.read_text()
text=text.replace('from scipy.ndimage import binary_dilation','from scipy.ndimage import binary_dilation\nfrom correction import prepare as prepare_correction')
text=text.replace('corrected=module.prepare(P/\'sources/entry-right-arm-v2.png\',heads,6,1.4)','corrected=prepare_correction(P/\'sources/entry-right-arm-v2.png\',heads,primary[-1])')
text=text.replace('(768,535)','(768,538)')
text=text.replace('raw,labs,ids,grade,curve=corrected if i==1 else primary','raw,labs,ids,grade,curve=corrected if i==1 else primary\n  sx,sy=(.214,.2455) if i==1 else (.214,.251)')
text=text.replace("'protectedBodyFromY':hy+31", "'protectedBodyFromY':hy+31,'fixedSourceRuler':[sx,sy],'source':'entry-right-arm-v2.png' if i==1 else 'entry-v1.png'")
text=text.replace("'correctedPose':1", "'correctedPose':1,'correctedGeneration':'exec-e66eb374-e924-4be9-8f4f-a905d3b27743','correctedOpaqueThreshold':240,'correctedRuler':[.214,.2455]")
path.write_text(text)
print('Corrected atlas: near-opaque segmentation, separately frozen source ruler, primary grade')
