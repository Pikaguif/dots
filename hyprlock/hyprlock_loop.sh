CURRENT=$(playerctl loop)

if [ $CURRENT = "None" ]; then
	playerctl loop Playlist
elif [ $CURRENT = "Playlist" ]; then
	playerctl loop Track
else
	playerctl loop None
fi
