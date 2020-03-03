#! /bin/bash

while true
do

eval $(xdotool getmouselocation --shell)

if [ $X -gt 1258 ]
then
xdotool mousemove 1258, $Y
fi

done
