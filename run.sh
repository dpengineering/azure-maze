#!/bin/bash

# CD to the directory that contains this script
cd $(dirname $(readlink -f "$0"))

python3 -m main.py -v tracking-module/trackhands /usr/lib
