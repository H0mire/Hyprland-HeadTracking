import cv2
import mediapipe as mp
import asyncio
from interfaces.ITracker import ITracker
from utilities.hyprland_ipc import HyprlandIPC


class HeadTracker(ITracker):
    def __init__(self, sensitivity=1, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh()
        self.mp_drawing = mp.solutions.drawing_utils
        self.hyprland = HyprlandIPC()
        self.screen_width, self.screen_height = asyncio.run(
            self.get_screen_dimensions()
        )
        self.sensitivity = sensitivity
        self.previous_x, self.previous_y = None, None

    async def get_screen_dimensions(self):
        return await self.hyprland.get_focused_monitor_dimensions()

    def get_position(self):
        success, image = self.cap.read()
        if not success:
            return None, None, None

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing.DrawingSpec(
                        color=(0, 255, 0), thickness=1, circle_radius=1
                    ),
                )
                nose_tip = face_landmarks.landmark[1]
                x = int(nose_tip.x * self.screen_width)
                y = int(nose_tip.y * self.screen_height)

                # Skalieren Sie die Veränderung der Position basierend auf der Sensitivität
                if self.previous_x is not None and self.previous_y is not None:
                    delta_x = x - self.previous_x
                    delta_y = y - self.previous_y

                    x = self.previous_x + int(delta_x * self.sensitivity)
                    y = self.previous_y + int(delta_y * self.sensitivity)

                self.previous_x, self.previous_y = x, y
                return x, y, image

        return None, None, image

    def display(self, image):
        cv2.imshow("Head Tracking", image)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
