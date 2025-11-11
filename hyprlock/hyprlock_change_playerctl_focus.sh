#! /usr/bin/bash

# Requires playerctld to be running

CURRENT_FOCUS=$(playerctl metadata | awk '{print $1}' | sort -u)
ALL_PLAYERS=$(playerctl metadata -a | awk '{print $1}' | sort -u)

ALL_PLAYERS=($ALL_PLAYERS)

echo "Current focus: $CURRENT_FOCUS"
echo "All players alone: ${ALL_PLAYERS[@]}"

for i in ${!ALL_PLAYERS[@]}; do
	echo "INDEX: $i"
	if [ ${ALL_PLAYERS[$i]} = $CURRENT_FOCUS ]; then
		INDEX=$i
	fi
done

INDEX=$(($INDEX+1))
echo $INDEX
echo ${#ALL_PLAYERS[@]}

if [ $INDEX = ${#ALL_PLAYERS[@]} ]; then
	NEW_FOCUS=${ALL_PLAYERS[0]}
else
	NEW_FOCUS=${ALL_PLAYERS[$INDEX]}
fi
echo $NEW_FOCUS

if [ $(playerctl -s -p $NEW_FOCUS shuffle Toggle) ]; then
	echo "Command worked"
	playerctl -s -p $NEW_FOCUS shuffle Toggle
else
	echo "Command not worked"
	playerctl -s -p $NEW_FOCUS play-pause
	playerctl -s -p $NEW_FOCUS play-pause
fi

playerctl metadata | awk '{print $1}' | sort -u
