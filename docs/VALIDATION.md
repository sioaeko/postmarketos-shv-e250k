# Validation boundary

Validated on one physical **KT SHV-E250K, S6EVR02**, September 2026. The initial release records the working device; it does not claim a successful fresh install on another phone.

## Kernel and display

- Running release `7.2.6-postmarketos-exynos4-panel1`, build `#2-postmarketOS`, compiler clang 23.1.1.
- Installed APK and its staged kernel/DTB/config verified by SHA-256.
- 598 rootfs modules; primary and extra initramfs modules checked against the exact corresponding build (23 and 9 modules respectively).
- BOOT read-back matched the prepared image, with 180,224 bytes unused in the 8 MiB partition. That personalized image is not distributed.
- S6EVR02 brightness is restored before display-on. The owner confirmed normal colors and brightness on the running phone. The delayed DRM initialization workaround remains necessary in this setup.
- This work retained the previous kernel/module sets and did not change RECOVERY.

## Input and session

- Touchscreen and Wacom S Pen are enabled simultaneously in the unlocked Sway session. Five-point pen calibration was physically checked by the owner (sample RMS error 3.14 px, maximum 4.73 px on a 720×1280 panel).
- Menu/home/back bindings and key illumination were checked on-device.
- Original 120-second idle → touch-disabled lock was identified from the live Sxmo state, input flags and stock hooks.
- The release sets 600-second local idle and skips that intermediate state. A live screenoff → single-power-action → unlock transition restored both touchscreen and pen input; the active swayidle command was verified at 600 seconds. Software action invocation verifies the handler, not a robot pressing the physical key.
- SSH remains reachable while the screen is off; suspend is disabled deliberately, with a battery-life cost.

## Applications

- Chromium opened Example Domain with GPU/shader-disk-cache disabled, while retaining its sandbox.
- Firefox ESR with mobile-config-firefox displayed its mobile UI and `about:mobile` settings. Existing profile/bookmark files were preserved.

## Publication checks

`kernel/source-verification.json` records a clean source comparison against the build tree. Additional publication checks cover shell/Python syntax, boot-image packing against a local reference, module comparisons and package signature verification. New build wrappers are provided for reproduction; the shipped kernel was not recompiled during publication, and the working phone was not wiped or reflashed to test the public instructions.

The source comparison covered 94,793 regular files with zero mismatches. A fresh isolated `apk add --no-scripts` with the public verification key installed all 617 payload files byte-identically to staging. The standalone BOOT packer reproduced the local verified image byte-for-byte, rejected malformed inputs/oversize images, and passed a CLI run with synthetic UUIDs. The boot-deploy recompression helper preserved the verified kernel/header/ramdisk. The live idle log also recorded the automatic screenoff transition exactly 600 seconds after timer setup.

Unknowns: another unit, alternate panels/variants, full clean install, telephony, camera, audio, Bluetooth, accelerated video, complete suspend/resume and long-duration reliability. Please report the exact model, panel, kernel release and redacted logs with a reproducible issue. Do not attach EFS, private keys or an unredacted disk image.
