import hashlib, importlib.util, json, tempfile, unittest, sys, io, contextlib
from pathlib import Path
spec=importlib.util.spec_from_file_location('manifest',Path(__file__).resolve().parents[1]/'tools/build_release_manifest.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class CrewSourceKeys(unittest.TestCase):
 def rows(self):
  return [{'path':'res://character/z.png','sha256':'ab'*32,'bytes':1}, {'path':'res://character/a.png','sha256':'cd'*32,'bytes':1}, {'path':'res://assets/other.png','sha256':'ef'*32,'bytes':1}]
 def test_compact_sorted_and_exact(self):
  d=m.encode_crew_source_keys(self.rows())
  self.assertEqual(d.get('schema'),1,'Generate the compact source key table')
  expected=sorted((hashlib.sha256(x['path'].encode()).digest(),bytes.fromhex(x['sha256'])) for x in self.rows()[:2])
  keys=b''.join(x[0] for x in expected);values=b''.join(x[1] for x in expected)
  self.assertEqual(d['count'],2);self.assertEqual(d['path_keys'],keys.hex());self.assertEqual(d['source_keys'],values.hex())
  self.assertEqual(d['checksum'],hashlib.sha256(keys+values).hexdigest())
  self.assertNotIn('res://',json.dumps(d))
 def test_deterministic_input_order(self):
  self.assertEqual(m.encode_crew_source_keys(self.rows()),m.encode_crew_source_keys(list(reversed(self.rows()))))
 def test_invalid_and_duplicate_sources_rejected(self):
  with self.assertRaises(ValueError):m.encode_crew_source_keys([{'path':'res://character/a.png','sha256':'bad'}])
  with self.assertRaises(ValueError):m.encode_crew_source_keys(self.rows()+[self.rows()[0]])
 def test_generation_refreshes_manifest_record_from_new_source(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);target=root/'assets/tablet-crew-source-keys.json';target.parent.mkdir();target.write_text('{}')
   rows=self.rows()+[{'path':'res://assets/tablet-crew-source-keys.json','sha256':'stale','bytes':2}]
   m.refresh_crew_source_keys(rows,root)
   self.assertEqual(json.loads(target.read_text()),m.encode_crew_source_keys(rows))
   self.assertEqual(rows[-1]['sha256'],hashlib.sha256(target.read_bytes()).hexdigest())
   self.assertEqual(rows[-1]['bytes'],target.stat().st_size)
   prior=target.read_bytes();rows[0]['sha256']='12'*32;m.refresh_crew_source_keys(rows,root)
   self.assertNotEqual(prior,target.read_bytes())
 def test_unselected_index_does_not_create_new_files(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);m.refresh_crew_source_keys(self.rows(),root);self.assertEqual(list(root.iterdir()),[])
 def test_main_regenerates_before_final_manifest_hash(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder)
   files={'project.godot':'run/main_scene="res://scenes/title_screen.tscn"',
    'scenes/title_screen.tscn':'path="res://scripts/player.gd"',
    'scripts/player.gd':'const INDEX="res://assets/tablet-crew-source-keys.json"\nconst PNG="res://character/a.png"',
    'assets/tablet-crew-source-keys.json':'{}', 'character/a.png':'first',
    'addons/brine_raw_export/plugin.gd':'# exporter',
    'export_presets.cfg':'[preset.0]\nname="iPad QA"\nexport_filter="all_resources"\n',
    'SOURCE_PROVENANCE.json':json.dumps({'build':{'git_commit':'fixture'}})}
   for name,body in files.items():
    path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)
   prior=(m.ROOT,m.MANIFEST,sys.argv,m.collect)
   original_collect=m.collect
   try:
    m.ROOT=root;m.MANIFEST=root/'assets/runtime-release.json';m.collect=lambda:original_collect(root);sys.argv=['build_release_manifest.py','--preset','iPad QA']
    with contextlib.redirect_stdout(io.StringIO()):m.main()
    first=json.loads(m.MANIFEST.read_text());(root/'character/a.png').write_text('changed')
    with contextlib.redirect_stdout(io.StringIO()):m.main()
    final=json.loads(m.MANIFEST.read_text());self.assertNotEqual(first['source_sha256'],final['source_sha256'])
    target=root/'assets/tablet-crew-source-keys.json';record=next(x for x in final['files'] if x['path']=='res://assets/tablet-crew-source-keys.json')
    self.assertEqual(record['sha256'],hashlib.sha256(target.read_bytes()).hexdigest())
    self.assertEqual(json.loads(target.read_text()),m.encode_crew_source_keys(final['files']))
   finally:m.ROOT,m.MANIFEST,sys.argv,m.collect=prior
if __name__=='__main__':unittest.main()
