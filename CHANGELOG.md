# Changes

## v0.1.0-experimental.1 — 2026-09-20

Initial public developer release, tested on one KT SHV-E250K (S6EVR02).

- Port Exynos4/Note2 support to Linux 7.2.6; ship the installed `panel1` build.
- Restore cached gamma/AID/ACL/ELVSS before enabling the panel.
- Keep the proven late-DRM startup workaround and BOOT size checks.
- Include touchscreen gestures, calibrated S Pen, menu/home/back bindings, key LEDs and Sway wake retries.
- Set local-input idle to 600 seconds. Skip the intermediate screen-on/touch-disabled lock state and restore touch + pen on wake.
- Include Chromium GPU flags and document Firefox mobile configuration.
- Publish complete matching kernel source, signature key, provenance and limitations. No personal rootfs, BOOT image, firmware extraction or account data is included.
- Use English documentation by default, with separate Korean README and usage translations. Include an unsubmitted draft for a scoped postmarketOS wiki update.
