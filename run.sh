#! /bin/bash



FILE=./vis_cpp_tracker/build/bin/trackhands
if ! [[ -f "$FILE" ]]; then
    echo "Trackhands not compiled!"
    exit
fi

echo "Azure Maze starting."


echo "Starting Trackhands"
export DISPLAY:=1
./vis_cpp_tracker/build/bin/trackhands &
declare -i track_PID=$!
echo "Trackhands PID: ${track_PID}"

sleep 0.5
echo "Starting Python"
python3 -m main.py -v tracking-module/trackhands /usr/lib &
declare -i py_PID=$!
echo "Python PID: ${py_PID}"




echo "Starting mouse limiter."

while true
do

eval $(xdotool getmouselocation --shell)

if [ $X -gt 1265 ]
then
xdotool mousemove 1265, $Y
fi

read ans

if [[ $ans == "exit" ]]; then
  kill $py_PID
  kill $track_PID
  echo "Program exited."
fi

done
