LENGTH=$(playerctl metadata mpris:length)
LENGTH=$(($LENGTH/1000000))
POSITION=$(playerctl position)
POSITION=${POSITION%.*}

LEN_M=$((LENGTH/60))
LEN_M=$(printf "%02d" $LEN_M)
LEN_S=$((LENGTH%60))
LEN_S=$(printf "%02d" $LEN_S)

POS_M=$((POSITION/60))
POS_M=$(printf "%02d" $POS_M)
POS_S=$((POSITION%60))
POS_S=$(printf "%02d" $POS_S)

echo "$POS_M:$POS_S / $LEN_M:$LEN_S"
