"""Runner launch boundary checks; a fake engine never accesses player data."""
from pathlib import Path
import contextlib,io,os,sys,tempfile,unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import run_tests as runner

class Isolation(unittest.TestCase):
    def fixture(self,folder):
        root=Path(folder);(root/'tests').mkdir();(root/'tests/test_probe.gd').write_text('extends SceneTree\n')
        return root
    def run_fake(self,root,seen):
        def fake(cmd,log,timeout,**kwargs):
            seen.append(kwargs['env']);return 0,'PASS',False,False
        with patch.object(runner,'ROOT',root),patch.object(runner,'run_process',fake),contextlib.redirect_stdout(io.StringIO()):
            return runner.run(['--only','test_probe','--godot','never-launched'])
    @unittest.skipUnless(sys.platform=='win32','Windows APPDATA contract')
    def test_default_never_launches_against_real_profile(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.fixture(folder);seen=[]
            real=Path.home()/'AppData/Roaming'
            with patch.dict(os.environ,{'APPDATA':str(real)}):self.assertEqual(self.run_fake(root,seen),0)
            self.assertEqual(len(seen),1)
            self.assertNotEqual(Path(seen[0]['APPDATA']).resolve(),real.resolve())
            self.assertEqual(seen[0]['BRINESPACE_TEST_USER_DIR'],(Path(seen[0]['APPDATA'])/'Godot/app_userdata/BrineSpace').as_posix())
    @unittest.skipUnless(sys.platform=='win32','Windows APPDATA contract')
    def test_explicit_fixture_cannot_redirect_to_real_profile(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.fixture(folder);seen=[]
            with patch.object(runner,'own_scratch',return_value=Path.home()/'AppData/Roaming'):
                with self.assertRaises(ValueError):self.run_fake(root,seen)
            self.assertEqual(seen,[])
    def test_darwin_launch_uses_scratch_home(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.fixture(folder);seen=[]
            with patch.object(sys,'platform','darwin'):self.assertEqual(self.run_fake(root,seen),0)
            chosen=Path(seen[0]['HOME'])
            self.assertNotEqual(chosen,Path.home())
            self.assertEqual(seen[0]['BRINESPACE_TEST_USER_DIR'],(chosen/'Library/Application Support/Godot/app_userdata/BrineSpace').as_posix())
    def test_linux_launch_uses_scratch_xdg(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.fixture(folder);seen=[]
            with patch.object(sys,'platform','linux'):self.assertEqual(self.run_fake(root,seen),0)
            chosen=Path(seen[0]['XDG_DATA_HOME'])
            self.assertEqual(seen[0]['BRINESPACE_TEST_USER_DIR'],(chosen/'Godot/app_userdata/BrineSpace').as_posix())

if __name__=='__main__':unittest.main()
