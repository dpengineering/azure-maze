import os
import time
import math
import numpy as np
import select
import argparse
import subprocess
import collections
from . import logger
from .linalg_helpers import *


l = logger.getChild("tracker")

PREFIX = b"HT! "
HAND_DATA = b"HAND DATA: "
SEP_CHAR = b"|"
FRAME_END = b"FRAME END"

DEG_TO_RAD = (2 * math.pi) / 360

class Tracker(object):
    def __init__(self, tracker, working_directory):
        self.tracker = tracker
        self.working_directory = working_directory
        self.proc = None

    def sync_stream(self):
        # After a long-running operation such as the TAS, a large amount of data
        # can build up in the proc.stdout buffer. `select` checks if data is available,
        # which allows us to skip past the data that has built up.
        # When select returns false, there is no more data available and we are back
        # to "real-time."
        while self.proc.stdout in select.select([self.proc.stdout], [], [], 0)[0]:
            self.proc.stdout.readline()

    def get_frame(self):
        angle = self.proc.stdout.readline().strip()
        return angle

    def stream(self):
        time.sleep(4)
        l.info("Beginning stream")
        self.proc = subprocess.Popen([self.tracker], cwd=self.working_directory,
                                     stdout=subprocess.PIPE)
        try:
            while True:
                angle = self.get_frame()
                yield angle
        finally:
            l.warn("Killing process after exception")
            self.proc.kill()
