import cv2
import mediapipe as mp
import time
from CursorTracker import CursorTracker

class HandTracker:
    def __init__(self, model):
        self.model = model
        self.latest_frame = None
        self.smoothing=0.5

        #Instance the class for move cursor
        self.cursorTracker = CursorTracker(self.smoothing)

        #Class for config model
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        #HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
        VisionRunningMode = mp.tasks.vision.RunningMode

        #Params model
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model),
            running_mode=VisionRunningMode.LIVE_STREAM,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            num_hands=1,
            result_callback=self.output_frame)

        self.detector =  HandLandmarker.create_from_options(options)

    def output_frame(self, result, output_image: mp.Image, timestamp_ms: int):
        self.latest_frame = result

    def draw_landmark(self, landmark, frame, width, height):
        cx, cy = int(landmark.x * width), int(landmark.y * height)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    def run(self):
        # 0:extern camera
        # 1:intern camera
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            #Capture the frames from the camera.
            success, frame = cap.read()
            if not success:
                break

            #Resolution frame
            height, width, _ = frame.shape

            #======== Convert the frame received from OpenCV to a MediaPipe’s Image object. =========

            #Converts OpenCV BGR frames to RGB for the model
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #We create the images in the format that Mediapipe needs RGB
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # ========

            #Need to know the time in milliseconds of each frame since it is a video stream,
            #and we do not want them to be displayed out of order.
            timestamp = int(time.time() * 1000)
            self.detector.detect_async(mp_image, timestamp)

            #Draw frames if available
            if self.latest_frame and self.latest_frame.hand_landmarks:
                fingerIndex = self.latest_frame.hand_landmarks[0][8]

                self.cursorTracker.move_cursor(fingerIndex.x, fingerIndex.y)
                self.draw_landmark(fingerIndex, frame, width, height)

            #Display frames in video
            cv2.imshow('frame', frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        #Free resources
        cap.release()
        cv2.destroyAllWindows()
