# Applying the developer release

**This release does not provide a tested first-install procedure from Android.** It publishes the running kernel and the changes used on an existing internal-storage postmarketOS installation. Do not flash the APK or the source archive with TWRP. A distributable clean rootfs and end-to-end installation image still need to be built and tested on a separate device.

## Before changing an existing installation

Confirm the actual hardware is **KT SHV-E250K, S6EVR02 panel**. The validated phone used bootloader `E250KKTUKOH4`. Its TWRP identified itself as GT-N7100/t03g; that label was not the hardware variant. Determine partition names and filesystem UUIDs from the recipient device, never from someone else's backup.

Keep a tested recovery path and backups of BOOT, the boot filesystem and the matching rootfs/module set. Keep EFS/radio and personal backups private. This project does not replace or repartition RECOVERY, EFS or modem partitions. The tested TWRP version was 3.7.0_9-0. It could mount this newer ext4 rootfs only read-only with `noload`, because its old kernel did not understand an ext4 feature. Do not remove ext4 features just to make recovery write it.

## Verify the download

Download the APK, corresponding source, `SHA256SUMS` and repository overlay from the **same release tag**. Check SHA-256 before use. The release binary is signed with the included public key:

The binary uses the apk-tools v3 package format; package verification and a fresh offline `apk add --no-scripts` were checked with apk-tools 3.0.8. Older apk-tools v2 installations need a compatible packaging environment. `apk extract` 3.0.8 into a completely empty directory did not create intermediate directories in our check; use normal package installation in an offline target instead.

```sh
sha256sum -c SHA256SUMS
apk --keys-dir ./keys verify ./linux-postmarketos-exynos4-7.2.6-r1.apk
```

The public-key SHA-256 is `0e0c96a19d2611a44ed924f7adca7b36840c2f9a63416162595ff60392c55180`. Adding a key to `/etc/apk/keys` grants package trust; inspect the source and decide whether to trust it. Never put a private signing key or an SSH private key into the rootfs overlay.

## Assemble a target rootfs offline

Use a prepared postmarketOS armv7 rootfs with the matching archived `device-samsung-t0lte` 6-r0 / S6EVR02 subpackage, Sxmo/Sway and its dependencies. [PROVENANCE.md](PROVENANCE.md) pins the pmaports revision. That device package is archived/unmaintained and is not automatically available from every current repository snapshot.

The device package refers to `firmware-samsung-midas-wifi` and Bluetooth/media firmware. Obtain firmware through the appropriate postmarketOS packages and their licensing terms; this release does not redistribute extracted firmware, Wi-Fi credentials or device NVRAM. The tested installation had functioning firmware already. Fresh-device firmware provisioning is not established by this release.

Install or stage the APK inside that target using its normal package tools. Kernel package hooks can regenerate initramfs and invoke boot-deploy; control those hooks in the **offline target** and inspect the result before any flash. Do not run an unreviewed live kernel update over SSH. Preserve rollback copies of the previous matching modules and boot files.

Merge `overlay/system/` into the target filesystem, preserving executable modes. Review each file first. Additional integration points are deliberately documented instead of replacing the target's global config:

```sh
# Append/merge into /etc/deviceinfo; keep the base device package settings.
deviceinfo_flash_kernel_on_update="false"
deviceinfo_mkinitfs_postprocess="/usr/local/libexec/note2-boot-fit"

# Merge into /etc/conf.d/greetd, preserving the existing cfgfile.
rc_need="note2-display"
```

Enable `sshd`, `note2-display` and the chosen graphical login service in the target's OpenRC default runlevel. `note2-display` requires SSH first and delays explicit `exynosdrm` loading until uptime 60 seconds. Do not enable the old `note2-backlight` guard alongside it. Keep `drm_client_lib.active=` empty and the `exynosdrm` blacklist in early boot as supplied by the kernel config and modprobe overlay.

Initialize an ordinary user through postmarketOS, add the appropriate `input`/`video` permissions for the distro, and start Sxmo once so its normal profile/config exist. Back up `~/.config/sxmo`, then merge `overlay/user/` into that user's home. Add:

```sh
# ~/.config/sxmo/profile
. "$HOME/.config/sxmo/note2-idle.conf"
"$HOME/.local/bin/note2-keylights" on
```

```text
# ~/.config/sxmo/sway
include ~/.config/sxmo/note2-keys.conf
include ~/.config/sxmo/note2-spen.conf
```

Choose **Sxmo (Note2)** in the login session selector. Its wrapper disables automatic suspend to keep SSH reachable. Configure your own account, SSH authorized key and Wi-Fi locally. There is no distributed password, authorized key, fixed private IP or wallpaper. The S Pen calibration is device-specific; test its alignment on your panel.

Regenerate primary and extra initramfs from this target with the coherent kernel module set. Check their module content with `tools/verify-initramfs.py`, then validate the boot image size, addresses, filesystem UUIDs and recovery path. See [BUILD.md](BUILD.md). A freshly generated initramfs may differ in size and required files; the old personalized archives are not supplied as a shortcut.

## Flash and recovery boundary

This repository intentionally has no automatic raw-partition flasher. The validated installation updated the prepared matching boot/root files and wrote **BOOT only**, then read BOOT back and verified its hash. Repeat that only after independently confirming the recipient partition map and prepared image. A file named `boot-local.img` alone is not evidence that it is safe for a device.

If the new kernel does not boot, restore the prior BOOT **and matching boot filesystem/initramfs/modules** using recovery or the known-good installation. Do not restore just one archive from a different build. Expect the 60-second display delay; if SSH comes up, inspect `/var/log/note2-display.log`, the current kernel release and module-load errors before making further changes.

Full clean-install automation and another-device validation are follow-up work, not completed features of v0.1.0.
