# Azure Maze #
Kinetic Maze, with the Azure Kinect instead of XBox Kinect.



## Installation ##
Instructions to install the Azure Kinect SDK are from microsoft, copied here for convinience. No other dependencies should be needed.

1. Configure the Microsoft Package Repository, and install the Azure Kinect packages and headers/cmake files:
```
 curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
 sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod
 sudo apt-get update
 sudo apt install k4a-tools
 sudo apt install libk4a1.1-dev
```


## Azure Kinect on Linux ##
As most Microsoft documentation is windows based, Linux usage will be documented as thoroughly as possible for future use. In general, follow instructions in the Microsoft documentation.

To launch the Azure Kinect Viewer, run `k4aviewer` in the command line.

## Project Info ##
C tracker code is mostly pulled from Microsoft sample code.

Current plan: Create two FIFO pipes, one for image data and one for joint (aka hand angle) data. Then figure out how to access those from python, or another C program. May want to convert entire project to C, but unlikely.

Joint info is priority, to get project back to basic working state on new hardware.

### Things to test ###
See if the body tracker renumbers bodies when one leaves, so the program calculates the angle for the actual user.

### To-do ###
Make an Azure Kinect library for DPEA Python programmers, if determined useful for future use.

WHEN HARDWARE ARRIVES:
Test Viewer
Test sample code for body tracking, note how new bodies are handled and what happens when old bodies leave, e.g. id reassignments?
IF ids not reassigned, check if skeleton data becomes null

See if body tracking SDK sample draws the skeleton, if so implement into imageFIDO at some point with it, if not figure out how to access data. If needed, potentially run the body tracking equivalent of k4 viewer in parallel?

After C tracker is confirmed to work (print out angle, figure out access with a python program, maybe by seeing what happens to the fido file when written to), then reimplement all of game.

## Reference Links ##
[Azure Kinect Samples](https://github.com/microsoft/Azure-Kinect-Samples)
[Azure Kinect SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK)
[Azure Kinect DK Documentation](https://docs.microsoft.com/en-us/azure/kinect-dk/)

[Body Tracking SDK Reference](https://microsoft.github.io/Azure-Kinect-Body-Tracking/release/1.x.x/index.html)
[Azure Kinect Sensor SDK Reference](https://microsoft.github.io/Azure-Kinect-Sensor-SDK/master/index.html)
