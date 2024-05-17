import asyncio
import time
from utilities.hyprland_ipc import HyprlandIPC
from interfaces.ITracker import ITracker
import cv2


class FocusController:
    def __init__(self, tracker: ITracker, mouse_control=False):
        self.hyprland = HyprlandIPC()
        self.tracker = tracker
        self.last_focused_window = None
        self.mouse_control = mouse_control

    async def update_focus(self):
        while True:
            try:
                x, y, image = self.tracker.get_position()

                if self.mouse_control:
                    await self.hyprland.move_cursor(x, y)

                if x is not None and y is not None:
                    windows = await self.hyprland.get_windows()
                    target_window = None
                    for window in windows:
                        # Extract params by splitting by newline
                        window_address = window["address"]
                        win_x, win_y, win_width, win_height = (
                            window["at"][0],
                            window["at"][1],
                            window["size"][0],
                            window["size"][1],
                        )

                        if (
                            win_x is not None
                            and win_y is not None
                            and win_width is not None
                            and win_height is not None
                        ):
                            if (
                                win_x <= x <= win_x + win_width
                                and win_y <= y <= win_y + win_height
                            ):
                                target_window = window_address
                                break

                    if target_window and target_window != self.last_focused_window:
                        await self.hyprland.focus_window(target_window)
                        # Optional: move the cursor to the top left corner of the window if you dont want to see the cursor
                        # await self.hyprland.move_cursor_to_corner(0)
                        self.last_focused_window = target_window

                # self.tracker.display(image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break

                time.sleep(0.1)
            except Exception as e:
                print("Error:", e)

    def run(self):
        try:
            asyncio.run(self.update_focus())
        finally:
            self.tracker.release()
