from pathlib import Path
P=Path(__file__).resolve().parent
H=P.parent/'bill-seated-helmet-east-coherent-v1';H.mkdir(exist_ok=True)
text=(P.parent/'bill-recover-air-helmet-east-coherent-v1/build.py').read_text()
text=text.replace('bill-recover-air-east-coherent-v1','bill-seated-east-coherent-v1').replace('if i in [0,5]:','if i==0:').replace('Bill east helmet air recovery candidate','Bill east helmet sitting candidate').replace('exact equipped idle endpoints','exact equipped standing endpoint;seated loop pending').replace('Built east helmet recovery;native tilted head;exact idle ends','Built east helmet sitting;native tilted head;protected body')
text=text.replace("record['sourcePose']","record['frame']")
(H/'build.py').write_text(text)
print('Prepared native east helmet fitting for every authored sitting interior')
