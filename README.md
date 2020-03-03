# Azure Maze #
Kinetic Maze, with the Azure Kinect instead of XBox Kinect.



## Installation ##
Instructions to install the Azure Kinect SDK are from microsoft, copied here for convinience.

1. Configure the Microsoft Package Repository, and install the Azure Kinect packages (tools, headers, and body tracking):
```
 curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
 sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod
 sudo apt-get update
 sudo apt install k4a-tools
 sudo apt install libk4a1.1-dev
 sudo apt install libk4abt1.0-dev
```
Note: requires OpenGL 4.4 and above,

When installing Azure Kinect Samples (Git submodule info):
https://github.com/microsoft/Azure-Kinect-Sensor-SDK/issues/896

if device unavailable after compiling samples, run with sudo as rules not properly set.

```
pip3 install kivy
```


## Azure Kinect on Linux ##
As most Microsoft documentation is windows based, Linux usage will be documented as thoroughly as possible for future use. In general, follow instructions in the Microsoft documentation.

To launch the Azure Kinect Viewer, run `k4aviewer` in the command line.

Joints: x,y,z, measured in mm from the lens of the camera.

## How to Run ##

**OUTDATED - INSTRUCTIONS INTENDED FOR RELEASE v1.0, script deleted from up to date repo**

Compile the tracker by running:
```
make
```
(In the subfolder).

From the project directory:
```
./run.sh
```

If the program crashes, current method of resetting is to restart the computer to free port 7266. Also, to reset the ODrive, wait for the fan on the power supply to stop before turning the power strip back on, to ensure power to the ODrive actually cut.


**To run the current prototype**

**If motors are needed, uncomment the motor lines from main.py**

With two monitors:
Make a terminal window on both screens.

In vis_cpp_tracker, run the trackhands script in /build/bin. If this is not compiled, go to /build and run:
```
rm -r *
cmake ..
make
```
After compiling, follow the instructions from the beginning once more.

Run the script.

On the other terminal window (on the second monitor), run ```python3 main.py```.

With one monitor: change vis_cpp_tracker/libs/k4abt_libs/window_controller_3d/WindowController3d.h line 49 to bool fullscreen = false, then follow the instructions for two monitors.

One monitor can be used with fullscreen, however there will be no way to exit.



## Reference Links ##
[Azure Kinect Samples](https://github.com/microsoft/Azure-Kinect-Samples)

[Azure Kinect SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK)

[Azure Kinect DK Documentation](https://docs.microsoft.com/en-us/azure/kinect-dk/)

[Body Tracking SDK Reference](https://microsoft.github.io/Azure-Kinect-Body-Tracking/release/1.x.x/index.html)

[Azure Kinect Sensor SDK Reference](https://microsoft.github.io/Azure-Kinect-Sensor-SDK/master/index.html)
