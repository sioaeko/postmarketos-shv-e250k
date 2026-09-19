# Kernel build

This is an experimental port, not an upstream pmaports submission. The shipped APK is the exact package installed during device validation. Recompiling creates a new build; byte-for-byte reproducibility is not claimed.

## Inputs

- Upstream `linux-7.2.6.tar.xz`: <https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-7.2.6.tar.xz>
- SHA-256: `039aef84f2b0994aeda3f4fcfc3d02ec9d7a9bbb9020ea264c43f446c860f606`
- Apply every `kernel/patches/*.patch` in filename order, then copy `kernel/config/note2.config` to `.config`.
- Alternatively extract the release asset `linux-7.2.6-note2-panel1-source.tar.gz`. It already contains those changes, `.config`, build/package scripts and these instructions. Do not apply the patches twice.

The release build used Alpine's pmbootstrap native chroot, pmbootstrap 3.11.1, clang/LLVM 23.1.1, `ARCH=arm LLVM=1`, ccache, 4 GiB RAM, 6 GiB swap and four jobs. Build in Linux, in a fresh source directory **outside this Git checkout** (the config enables automatic local versions). A Windows host can use a Linux VM. Do not compile on the phone.

Required tools include GNU make, clang, lld, LLVM binutils, a host C toolchain, flex, bison, bc, perl, Python 3, OpenSSL and libelf development files, pahole/dwarves, zstd, kmod/depmod, patch, tar, xz and coreutils. Alpine package names and LLVM availability vary with the repository snapshot. The original native chroot remains the reference environment.

```sh
# Run from the repository. Choose fresh directories outside the checkout.
repo=$(pwd)
work=$(mktemp -d)
tar -xJf /path/to/linux-7.2.6.tar.xz -C "$work"
for patch_file in "$repo"/kernel/patches/*.patch; do
    (cd "$work/linux-7.2.6" && patch -p1 < "$patch_file") || exit 1
done
cp kernel/config/note2.config "$work/linux-7.2.6/.config"
JOBS=4 CC='ccache clang' sh tools/build-kernel.sh \
    "$work/linux-7.2.6" "$work/staging"
```

The build script uses the same kernel targets and staging layout as the validated build. It does not install on a phone or change BOOT. `boot/vmlinuz`, DTB, `System.map`, config and all modules must come from this one build. The release build contains 598 modules.

## APK packaging

Use Alpine apk-tools v3 (`apk mkpkg`). Sign with **your own private key**, generated with Alpine's `abuild-keygen`; the repository contains only the public key for the published binary. Set a new package revision. The staging tree should have root-owned files and directory mode 0755, as in the original root-run packaging step.

```sh
python3 tools/package-kernel.py "$work/staging" ./kernel-local.apk \
    --sign-key /path/to/your-private.rsa --version 7.2.6-r2
apk --keys-dir /path/to/your-public-key-directory verify ./kernel-local.apk
```

The recorded r1 package was constructed from verified staging without another compilation. Its metadata, SHA-256 and public-key fingerprint are in `kernel/manifest.json`.

## Initramfs and BOOT

Keep primary initramfs, extra initramfs, rootfs modules and kernel together. Matching `uname -r` or vermagic **does not prove** compatibility: rebuilding can change module BTF identifiers and produce load failures when old modules are mixed in.

Generate initramfs inside a prepared postmarketOS target rootfs with the new module set and correct device package. See [INSTALL.md](INSTALL.md) for the remaining per-installation requirements. After generating both archives:

```sh
python3 tools/verify-initramfs.py --rootfs /path/to/coherent-staging \
    --release 7.2.6-postmarketos-exynos4-panel1 \
    /path/to/initramfs /path/to/initramfs-extra
```

The tool compares compressed module bytes against staging, catches wrong release paths, and requires at least one module in each supplied archive. It does not validate every other initramfs file or partition layout.

`note2-boot-fit` is a boot-deploy postprocess helper: it recompresses a generated legacy Android v0 ramdisk as XZ/CRC32 and rejects a BOOT image larger than 8 MiB. It preserves boot-deploy's kernel, DTB and command line; it never flashes. Run it in a staging boot directory with backups, since it replaces both `boot.img` and the ramdisk file.

For already validated archives, the standalone packer uses the recipient's own UUIDs:

```sh
python3 tools/mkboot-note2.py \
    --kernel /path/to/staging/boot/vmlinuz \
    --dtb /path/to/staging/boot/dtbs/exynos4412-n7105-s6evr02.dtb \
    --system-map /path/to/staging/boot/System.map \
    --initramfs /path/to/initramfs.xz \
    --boot-uuid "$YOUR_BOOT_FILESYSTEM_UUID" \
    --root-uuid "$YOUR_ROOT_FILESYSTEM_UUID" \
    --pad-to-partition --output ./boot-local.img
```

BOOT is exactly 8,388,608 bytes on the tested device. Header base is `0x40000000`, kernel offset `0x8000`, ramdisk offset `0x01000000`, tags offset `0x100`, page size 2048. The observed S-Boot loader places initrd at `0x42000000`; the packer checks the supplied `System.map` against that boundary. These checks do not establish compatibility with a different bootloader or model.
