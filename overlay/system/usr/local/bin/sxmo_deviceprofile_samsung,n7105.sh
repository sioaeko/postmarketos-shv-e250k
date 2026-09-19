#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-only
# KT Galaxy Note2 SHV-E250K with the n7105 mainline device tree.
# Verified from input capabilities: gpio-keys carries KEY_POWER and volume.
export SXMO_POWER_BUTTON="1:1:gpio-keys"
export SXMO_VOLUME_BUTTON="1:1:gpio-keys"
export SXMO_SWAY_SCALE="2"
export SXMO_LISGD_INPUT_DEVICE="/dev/input/by-path/platform-13890000.i2c-event"
# This installation is used primarily through Wi-Fi SSH; no working modem.
export SXMO_NO_MODEM="1"
