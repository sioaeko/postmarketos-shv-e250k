#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
"""Package a coherent build staging directory using Alpine apk-tools v3."""
import argparse
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('stage', type=Path)
p.add_argument('output', type=Path)
p.add_argument('--sign-key', required=True, type=Path)
p.add_argument('--version', required=True, help='Use your own revision, e.g. 7.2.6-r2')
a = p.parse_args()
if a.output.exists():
    p.error('Output already exists')
stage = a.stage.resolve(strict=True)
release = (stage / 'usr/share/kernel/postmarketos-exynos4/kernel.release').read_text().strip()
for path in ('boot/vmlinuz', 'boot/config', 'boot/System.map',
             'boot/dtbs/exynos4412-n7105-s6evr02.dtb'):
    if not (stage / path).is_file():
        p.error(f'Missing {path}')
if not any((stage / 'usr/lib/modules' / release).rglob('*.ko*')):
    p.error('Missing modules')
if any(path.is_symlink() for path in stage.rglob('*')):
    p.error('Staging contains symlinks; inspect it before packaging')
metadata = {
    'name': 'linux-postmarketos-exynos4', 'version': a.version, 'arch': 'armv7',
    'origin': 'linux-postmarketos-exynos4', 'license': 'GPL-2.0-only',
    'description': 'Experimental Linux kernel for KT Note2 SHV-E250K (S6EVR02)',
    'url': 'https://github.com/sioaeko/postmarketos-shv-e250k',
    'maintainer': 'Local builder', 'build-time': str(int(time.time())),
}
cmd = ['apk', 'mkpkg', '--files', str(stage), '--output', str(a.output),
       '--compat', '3.0.0', '--sign-key', str(a.sign_key)]
for key, value in metadata.items():
    cmd += ['--info', f'{key}:{value}']
subprocess.run(cmd, check=True)
