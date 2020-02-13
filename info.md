# Basic Info about Azure Maze #
**Last Updated: Feb. 12 2020, by Andrew Xie**

| Date | Project Status |
|------|------|
| 1/29/2020 | Azure Kinect software setup, code and repository prepared for hardware. |
| 1/31/2020 | First Azure Kinect arrived at DPEA. |
| 2/12/2020 | Reached working status with motors, minimum viable product. |

This project will be documented in order to avoid the mess of almost all other DPEA projects, where new teams have difficulty understanding code due to complete lack of documentation. This file may be worded/organized strangely and confusingly, if so Harlow should be able to clarify some things or provide contact info to previous teams.

Hopefully this file makes the transition into this decently complex project easier. Instructions on running the project will be stored in the readme.

*Please update this file when major changes are made, new functionality added, or problems that may be encountered by others are solved!* Do your part in preventing this from becoming the non-documented (Or inadequately documented) mess typical of other DPEA projects.

## Background ##
Azure maze is the third version of Kinetic Maze software for the DPEA. Version 1 was from Paul, which was replaced with Version 2 from Braedan.

[V1](https://github.com/dpengineering/kinetic-maze/tree/6517ff8c6544c4c8287182b5a3d50727d381c097) used C for tracking and Python for parsing, and [V2](https://github.com/bkenndpngineering/Kinetic-Maze-Reborn) was written off a pure Python tracking implementation found by Braedan. That implementation was found to have memory loss/packet loss issues over time, crashing after 5 minutes.

Turns out MS (Microsoft) Azure made a new Kinect last year (Feb. 2019), so one was bought for potential use, which resulted in this project. The vast majority of V3's code consists of modified Azure code, which is worth understanding. A chunk by chunk annotation with comments may be available eventually, but is not written yet.

## V.1 Project Structure, Files/Purpose ##
V1 is run via a shell script, and has a similar format to V3, since you have to run ```make``` in the tracker directory.

This program is a useful starting point for learning about the project's structure (via following import statements around different files), and a good study of using logger. However, now that Azure Maze has reached the same point in a more simple way, and likely will be the hardware/version used for future builds, it's more highly recommended to study how Azure Maze works.

## V.2 Project Structure, Files/Purpose ##
V2 is run directly through ```python3 main.py```. The current implementation has a interactive GUI and score input screen, however suffers **severe** memory/packet loss and will crash after 4 minutes max. Instead of using a C tracker, V2 uses a NiTE/OpenNI2 Python tracker stored in the submodule Kinect_Skeleton_Tracker, which needs to be initialized before running the program!

The primary purpose of V2 after being abandoned is to act as a demo for a pygame GUI that can be interacted with by a body tracker.

Likely cause of the memory loss is not releasing the tracked frame after being used, as the Azure Kinect requires. Finding a function to do that in the library will be needed, or adding a command to the library. As I could not find where the library is stored, this was not done and so there is no confirmation that releasing the frame will fix the packet loss.

### The V2 GUI ###
The GUI is 100% button based. Buttons are pressed by holding a hand over the button (so the onscreen location of the tracked hand, indicated with a circle drawn around the hand joint, is on the button), and the button will fade from green to red over a short time. This is to prevent accidental button presses, and is possible to disable.

Screens are displayed via a variable that saves the name of the current screen, and an if statement within the loop checks which "gamestate" (the screen name) is displayed and renders accordingly. Each loop deals with a single frame of tracked data.


## V.3 Project Structure, Files/Purpose ##

### Subfolders ###
* /tracking stores the C tracker.
* /testing contains the programs used to test possible solutions to problems encountered, and is kept to either test functions without the rest of the maze, or for future testing.

Note that testing may not be updated along with the main project, so the main project's implementations of testing code may differ greatly from what's in /testing.

The rest of the folder is the Python that runs the ODrive based off data from the C tracker, or misc files such as the license, readme, and todo.

### Files of interest ###

Due to parsing data completely in C instead of in Python (see footnote), much of V1's code has been replaced. However referencing it may still be useful. [Here](https://github.com/dpengineering/kinetic-maze/tree/38de238fccfc4a8ec9930c75112bbee1b0594ff2) is one of the commits with most of V1 intact, but with more joints being output and a basic skeleton tracking attempt in Pygame added.

Todo.md is more of a rambling ideas list, and the unimplemented ideas can be tested someday. (It's honestly disorganized enough that I can't make too much sense of most of it either).

#### The C tracker ####
The C tracker is built off MS Azure Kinect sample code, from a program called simple_sample. It takes the joint data, accesses the hand data, and calculates the angle between the hands of the closest user (found by measuring Z) using atan2 and the X/Y coordinates of the hands. This angle data is then sent along a TCP socket bound to 127.0.0.1, port 7266 [1].



#### physics.py ####
The original motor control code from V1, which could not be replaced due to heavy customization and JSON configs. The JSON configs will eventually be replaced with variables directly in the code.

#### run.sh ####
The run script is more complex than V1's, as the C server needs to be started slightly before the Python client. If you need output messages, unpipe the two processes from null. Be aware that both server and client will print at the same time, so remember to comment out the messages you don't need (print/printf) (> /dev/null 2>&1). **If the C program fails to create/bind a socket, exit asap and restart!**

## Previously Tested Features/Issues + Lessons learned ##

### Specific issues/solutions/implementations ###
- C to Python data transfer
  - V1: printing via STDOUT, Python reads STDOUT
  - V3:
    - Named pipe server (FIFO): Attempted, difficult to use [2] and abandoned. (May be considered for other projects with this need)
    - TCP socket transfer: Currently implemented method of data transfer, works well for sending the angle over.
- Motor control
  - *V1-3 all use the original physics.py.* A simplifying rewrite may be needed, but usage as a black box works well enough that this is not a priority.
  - physics.py can be a bit iffy, when rebooting remember to also cycle *all* the power strips to reset odrive, and to unplug everything from the Kinect for a full reset.
- Azure Kinect
  - Most Azure problems have solutions in the SDK Issues page, in the docs, or sample code. Check those carefully first!
  - Don't forget to release the frame after use.


### Generic lessons ###
**Check Issues from Github code that you're copying before you copy, they might reveal some problems that would break your code.** For example, the code used for V2 had an Issue from Jan. 2019 about memory loss that wasn't addressed, and if we saw that before we could've saved three months worth of work.

**Google your problems!** Chances are, someone on Stack Overflow has had your exact problem and the solution is on there. Learning to Google problems efficiently is the vast majority of problem solving.

## Footnotes and Important links ##

### Documentation ###

[Azure Kinect Samples](https://github.com/microsoft/Azure-Kinect-Samples)

[Azure Kinect SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK)

[Azure Kinect DK Documentation](https://docs.microsoft.com/en-us/azure/kinect-dk/)

[Body Tracking SDK Reference](https://microsoft.github.io/Azure-Kinect-Body-Tracking/release/1.x.x/index.html)

[Azure Kinect Sensor SDK Reference](https://microsoft.github.io/Azure-Kinect-Sensor-SDK/master/index.html)

### Old Code ###

[Kinetic Maze V1, pre-2019](https://github.com/dpengineering/kinetic-maze/tree/6517ff8c6544c4c8287182b5a3d50727d381c097)

[Kinetic Maze V2 (Reborn), Nov 2019 - Jan 2020](https://github.com/bkenndpngineering/Kinetic-Maze-Reborn)

### Footnotes ###

[1]: V1 sent all the raw joint info to Python via STDOUT. The C program printf'd the data, and Python read STDOUT and parsed the data. V3 does all the calculations before sending, and sends the angle in degrees. Note that V1 parsed the angle data to radians.

[2]: The FIFO server would write to the FIFO file, then need to be closed before Python could read. This would be done very quickly due to constant output of angle data, and Python had difficulty reading. Reading in Python was also a blocking function (non-blocking is possible via a flag). Overall not worth the hassle.
