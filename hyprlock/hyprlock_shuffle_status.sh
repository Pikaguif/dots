CURRENT=$(playerctl shuffle)

case $CURRENT in
    On)
        echo '<span color="#888888"> </span>'
        ;;

    Off)
        echo '<span color="#C07B67"> </span>'
        ;;
esac
