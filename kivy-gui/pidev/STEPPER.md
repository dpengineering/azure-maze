# Stepper
This file will give a basic overview of the functionality and uses of the stepper class

## Importing
Make sure you have pidev installed and then use this import statement.
```
from pidev.stepper import stepper
```

## Constructor

```
STEPPER = stepper()
```
When you create a stepper you can pass it a the various parameters detailed below.


**port:** port the stepper is connected to ```port=0```. 
            0-3 on the model XLT, 0-6 on model D.
            
**micro_steps:** how much each step is subdivided ```micro_steps=64```. 
Microstepping is used to give steppers smoother movement at the cost of torque. Most steppers have 200 steps per revolution 
, so if you set the microstepping to 64 the motor will have to move 12,800 'steps' to complete one rotation. acceptable 
values are (1,2,4,8,16,32,64,128) 


**hold_current, run_current, accel_current, deaccel_current**: amount of current going to the motor during different kinds of motion. default value is 20.
This value does not directly correlate to a value in Amps. The accepted values are 1-200 but in most use cases you shouldn't 
need above 20


**steps_per_unit:** Amount of steps per unit. Making use of this parameter will greatly increase the readability of you 
code and also make it easier to write.
Using this parameter and the correct movement functions (explained below)
allows you to move the steppers based on units such as rotations, inches, or millimeters, instead of steps. Default: 
200/25.4 (unit = 1mm on most common type of lead screw).
If you want to control in terms of steps set this to 1.


**speed:** How fast the stepper moves in terms of units Default: 1


## Setting steps_per_unit
### Control by revolutions
Most (Pretty sure all) of the steppers we use in the academy have 200 steps per revolutions. They are often paired with 
gearboxes or a transmission to give them more torque. 
Locate the gearing ratio and multiply that value by 200 to get your steps_per_unit
### Control by distance
Lead screws have a measurement of distance traveled per turn which will most likely be given in inches or millimeters. 
Now we just use basic unit conversion to get our steps_per_unit.
For this example we wil use a lead screw that has .5" per turn, and we want to control it using millimeters as our unit.

(200 steps/1 ~~rev~~) * (1 ~~rev~~/0.5 ~~in~~) * (1 ~~in~~/25.4mm)
which simplifies to 15.75 steps/mm giving us 15.75 for out steps_per_unit value
### Control by steps
If you want to control your motor using steps, set steps_per_unit to 1

## Homing the stepper
```STEPPER.home(direction)```

```direction``` can be either 0 or 1

Once the stepper reaches home it will set it's current position as 0. If your home sensor is offset from where you want 
your 0 position you can move to the position you want as 0 and the use the command ```STEPPER.set_as_home()```

If you project has a continuously rotating device controlled by a stepper, by default the stepper will stop when the limit
switch or proximity sensor are triggered. To disable this behavior run ```STEPPER.set_limit_hardstop(False)```
## Moving the stepper

There are a lot of different functions built in to move the stepper. Most of them will be listed below

```STEPPER.relative_move(distance_in_units)```:  This function takes into account both microstepping and steps_per_unit during the
 move. It is also blocking so your code will not continue until the movement is complete. It is recommend that this is 
 run on another thread
 
```STEPPER.start_relative_move(distance_in_units)```: This function is the same as the relative_move but it is not blocking. 
 NOTE: Once the slushengine has been given a movement command, you can not give it another command until the first one 
 finishes
 
```STEPPER.go_to_position(position_in_units)```: Moves to a position based of your home position. This code is blocking 
so your code will not continue until the movement is complete. It is recommend that this is run on another thread
 
```STEPPER.start_go_to_position(position_in_units)``` Moves to a position based on your home position. NOTE: Once the 
slushengine has been given a movement command, you can not give it another command until the first one 
 finishes
 

## Other useful commands

```STEPPER.stop()``` This will stop the motor in the middle of its motion. Will not decelerate.

```STEPPER.get_position_in_units()``` Will return the current position in units

```STEPPER.is_busy()```  will return True if the motor is currently in a movement. False if it is idle.
