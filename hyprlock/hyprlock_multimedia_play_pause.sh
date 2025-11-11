#! /usr/bin/bash

VALUE=$(playerctl status)

if [ $VALUE = Playing ]; then
	echo ⏸
elif [ $VALUE = Paused ]; then
	echo ⏵
else
	echo X
fi
