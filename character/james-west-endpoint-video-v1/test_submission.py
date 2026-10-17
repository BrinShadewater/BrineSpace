from pathlib import Path
import importlib.util,json,tempfile,unittest
from types import SimpleNamespace
from unittest.mock import patch
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1]
spec=importlib.util.spec_from_file_location('minimax_video',r/'tools/minimax_video.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Submission(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        for name in ['first','last']:Image.new('RGB',(512,512),'white').save(self.root/(name+'.png'))
        self.prompt=self.root/'prompt.txt';self.prompt.write_text('Small planted settle.')
        self.args=SimpleNamespace(image=self.root/'first.png',last_image=None,prompt_file=self.prompt,output=self.root/'job')
    def tearDown(self):self.tmp.cleanup()
    def run_submit(self):
        with patch.object(m,'api',return_value={'task_id':'offline'}) as api,patch('builtins.print'):
            m.submit(self.args)
        return api.call_args.args[1],json.loads((self.args.output/'generation.json').read_bytes())
    def test_default_unchanged(self):
        payload,ledger=self.run_submit();self.assertEqual(payload['model'],'MiniMax-Hailuo-2.3-Fast')
        self.assertNotIn('last_frame_image',payload);self.assertEqual(ledger['estimatedUSD'],.19)
    def test_exact_end_mode(self):
        self.args.last_image=self.root/'last.png';payload,ledger=self.run_submit()
        self.assertEqual(payload['model'],'MiniMax-Hailuo-02');self.assertEqual(ledger['estimatedUSD'],.28)
        self.assertTrue(payload['last_frame_image'].startswith('data:image/png;base64,'))
        self.assertEqual(payload['duration'],6);self.assertEqual(payload['resolution'],'768P')
        self.assertFalse(payload['prompt_optimizer']);self.assertIn('lastImageSha256',ledger)
        self.assertNotIn('last_frame_image',ledger['params'])
        self.assertNotIn('first_frame_image',ledger['params'])
    def test_bad_end_dimensions_no_post(self):
        Image.new('RGB',(600,512)).save(self.root/'last.png');self.args.last_image=self.root/'last.png'
        with patch.object(m,'api') as api,self.assertRaises(RuntimeError):m.submit(self.args)
        api.assert_not_called();self.assertFalse(self.args.output.exists())
    def test_duplicate_no_post(self):
        self.run_submit()
        with patch.object(m,'api') as api,self.assertRaises(FileExistsError):m.submit(self.args)
        api.assert_not_called()
    def test_ambiguous_failure_stays_exclusive(self):
        with patch.object(m,'api',side_effect=RuntimeError('Ambiguous')) as api,self.assertRaises(RuntimeError):m.submit(self.args)
        self.assertEqual(api.call_count,1)
        self.assertEqual(json.loads((self.args.output/'generation.json').read_bytes())['status'],'submission_error')
        with patch.object(m,'api') as api,self.assertRaises(FileExistsError):m.submit(self.args)
        api.assert_not_called()
    def test_secret_redacted(self):
        response=SimpleNamespace(status_code=400,json=lambda:{'base_resp':{'status_code':1,'status_msg':'secret-test-key'}})
        with patch.dict(m.os.environ,{'MINIMAX_API_KEY':'secret-test-key'}),patch.object(m.requests,'request',return_value=response):
            with self.assertRaises(RuntimeError) as e:m.api('video_generation',{})
        self.assertNotIn('secret-test-key',str(e.exception));self.assertIn('[REDACTED]',str(e.exception))

if __name__=='__main__':unittest.main()
