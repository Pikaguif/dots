#! /usr/bin/bash

url=$(playerctl metadata mpris:artUrl)
artist=$(playerctl metadata xesam:artist | sed 's/\//\?/g')
album=$(playerctl metadata xesam:album | sed 's/\//\?/g')

IS_FIREFOX="$(playerctl metadata | grep "firefox")"

if [ "$(echo "$IS_FIREFOX")" != "" ]; then
	album=$(playerctl metadata xesam:title | sed 's/\//\?/g')
fi

metadata=$(printf "$artist - $album")


if [ $url == "No player found" ]
then
  exit
elif [ -f /home/Pikaguif/.cache/niri_things/hyprlock/"$metadata".png ]
then
  echo /home/Pikaguif/.cache/niri_things/hyprlock/"$metadata".png
else
  curl  $url -o /home/Pikaguif/.cache/niri_things/hyprlock/"$metadata"
  ffmpeg -i /home/Pikaguif/.cache/niri_things/hyprlock/"$metadata" -vf "scale=300:-1,pad=300:300:0:(oh-ih)/2:0x00800000" -pix_fmt rgba /home/Pikaguif/.cache/niri_things/hyprlock/"$metadata".png
  rm /home/Pikaguif/.cache/niri_things/hyprlock/"$metadata"
  echo /home/Pikaguif/.cache/niri_things/hyprlock/"$metadata".png
fi
