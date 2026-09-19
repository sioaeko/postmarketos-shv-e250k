#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
"""Create a Note2 Android v0 BOOT image with the recipient's filesystem UUIDs.

No block devices are written. Kernel, DTB and initramfs must be one coherent build.
"""
import argparse
import hashlib
import lzma
from pathlib import Path
import struct
import uuid

PAGE = 2048
LIMIT = 8 * 1024 * 1024


def align(data):
    return data + bytes((-len(data)) % PAGE)


def make_image(kernel, dtb, ramdisk, boot_uuid, root_uuid):
    if kernel[0x24:0x28] != b'\x18\x28\x6f\x01':
        raise ValueError('Not an ARM zImage')
    if len(dtb) < 40 or struct.unpack_from('>II', dtb) != (0xD00DFEED, len(dtb)):
        raise ValueError('Invalid DTB')
    if b'samsung,n7105\0' not in dtb or b'samsung,s6evr02\0' not in dtb:
        raise ValueError('Expected n7105 S6EVR02 DTB')
    unpacked = lzma.decompress(ramdisk)
    if not unpacked.startswith((b'070701', b'070702')):
        raise ValueError('Expected an LZMA/XZ compressed newc initramfs')
    kernel += dtb
    cmdline = ('quiet splash plymouth.ignore-serial-consoles plymouth.prefer-fbcon '
               f'pmos_boot_uuid={uuid.UUID(boot_uuid)} '
               f'pmos_root_uuid={uuid.UUID(root_uuid)} pmos_rootfsopts=defaults').encode()
    if len(cmdline) >= 512:
        raise ValueError('Command line exceeds legacy header limit')
    header = bytearray(PAGE)
    header[:8] = b'ANDROID!'
    struct.pack_into('<10I', header, 8, len(kernel), 0x40008000,
                     len(ramdisk), 0x41000000, 0, 0x40F00000,
                     0x40000100, PAGE, 0, 0)
    header[64:64 + len(cmdline)] = cmdline
    checksum = hashlib.sha1()
    for part in (kernel, ramdisk, b''):
        checksum.update(part)
        checksum.update(struct.pack('<I', len(part)))
    header[576:596] = checksum.digest()
    image = bytes(header) + align(kernel) + align(ramdisk)
    if len(image) > LIMIT:
        raise ValueError(f'BOOT is too large: {len(image)} > {LIMIT}')
    return image


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('kernel', 'dtb', 'initramfs', 'system-map', 'output'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--boot-uuid', required=True)
    p.add_argument('--root-uuid', required=True)
    p.add_argument('--pad-to-partition', action='store_true')
    a = p.parse_args()
    if a.output.exists():
        p.error('Output already exists')
    symbols = [line.split() for line in a.system_map.read_text().splitlines()]
    ends = [int(x[0], 16) for x in symbols if len(x) == 3 and x[2] == '_end']
    if len(ends) != 1 or not 0xC0000000 < ends[0] < 0xC2000000:
        p.error('Kernel memory end overlaps the observed S-Boot initrd at 0x42000000')
    image = make_image(a.kernel.read_bytes(), a.dtb.read_bytes(),
                       a.initramfs.read_bytes(), a.boot_uuid, a.root_uuid)
    used = len(image)
    if a.pad_to_partition:
        image += bytes(LIMIT - used)
    with a.output.open('xb') as stream:
        stream.write(image)
    print(f'BOOT used={used}/{LIMIT}, bytes={len(image)}, sha256={hashlib.sha256(image).hexdigest()}')


if __name__ == '__main__':
    main()
