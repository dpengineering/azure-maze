# Azure Maze
Kinetic Maze, with the Azure Kinect instead of XBox Kinect.
Rewrite #3 total, #2 of 2019-2020


##Installation
Instructions to install the Azure Kinect SDK are from microsoft, copied here for convinience.

1. Configure the Microsoft Package Repository, and install the Azure Kinect packages and headers/cmake files:
```
 curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
 sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod
 sudo apt-get update
 sudo apt install k4a-tools
 sudo apt install libk4a1.1-dev
```
