IS_FIREFOX="$(playerctl metadata | grep "firefox")"

if [ "$(echo "$IS_FIREFOX")" != "" ]; then
    echo "/home/Pikaguif/.config/hypr/img/169.png"
else
	echo "/home/Pikaguif/.config/hypr/img/11.png"
fi
