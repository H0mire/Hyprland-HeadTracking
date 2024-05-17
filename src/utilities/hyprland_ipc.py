import os
import asyncio
import json


class HyprlandIPC:
    def __init__(self):
        instance_signature = os.getenv("HYPRLAND_INSTANCE_SIGNATURE")
        if not instance_signature:
            raise EnvironmentError(
                "HYPRLAND_INSTANCE_SIGNATURE environment variable is not set"
            )
        self.socket_path = f"/tmp/hypr/{instance_signature}/.socket.sock"

    async def send_and_receive(self, command, flags=""):
        try:
            reader, writer = await asyncio.open_unix_connection(self.socket_path)
            writer.write((flags + "/" + command).encode("utf-8"))
            await writer.drain()

            data = ""
            while True:
                line = await reader.readline()
                if not line:
                    break
                data += line.decode("utf-8")

            writer.close()
            await writer.wait_closed()

            return data

        except Exception as e:
            print("Error:", e)

    async def get_windows(self):
        response = await self.send_and_receive("clients", "j")
        if not response:
            return []
        # load json
        response = json.loads(response)
        return response

    async def focus_window(self, window_address):
        response = await self.send_and_receive(
            f"dispatch focuswindow address:{window_address}"
        )
        if "ok" in response:
            print(f"Focused window: {window_address}")
        else:
            print(f"Failed to focus window: {window_address}")

    async def move_cursor(self, x, y):
        response = await self.send_and_receive(f"dispatch movecursor {x} {y}")
        if "ok" in response:
            print(f"Moved cursor to: {x}, {y}")
        else:
            print(f"Failed to move cursor to: {x}, {y}")

    async def move_cursor_to_corner(self, corner=0):
        response = await self.send_and_receive(f"dispatch movecursortocorner {corner}")
        if "ok" in response:
            print(f"Moved cursor to corner: {corner}")
        else:
            print(f"Failed to move cursor to corner: {corner}")

    async def get_focused_monitor_dimensions(self):
        response = await self.send_and_receive("monitors", "j")
        if not response:
            return 0, 0
        # load json
        response = json.loads(response)

        for monitor in response:
            if monitor["focused"]:
                width, height, pos_x, pos_y = (
                    monitor["width"],
                    monitor["height"],
                    monitor["x"],
                    monitor["y"],
                )
                return width, height, pos_x, pos_y
