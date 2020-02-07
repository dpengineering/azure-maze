import os
import logging
import argparse
from . import Kinect, logger

if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)-7s | %(asctime)-23s | %(name)-8s | %(message)s")
    parser = argparse.ArgumentParser(description="Run the kinect.")

    parser.add_argument("tracker_path",
                        help="path to the `trackhands` executable")
    parser.add_argument("tracker_working_directory",
                        help="path to the working directory containing the data for trackhands")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="set logging to DEBUG")

    args = parser.parse_args()
    if args.verbose:
        logger.setLevel("DEBUG")

    km = Kinect(os.path.abspath(args.tracker_path),
                     os.path.abspath(args.tracker_working_directory))
    km.run()
