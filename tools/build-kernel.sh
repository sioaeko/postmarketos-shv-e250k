#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-only
# Build in a freshly extracted corresponding-source tree; stage into a new dir.
set -eu
[ "$#" = 2 ] || { echo "Usage: $0 SOURCE_DIR NEW_STAGING_DIR" >&2; exit 2; }
src=$(realpath "$1")
stage=$(realpath -m "$2")
[ ! -e "$stage" ] || { echo 'Staging destination must not exist' >&2; exit 1; }
[ -f "$src/.config" ] && [ -f "$src/Makefile" ]
cd "$src"
make ARCH=arm LLVM=1 CC="${CC:-clang}" \
    KBUILD_BUILD_VERSION="${KBUILD_BUILD_VERSION:-2-postmarketOS}" \
    -j"${JOBS:-4}" zImage modules samsung/exynos4412-n7105-s6evr02.dtb
release=$(cat include/config/kernel.release)
[ "$release" = 7.2.6-postmarketos-exynos4-panel1 ] || {
    echo "Unexpected release $release; use a source directory outside a Git checkout" >&2
    exit 1
}
mkdir -p "$stage/boot/dtbs" "$stage/usr/share/kernel/postmarketos-exynos4"
make ARCH=arm LLVM=1 INSTALL_MOD_STRIP=1 INSTALL_MOD_PATH="$stage/usr" modules_install
# These generated links point back into the builder's workspace.
for link in build source; do
    path="$stage/usr/lib/modules/$release/$link"
    [ ! -L "$path" ] || unlink "$path"
done
depmod -b "$stage/usr" -a "$release"
cp arch/arm/boot/zImage "$stage/boot/vmlinuz"
cp arch/arm/boot/dts/samsung/exynos4412-n7105-s6evr02.dtb "$stage/boot/dtbs/"
cp .config "$stage/boot/config"
cp System.map "$stage/boot/System.map"
cp include/config/kernel.release "$stage/usr/share/kernel/postmarketos-exynos4/"
echo "Coherent kernel/module staging created at $stage; no device was changed."
