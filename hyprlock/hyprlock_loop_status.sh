CURRENT=$(playerctl loop)

case $CURRENT in

	None)
		echo '<span color="#888888"> </span>'
		;;

	Playlist)
		echo '<span color="#C07B67"> </span>'
		;;

	Track)
		echo '<span color="#C07B67">₁ </span>'
		;;
esac
