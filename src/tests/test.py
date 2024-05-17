import asyncio
import os
from utilities.hyprland_ipc import HyprlandIPC


async def test_connection():
    try:
        ipc = HyprlandIPC()
        response = await ipc.send_and_receive("ping")
        print("Connected successfully!")
        print("Response:", response)
    except Exception as e:
        print("Connection failed:", e)


if __name__ == "__main__":
    instance_signature = os.getenv("HYPRLAND_INSTANCE_SIGNATURE")
    if not instance_signature:
        print("HYPRLAND_INSTANCE_SIGNATURE environment variable is not set")
    else:
        asyncio.run(test_connection())
