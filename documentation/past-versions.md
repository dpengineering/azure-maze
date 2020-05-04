# Previous versions #

## Background ##
Azure maze is the **third** version of Kinetic Maze software for the DPEA.

[V1](https://github.com/dpengineering/kinetic-maze/tree/6517ff8c6544c4c8287182b5a3d50727d381c097) used C for tracking and Python for parsing.
[V2](https://github.com/bkenndpngineering/Kinetic-Maze-Reborn) was written off a pure Python tracking implementation. That implementation was found to have memory loss/packet loss issues over time, crashing after 3 minutes.

Microsoft Azure made a new Kinect last year (Feb. 2019), so one was bough. The vast majority of V3's code consists of modified Azure code.

---

## V.1 Project Structure, Files/Purpose ##
V1 is run via a shell script, and has a similar format to V3, since you have to run ```make``` in the tracker directory.

This program is a useful starting point for learning about the project's structure.

V1 was abandoned due to reliance on black box example code, and limits on accessing tracking data. Only one source could access the data at a time, so adding display would involve a major rewrite regardless.

---

## V.2 Project Structure, Files/Purpose ##
V2 is run through ```python3 main.py```. The current implementation has a interactive GUI and score input screen, however suffers severe memory loss and will crash after 4 minutes max. Instead of using a C tracker, V2 uses a NiTE/OpenNI2 Python tracker stored in the submodule Kinect_Skeleton_Tracker, which needs to be initialized before running the program.

The likely cause of the memory loss is not releasing the tracked frame after being used, as the Azure Kinect requires. Finding a function to do that in the library will be needed, or adding a command to the library. As I could not find where the library is, I couldn't add a frame release and so there is no confirmation that releasing the frame will fix the packet loss.

V2 was abandoned due to packet loss.

### The V.2 GUI ###
The V2 GUI is button based. Buttons are pressed by holding a hand over the button (so the onscreen location of the tracked hand, indicated with a circle drawn around the hand joint, is on the button), and the button will fade from green to red over a short time. This is to prevent accidental button presses, and is possible to disable.

Screens are displayed via a variable that saves the name of the current screen, and an if statement within the loop checks which "gamestate" (the screen name) is displayed and renders accordingly. Each loop deals with a single frame of tracked data.

---
