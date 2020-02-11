#!/bin/bash

# CD to the directory that contains this script
cd $(dirname $(readlink -f "$0"))

echo "Starting Trackhands"
./tracking-module/trackhands > /dev/null 2>&1 &
declare -i track_PID=$!

sleep 0.5
echo "Starting Python"
python3 -m main.py -v tracking-module/trackhands /usr/lib > /dev/null 2>&1 &
declare -i py_PID=$!

read ans

if [[ $ans == "exit" ]]; then
  kill $py_PID
  kill $track_PID
  echo "Program exited."
fi
