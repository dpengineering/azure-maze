# Todo #

### Short Term Todo ###
See if body tracking SDK sample draws the skeleton. If so, potentially have it draw on its own, while python only controls motors and parsing of angles, as images are not easily passed through FIFO pipes. Again, priority is to getting the game back into a working state, without a full GUI with menus and such. After that, then pass image to pygame and make GUIs.

After C tracker is confirmed to work (print out angle, figure out access with a python program, maybe by seeing what happens to the fido file when written to), then reimplement all of game. Also check out the windows3d visualization system, to see if it's what we want.

#### Software tests,beyond basic working state ####
How does Azure output the body tracking image? How can this image be passed to python for a pygame GUI?
Might need a GUI concept redesign to better fit the project, if needed just slap an arcade joystick on? Or a bluetooth remote? Some sort of station on an arm from the project that can telescope out to where the user would be standing and retract when the game starts?

##### UI Ideas #####
Maybe a pose detector and afk. AFK loop with a welcome message, then when someone approaches and gets in the pose the game detects, gives a few seconds to confirm, starts a countdown to start the game, starts the game, and if completed, if score in the HS list then assign a automatically generated user ID and register, if not show high scores regardless, then go back to afk loop.

If afk detected (original pose user gone), return to the timer, when timer runs out, quit to main waiting loop?

This would allow for a minimal GUI, mostly consisting of text. Could even use a LED strip and have scrolling instructions, instead of displaying also on the screen (which would be pretty small and hard to read from a distance anyways, especially if it's on a boom).

Also write up the user instructions for minimal guidance.

ADMIN SCREEN: Series of hardware switches to act as kill switches on various components?  Key, etc.

##### Fun ideas #####
Nixie tubes as a timer system, just for that retro feel


### Short Term Findings ###
FIFO write by writing and rewriting the first line of the file it makes (currently in tmp).
UArm tracking (arms in |\_o\_| shape) works decently, right arm needs to be slightly out though.


### Generic musing ###
For the actual tracker, the FIFO findings mean that two pipes will need to be created, one for image and one for joints. Python file may just want to access that?


#### Long Term Todo ####
Make an Azure Kinect library for DPEA Python programmers, if determined useful for future use.
