import cv2
import mediapipe as mp
from interfaces.ITracker import ITracker
from utilities.hyprland_ipc import HyprlandIPC
import asyncio


class EyeTracker(ITracker):
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1)
        self.mp_drawing = mp.solutions.drawing_utils
        self.hyprland = HyprlandIPC()
        self.screen_width, self.screen_height = asyncio.run(
            self.get_screen_dimensions()
        )

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
                # Use landmarks to calculate the eye position.
                left_eye_x = (
                    face_landmarks.landmark[133].x + face_landmarks.landmark[173].x
                ) / 2
                left_eye_y = (
                    face_landmarks.landmark[133].y + face_landmarks.landmark[173].y
                ) / 2
                right_eye_x = (
                    face_landmarks.landmark[362].x + face_landmarks.landmark[398].x
                ) / 2
                right_eye_y = (
                    face_landmarks.landmark[362].y + face_landmarks.landmark[398].y
                ) / 2

                # Calculate average eye position
                eye_x = int((left_eye_x + right_eye_x) / 2 * self.screen_width)
                eye_y = int((left_eye_y + right_eye_y) / 2 * self.screen_height)
                print(eye_x, eye_y)
                return eye_x, eye_y, image

        return None, None, image

    def display(self, image):
        cv2.imshow("Eye Tracking", image)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
