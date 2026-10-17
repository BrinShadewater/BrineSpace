from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'james-water-turn-family-v1/verify.py').read_text()
s=s.replace('james-water-turn-','james-water-cargo-turn-').replace("james-water-'+d","james-water-cargo-'+d").replace('swim-turn-','swim-carry-turn-').replace("'swim-'","'swim-carry-'").replace("key.split('-')[2:]","key.split('-')[3:]")
(P/'verify.py').write_text(s)
s=(P.parent/'james-water-turn-family-v1/native-staged.gd').read_text()
s=s.replace('james-water-turn-family-v1','james-water-cargo-turn-family-v1').replace('james-water-family-v1','james-water-cargo-family-v1').replace('swim-turn-','swim-carry-turn-').replace('"swim-"','"swim-carry-"').replace('"swim",','"swim-carry",').replace('key.get_slice("-",2)','key.get_slice("-",3)').replace('key.get_slice("-",3)\n\t\t\tvar row','key.get_slice("-",4)\n\t\t\tvar row').replace('JAMES WATER TURNS STAGED','JAMES WATER CARGO TURNS STAGED')
(P/'native-staged.gd').write_text(s)
print('Prepared exact cargo endpoints, reverse/composition and native playback verification')
