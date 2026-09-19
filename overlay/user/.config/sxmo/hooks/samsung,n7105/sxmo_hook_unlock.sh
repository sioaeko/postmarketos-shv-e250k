#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-only
# configversion: 5697e0579ea20a4a6b8dc05f5814d0c6
. "$HOME/.config/sxmo/note2-idle.conf"
/usr/share/sxmo/default_hooks/sxmo_hook_unlock.sh "$@"
swaymsg -q 'input "1386:0:Wacom_T0_Note2_S_Pen" events enabled'
/usr/local/bin/note2-sxmo-wake
"$HOME/.local/bin/note2-keylights" on
