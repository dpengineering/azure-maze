#! /bin/bash

echo "Starting mouse limiter."
while true
do

eval $(xdotool getmouselocation --shell)

if [ $X -gt 1265 ]
then
xdotool mousemove 1265, $Y
fi

done
