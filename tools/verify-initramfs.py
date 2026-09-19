#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
"""Compare every primary/extra initramfs module against a coherent rootfs staging."""
import argparse
import gzip
import hashlib
import lzma
from pathlib import Path, PurePosixPath


def newc(data):
    offset = 0
    while offset + 110 <= len(data):
        header = data[offset:offset + 110]
        if header[:6] not in (b'070701', b'070702'):
            raise ValueError(f'Invalid newc header at {offset}')
        fields = [int(header[i:i + 8], 16) for i in range(6, 110, 8)]
        size, namesize = fields[6], fields[11]
        if namesize < 1:
            raise ValueError('Empty cpio name')
        start = offset + 110
        name = data[start:start + namesize - 1].decode()
        start = (start + namesize + 3) & ~3
        if start + size > len(data):
            raise ValueError('Truncated cpio entry')
        if name == 'TRAILER!!!':
            return
        yield name, data[start:start + size]
        offset = (start + size + 3) & ~3
    raise ValueError('Missing cpio trailer')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rootfs', type=Path, required=True)
    p.add_argument('--release', required=True)
    p.add_argument('archives', type=Path, nargs='+')
    a = p.parse_args()
    root = a.rootfs.resolve(strict=True)
    for archive in a.archives:
        data = archive.read_bytes()
        if data.startswith(b'\x1f\x8b'):
            data = gzip.decompress(data)
        elif not data.startswith((b'070701', b'070702')):
            data = lzma.decompress(data)
        count = 0
        for name, contents in newc(data):
            rel = PurePosixPath(name.removeprefix('./'))
            if rel.is_absolute() or '..' in rel.parts:
                raise ValueError(f'Unsafe archive path: {name}')
            if not any(name.endswith(s) for s in ('.ko', '.ko.zst', '.ko.xz', '.ko.gz')):
                continue
            if a.release not in rel.parts:
                raise ValueError(f'Wrong kernel release: {name}')
            parts = rel.parts
            if parts[:1] == ('lib',):
                rel = PurePosixPath('usr', *parts)
            target = (root / rel).resolve(strict=True)
            if not target.is_relative_to(root):
                raise ValueError('Module resolves outside staging')
            if hashlib.sha256(contents).digest() != hashlib.sha256(target.read_bytes()).digest():
                raise ValueError(f'Module mismatch: {name}')
            count += 1
        if not count:
            raise ValueError(f'No modules found: {archive}')
        print(f'{archive.name}: {count} modules match the staged kernel build')


if __name__ == '__main__':
    main()
