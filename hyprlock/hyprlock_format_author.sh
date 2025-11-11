AUTHOR="$(playerctl metadata xesam:artist)"
ALBUM="$(playerctl metadata xesam:album)"

IS_FIREFOX="$(playerctl metadata | grep "firefox")"

if [ "$(echo "$IS_FIREFOX")" != "" ]; then
	METADATA="$(playerctl metadata)"
	
	if [ "$(echo "$METADATA" | grep "youtube")" != "" ]; then
		ALBUM="YouTube"
	elif [ "$(echo "$METADATA" | grep "twitch")" != "" ]; then
		ALBUM="Twitch"
	else
		ALBUM="Firefox"
	fi
fi

echo $AUTHOR · $ALBUM
