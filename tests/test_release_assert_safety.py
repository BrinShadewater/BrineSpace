from pathlib import Path
import re, subprocess, unittest
ROOT = Path(__file__).resolve().parents[1]
def unsafe_asserts(source):
    # Strip literals/comments while retaining newlines for actionable locations.
    clean = re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|#[^\n]*', lambda m: '\n' * m[0].count('\n'), source)
    found = []
    for match in re.finditer(r'\bassert\s*\(', clean):
        depth, end = 1, match.end()
        while end < len(clean) and depth:
            depth += (clean[end] == '(') - (clean[end] == ')')
            end += 1
        if re.search(r'\b(?:load\w*)\s*\(', clean[match.end():end]):
            found.append(clean.count('\n', 0, match.start()) + 1)
    return found
class ReleaseSafety(unittest.TestCase):
    def test_detects_multiline_side_effects(self):
        self.assertEqual(unsafe_asserts('assert(\n image.load_png_from_buffer(bytes) == OK\n)'), [1])
        self.assertEqual(unsafe_asserts('# assert(image.load(x))\nassert(ok, "load(x)")'), [])
    def test_runtime_asserts_have_no_loading(self):
        names = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '*.gd'], cwd=ROOT, text=True).splitlines()
        bad = []
        for name in set(names):
            if name.startswith(('tests/', 'tools/')):
                continue
            path = ROOT / name
            if path.is_file():
                bad.extend(f'{name}:{line}' for line in unsafe_asserts(path.read_text(encoding='utf-8-sig')))
        self.assertEqual(bad, [], 'Side effects stripped from release asserts: ' + ', '.join(bad))
if __name__ == '__main__':
    unittest.main()
