# Azure Maze
Kinetic Maze, with the Azure Kinect instead of XBox Kinect.



## Installation
Instructions to install the Azure Kinect SDK are from microsoft, copied here for convinience. No other dependencies should be needed.

1. Configure the Microsoft Package Repository, and install the Azure Kinect packages and headers/cmake files:
```
 curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
 sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod
 sudo apt-get update
 sudo apt install k4a-tools
 sudo apt install libk4a1.1-dev
```


## Azure Kinect on Linux
As most Microsoft documentation is windows based, Linux usage will be documented as thoroughly as possible for future use. In general, follow instructions in the Microsoft documentation.

To launch the Azure Kinect Viewer, run `k4aviewer` in the command line. 


