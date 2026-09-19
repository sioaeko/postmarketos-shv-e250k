#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-only
# configversion: 66b67db06146e3b2dd3ae9a6f1411c5e
swaymsg -q 'input "1386:0:Wacom_T0_Note2_S_Pen" events disabled'
/usr/share/sxmo/default_hooks/sxmo_hook_screenoff.sh "$@"
"$HOME/.local/bin/note2-keylights" off
