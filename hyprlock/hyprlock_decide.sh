#! /usr/bin/bash

PLAYERCTL=$(playerctl -a metadata)

if [ "$PLAYERCTL" = "" ]; then
	echo "Test"
	(hyprlock --config "/home/Pikaguif/.config/hypr/hyprlock_no_mm.conf")&
else
	(hyprlock --config "/home/Pikaguif/.config/hypr/hyprlock.conf")&
fi

sleep 0.8
killall --signal USR2 hyprlock
