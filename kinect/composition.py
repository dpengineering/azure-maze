from .tracker import Tracker
from .config import global_config as c
from . import logger
import os


l = logger.getChild("composition")

class Kinect:
    def __init__(self, tracker_path, tracker_wd):
        self.tracker_path = tracker_path
        self.tracker_wd = tracker_wd
        self.kmm = None
        self.tracker = None

    def run(self):
        self.tracker = Tracker(self.tracker_path, self.tracker_wd)
        l.info("Starting main loop")
        for angle in self.tracker.stream():
            if angle is not None:
                l.debug("Got angle: %1.2f", angle)
                #ANGLE CODE HERE, angle goes from approx -0.5 to 0.5.
            else:
                #IF ANGLE EQUALS ZERO
                l.debug("ZERO")
