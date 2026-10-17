from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
test=(ROOT/'tests/test_bill_reading_entry_east_candidates.gd').read_text().replace('bill-reading-entry-east-v1','bill-inspect-entry-east-v1').replace('bill-reading-entry-east-candidate-native-v1','bill-inspect-entry-east-candidate-native-v1').replace('==40.0','==0.0').replace('Dry seated depth','Dry standing depth').replace('BILL READING ENTRY','BILL INSPECT ENTRY EAST')
joins='''
			var idle_file: String="res://character/bill-seated-east-coherent-v1/frames/sit-down-east/000.png" if spec[1].is_empty() else "res://character/bill-seated-helmet-east-coherent-v1/frames/sit-down-east/000.png"
			var held_file: String="res://character/bill-inspect-east-coherent-v1/frames/bare/000.png" if spec[1].is_empty() else "res://character/bill-inspect-east-coherent-v1/frames/helmet/000.png"
			var entering: bool=state.id=="inspect-enter-east"
			check(row[0].get_image().get_data()==Image.load_from_file(idle_file if entering else held_file).get_data(),"Native exact first idle/held join")
			check(row[-1].get_image().get_data()==Image.load_from_file(held_file if entering else idle_file).get_data(),"Native exact final held/idle join")
'''
test=test.replace('\t\t\treviews.append(row)',joins+'\t\t\treviews.append(row)')
(ROOT/'tests/test_bill_inspect_entry_east_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_inspect_entry_east_candidates.gd.uid').write_text('uid://g7b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_reading_entry_east_candidate_validation.py').read_text().replace('bill-reading-entry-east-candidate-native-v1','bill-inspect-entry-east-candidate-native-v1').replace('test_bill_reading_entry_east_candidates','test_bill_inspect_entry_east_candidates').replace('BILL READING','BILL INSPECT')
(ROOT/'tools/run_bill_inspect_entry_east_candidate_validation.py').write_text(runner)
review=(P.parent/'bill-reading-entry-east-v1/build_review.py').read_text().replace('bill-seated-loops-east-v1','bill-inspect-east-coherent-v1').replace('read-seated-east','inspect-east').replace('east tablet transitions','east reader transitions').replace('Take out tablet, read, put it away. Exact seated/reading endpoint joins and native selected east helmet.','Draw the reader, inspect, stow. Exact standing idle/held endpoint joins and native selected east helmet.').replace('East seated/reading loop review','East standing inspection review')
(P/'build_review.py').write_text(review)
print('Prepared finite standing reader transition/player/join fixture')
