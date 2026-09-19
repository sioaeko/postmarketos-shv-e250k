#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-only
# configversion: 113bf453dd3310afff192d841089e5ac
. "$HOME/.config/sxmo/note2-idle.conf"
case "$1" in
    powerbutton_one|powerbutton_two|powerbutton_three)
        if sxmo_state.sh is_locked; then
            exec sxmo_state.sh set unlock
        fi
        ;;
    bottomleftcorner)
        sxmo_dmenu.sh close
        sxmo_keyboard.sh close
        exec sxmo_state.sh set screenoff
        ;;
esac
exec /usr/share/sxmo/default_hooks/sxmo_hook_inputhandler.sh "$@"
