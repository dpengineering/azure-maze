# Basic Info about Azure Maze #
*Last Updated: Fev. 10 2020, by Andrew Xie*

This project will be documented in order to avoid the mess of almost all other DPEA projects, where new teams have difficulty understanding code due to complete lack of documentation. This file may be worded/organized strangely and confusingly, if so Harlow should be able to clarify some things or provide contact info to previous teams.

Hopefully this file makes the transition into this decently complex project easier.

*Please update this file when major changes are made, new functionality added, or problems that may be encountered by others solved! Do your part in preventing this from becoming the non-documented (Or inadequately documented) mess typical of other DPEA projects*

## Background ##
Azure maze is the third version of Kinetic Maze software for the DPEA. Version 1 was from Paul, which was replaced with Version 2 from Braedan.

V1 used C for tracking and Python for parsing, and V2 was written off a pure Python tracking implementation found by Braedan. [LINK TO GIT]. That implementation was found to have memory loss/packet loss issues over time, crashing after 5 minutes.

Turns out MS (Microsoft) Azure made a new Kinect last year (Feb. 2019), so one was bought for potential use, which resulted in this project. The vast majority of V3's code consists of modified Azure code, which is worth understanding. A chunk by chunk annotation with comments may be available eventually, but is not written yet.

## Project Structure, Files/Purpose ##

### Subfolders ###
* /tracking stores the C tracker.
* /testing contains the programs used to test possible solutions to problems encountered, and is kept to either test functions without the rest of the maze, or for future testing.

Note that testing may not be updated along with the main project, so the main project's implementations of testing code may differ greatly from what's in /testing.

The rest of the folder is the Python that runs the ODrive based off data from the C tracker, or misc files such as the license, readme, and todo.

### Files of interest ###

Due to parsing data completely in C instead of in Python (see footnote), much of V1's code has been replaced. However referencing it may still be useful. [LINK TO COMMIT]

Todo.md is more of a rambling ideas list, and the unimplemented ideas can be tested someday. (It's honestly disorganized enough that I can't make too much sense of most of it either).

#### The C tracker ####
The C tracker is built off MS Azure Kinect sample code, from a program called simple_sample. It takes the joint data, accesses the hand data, and calculates the angle between the hands of the closest user (found by measuring Z) using atan2 and the X/Y coordinates of the hands. This angle data is then sent along a TCP socket bound to 127.0.0.1, port 7266 [^1].

[^1]: V1 sent all the raw joint info to Python via STDOUT. The C program printf'd the data, and Python read STDOUT and parsed the data. V3 does all the calculations before sending, and sends the angle in degrees. Note that V1 parsed the angle data to radians.

#### physics.py ####
The original motor control code from V1, which could not be replaced due to heavy customization and JSON configs. The JSON configs will eventually be replaced with variables directly in the code.

## Previously Tested Features/Issues + Lessons learned ##

### Specific issues ###
- *C to Python data transfer*
  - *V1:* printing via STDOUT, Python reads STDOUT
  - *V3:*
    - Named pipe server (FIFO): Attempted, difficult to use [^2] and abandoned. (May be considered for other projects with this need)
    - TCP socket transfer: Currently implemented method of data transfer, works well for sending the angle over.
- *Motor control*
  - *V1-3 all use the original physics.py.* A simplifying rewrite may be needed, but usage as a black box works well enough that this is not a priority.
- *Azure Kinect* Most Azure problems have solutions in the SDK Issues page, in the docs, or sample code. Check those carefully first!
  - Don't forget to release the frame after use.

### Generic lessons ###
*Check Issues from Github code that you're copying before you copy, they might reveal some problems that would break your code.* For example, the code used for V2 had an Issue from Jan. 2019 about memory loss that wasn't addressed, and if we saw that before we could've saved three months worth of work.


[^2]: The FIFO server would write to the FIFO file, then need to be closed before Python could read. This would be done very quickly due to constant output of angle data, and Python had difficulty reading. Reading in Python was also a blocking function (non-blocking is possible via a flag). Overall not worth the hassle.