"""Inspect an exported Mac ZIP without claiming native execution acceptance."""
import argparse
import json
import plistlib
import struct
import zipfile


def inspect(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        plists = [name for name in names if name.endswith('.app/Contents/Info.plist')]
        if len(plists) != 1:
            raise ValueError('Expected exactly one app Info.plist')
        prefix = plists[0].removesuffix('Info.plist')
        info = plistlib.loads(archive.read(plists[0]))
        executable = prefix + 'MacOS/' + info['CFBundleExecutable']
        with archive.open(executable) as stream:
            header = stream.read(4096)
        magic, count = struct.unpack_from('>II', header)
        if magic != 0xCAFEBABE or count != 2:
            raise ValueError('Expected a Universal 2 Mach-O executable')
        architectures = [struct.unpack_from('>I', header, 8 + i * 20)[0] for i in range(count)]
        if set(architectures) != {0x01000007, 0x0100000C}:
            raise ValueError(f'Expected x86_64 and arm64, found {architectures}')
        mode = archive.getinfo(executable).external_attr >> 16
        if not mode & 0o111:
            raise ValueError('Executable permission missing from ZIP')
        packs = [name for name in names if name.startswith(prefix) and name.endswith('.pck')]
        if len(packs) != 1:
            raise ValueError('Expected exactly one runtime PCK')
        if any(name.endswith('/override.cfg') for name in names):
            raise ValueError('QA override must not ship')
        return {'bundle_identifier': info['CFBundleIdentifier'], 'executable': executable,
                'architectures': ['x86_64', 'arm64'], 'executable_mode': oct(mode),
                'pack': packs[0], 'pack_bytes': archive.getinfo(packs[0]).file_size,
                'native_runtime_verified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('zip')
    args = parser.parse_args()
    print(json.dumps(inspect(args.zip), indent=2))
