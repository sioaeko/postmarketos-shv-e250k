#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-only
# configversion: 70028f54f5d7428d4e3178de5c98978b
. "$HOME/.config/sxmo/note2-idle.conf"
swaymsg -q 'input "1386:0:Wacom_T0_Note2_S_Pen" events disabled'
/usr/share/sxmo/default_hooks/sxmo_hook_lock.sh "$@"
/usr/local/bin/note2-sxmo-wake
"$HOME/.local/bin/note2-keylights" on
