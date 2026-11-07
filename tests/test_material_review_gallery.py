import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('gallery',Path(__file__).resolve().parents[1]/'tools/build_material_review_gallery.py')
gallery=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gallery)


class GalleryDiscoveryTests(unittest.TestCase):
    def record(self,root,name,export='wall.png'):
        path=root/'assets'/'pair'/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps({'asset_id':name,'export_path':'assets/pair/'+export,
                                   'export_sha256':'unchanged','review':{}}),encoding='utf-8')
        return path

    def test_multi_asset_records_and_legacy_exclusion(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            self.record(root,'wall-review.json')
            self.record(root,'dolly-review.json','dolly.png')
            (root/'assets/pair/legacy-review.json').write_text('{"assets":[]}',encoding='utf-8')
            self.assertEqual(len(gallery.discover_records(root)),2)

    def test_duplicate_export_is_not_double_counted(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            self.record(root,'material-scale-review.json')
            self.record(root,'wall-review.json')
            with self.assertRaisesRegex(ValueError,'Duplicate export'):
                gallery.discover_records(root)

    def test_findings_preserve_uncertainty(self):
        findings=gallery.review_findings({'materials':{'findings':['Owner review pending']}})
        self.assertIn('materials: unreviewed',findings)
        self.assertIn('Owner review pending',findings)

    def test_contexts_keep_rejected_host_and_limited_proposal(self):
        reviews={'materials':{},'integration':{},'host_study':{'verdict':'layout_rejected'},
                 'relocation_study':{'verdict':'agent_pass_static_layout'},'supported_group':{'verdict':None}}
        self.assertEqual([name for name,_ in gallery.contextual_reviews(reviews)],
                         ['host_study','relocation_study','supported_group'])

    def test_render_context_evidence_and_stale_warning(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); path=self.record(root,'material-scale-review.json')
            (path.parent/'wall.png').write_bytes(b'export')
            (root/'output').mkdir(); (root/'output/host.png').write_bytes(b'changed evidence')
            data=json.loads(path.read_text());data['review']={
                'host_study':{'verdict':'layout_rejected','evidence':'output/host.png','findings':['<door blocked>']},
                'relocation_study':{'verdict':'agent_pass_static_layout','findings':['Crew access unverified']}}
            data['evidence_hashes']={'output/host.png':'old'};path.write_text(json.dumps(data))
            output=root/'output/gallery.html'
            with patch.object(gallery,'ROOT',root),patch.object(gallery,'OUTPUT',output): gallery.main()
            rendered=output.read_text()
            for expected in ('host study: layout_rejected','relocation study: agent_pass_static_layout',
                             'Crew access unverified','&lt;door blocked&gt;','STALE evidence','href="host.png"'):
                self.assertIn(expected,rendered)


if __name__=='__main__':
    unittest.main()
