import argparse
from trackers.head_tracker import HeadTracker
from focus_controller import FocusController
from tests.test import test_connection
import asyncio
import os

from trackers.eye_tracker import EyeTracker  # Import the EyeTracker

os.environ["QT_QPA_PLATFORM"] = "xcb"  # or 'xcb'


def main():
    parser = argparse.ArgumentParser(description="Run head tracking or eye tracking.")
    parser.add_argument(
        "mode", choices=["head", "eye"], help="Choose tracking mode: 'head' or 'eye'"
    )
    parser.add_argument(
        "--mouse-control", action="store_true", help="Enable mouse control"
    )  # Add the argument for mouse control

    parser.add_argument(
        "--camera-index", type=int, default=0, help="Specify the camera index"
    )

    args = parser.parse_args()

    if args.mode == "head":
        # Execute head_tracking.py
        tracker = HeadTracker()
        controller = FocusController(
            tracker, mouse_control=args.mouse_control
        )  # Pass the mouse_control argument to FocusController
        controller.run()
    elif args.mode == "eye":
        # Execute eye_tracking.py
        tracker = EyeTracker()
        controller = FocusController(
            tracker, mouse_control=args.mouse_control
        )  # Pass the mouse_control argument to FocusController
        controller.run()
    elif args.mode == "test":
        asyncio.run(test_connection())


if __name__ == "__main__":
    main()
