# Todo #

### Short Term Todo ###

WHEN HARDWARE ARRIVES:
Test Viewer
Test sample code for body tracking, note how new bodies are handled and what happens when old bodies leave, e.g. id reassignments?
Pretty much just see if the body tracker renumbers bodies when one leaves, so the program calculates the angle for the actual user.


IF ids not reassigned, check if skeleton data becomes null

See if body tracking SDK sample draws the skeleton, if so implement into imageFIDO at some point with it, if not figure out how to access data. If needed, potentially run the body tracking equivalent of k4 viewer in parallel?

After C tracker is confirmed to work (print out angle, figure out access with a python program, maybe by seeing what happens to the fido file when written to), then reimplement all of game.

### Short Term Findings ###
FIDO write by writing and rewriting the first line of the file it makes in tmp.


### Generic musing ###
For the actual tracker, the FIDO findings mean that two pipes will need to be created, one for image and one for joints. Python file may just want to access that?


#### Long Term Todo ####
Make an Azure Kinect library for DPEA Python programmers, if determined useful for future use.
