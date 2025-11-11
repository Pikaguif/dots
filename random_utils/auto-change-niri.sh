#!/usr/bin/bash

CURRENT_WORKSPACE="-1"
SWWW_COMMAND="swww img --transition-step 5 --transition-fps 60"

while sleep 0.3s; do
	WORKSPACE=$(niri msg workspaces | grep "*" | awk '{print $2}');

	echo $WORKSPACE
	echo "$SWWW_COMMAND ~/Documents/swww-wallpapers/wall$WORKSPACE-1.avif"
	
	if [[ $CURRENT_WORKSPACE != $WORKSPACE ]]; then  
		$SWWW_COMMAND ~/Documents/swww-wallpapers/wall$WORKSPACE-1.gif;
		export CURRENT_WORKSPACE=$WORKSPACE;
	fi
	echo $CURRENT_WORKSPACE
done

