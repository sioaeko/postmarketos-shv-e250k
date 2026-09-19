# Everyday settings

[English](USAGE.md) · [한국어](USAGE.ko.md)

## Display and input

Edit `SXMO_UNLOCK_IDLE_TIME=600` in `~/.config/sxmo/note2-idle.conf` to change the idle timeout in seconds. 600 means ten minutes. SSH traffic does not count as local Wayland input.

Stock Sxmo can enter a `lock` stage after 120 seconds, leaving the display on but disabling touch. This overlay sets `SXMO_STATES="unlock screenoff"` to skip that intermediate stage. One power-button action wakes the display and restores both touch and pen. This is not a PIN/password lock. `SXMO_LOCK_IDLE_TIME` matters only if a separate lock stage is restored.

The next unlock transition reads the timeout file again; new logins also load it. Sxmo's idle toggle creates `~/.cache/sxmo/sxmo.noidle`, which disables the idle timer while present. The separate `sxmo.nosuspend` marker is created by the Note2 session to keep SSH reachable with the screen off.

## Keys and S Pen

- Menu: open or close the application menu.
- Home: show the home workspace while keeping applications running.
- Back: close an open menu/keyboard, otherwise close the current window.
- Menu/Back illumination: on with the display, off with the display.

Pen calibration lives in `~/.config/sxmo/note2-spen.conf`. It was calibrated at five points on one device; other units may need different values. Touch and pen are deliberately disabled while the display is off.

## Wallpaper and browsers

Put your image on the phone, add this to `~/.config/sxmo/profile`, then log in again:

```sh
export SXMO_BG_IMG="$HOME/Pictures/wallpaper.jpg"
```

For Firefox's mobile interface:

```sh
sudo apk add firefox-esr mobile-config-firefox
```

Restart Firefox and visit `about:mobile`. There is no need to delete the existing profile. Tested versions: Firefox ESR 140.14.0-r0 and mobile-config-firefox 5.4.1-r0. Available versions depend on the repository snapshot.

Chromium uses the two GPU flags in `overlay/system/etc/chromium/zz-note2.conf`; the tested version was 152.0.7977.82-r1. Keep its sandbox enabled. Browser performance remains limited by this older ARMv7 hardware.

## Reboot

Use `sudo reboot` over SSH (`doas reboot` on distributions configured with doas). Allow more than 60 seconds for the display to initialize. SSH is configured to start before the display.
