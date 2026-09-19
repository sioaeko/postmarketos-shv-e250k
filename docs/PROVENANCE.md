# Sources and licensing

## Kernel

- Linux 7.2.6, upstream tarball from kernel.org. Exact hash in `kernel/manifest.json`.
- Exynos4 downstream base: <https://gitlab.com/exynos4-mainline/linux>, ref `v7.1.1-exynos4`, commit `3b51b9a62678973804c61ad66fffa10eba7d0fd8`.
- `0001-exynos4-note2-port.patch` is a combined source diff against pristine Linux 7.2.6, including Exynos4 support and the local Note2 changes. It is not an upstream commit series. Existing author/copyright notices remain in the source.
- `0002-s6evr02-restore-gamma-before-display-on.patch` restores cached panel brightness/gamma before DISPLAY_ON.
- `0003-remove-obsolete-n710x-dts.patch` records deletion of the upstream single-panel-era DTS, which the split variant DTS files replace. This deletion was present in the working build tree but omitted from the original combined diff; the publication comparison caught it. It does not add a new hardware change.
- The release provides a clean, fully patched corresponding-source archive, exact `.config` and the scripts used to describe the build and packaging procedure. No compiler outputs or personal build directory are included in that source archive.

Linux uses GPL-2.0 with the Linux syscall exception and per-file licenses. Preserve `COPYING` and the complete `LICENSES/` directory in the full source. Reference copies are in this repository's `licenses/`. Kernel patches/config remain subject to those upstream terms, rather than the repository's default license.

## Device and user environment

The postmarketOS pmaports revision used was `3b498d535550325163969b7f41695219983ae5de`, path `device/archived/device-samsung-t0lte`. Device package version 6-r0; selected panel subpackage `device-samsung-t0lte-kernel-s6evr02`. The package declares MIT. `device/deviceinfo.upstream` is a reference copy of its deviceinfo, not an independent supported-device package. See <https://gitlab.postmarketos.org/postmarketOS/pmaports>.

Sxmo upstream hook scripts are AGPL-3.0-only, copyright Sxmo Contributors. Our hook wrappers call the installed default scripts and retain their configversion markers. The project's non-kernel scripts, runtime configs and documentation are distributed under AGPL-3.0-only; see [LICENSE](../LICENSE). Upstream code and assets retain their own licenses. We do not claim authorship of Linux, Exynos4 mainline, postmarketOS, Sxmo, firmware or browser projects.

Firmware dependencies are obtained from their original packages. No extracted vendor firmware, device NVRAM, EFS data, private key, login credential, browser profile, personal wallpaper or personal disk image is included.
