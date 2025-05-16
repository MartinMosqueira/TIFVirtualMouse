import cv2
import mediapipe as mp
import time
import numpy as np
from tensorflow.keras.models import load_model
from training.FormatData import FormatData
from controller.AdaptiveCursor import AdaptiveCursor

class HandTracker:
    def __init__(self, modelHand):
        self.modelHand = modelHand
        self.latest_frame = None

        self.modelFinger = load_model('model/gesture_lstm.h5')
        # number of frames processed by model
        self.T = 30
        self.threshold = 0.6
        self.buffer = []

        # instance the class for move cursor
        self.cursorTracker = AdaptiveCursor(alpha_min=0.2, alpha_max=0.9, speed_sens=3.0)

        # instance the class for dataset
        self.formatData = FormatData()

        # class for config model
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        #HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
        VisionRunningMode = mp.tasks.vision.RunningMode

        # params model
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=modelHand),
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

    def finger_up(self):
        pass

    def run(self):
        # 0:extern camera
        # 1:intern camera
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            # capture the frames from the camera.
            success, frame = cap.read()
            if not success:
                break

            # resolution frame
            height, width, _ = frame.shape

            #======== Convert the frame received from OpenCV to a MediaPipe’s Image object.

            # converts OpenCV BGR frames to RGB for the model
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # create the images in the format that Mediapipe needs RGB
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # ========

            # need to know the time in milliseconds of each frame since it is a video stream,
            # and we do not want them to be displayed out of order.
            timestamp = int(time.time() * 1000)
            self.detector.detect_async(mp_image, timestamp)

            # draw frames if available
            if self.latest_frame and self.latest_frame.hand_landmarks:
                fingerMiddleTip = self.latest_frame.hand_landmarks[0][12]

                self.cursorTracker.move(fingerMiddleTip.x, fingerMiddleTip.y)
                self.draw_landmark(fingerMiddleTip, frame, width, height)

                # ========== TEST MODEL FINGER
                formatFrame = self.formatData.extract_scale_coordinates(self.latest_frame)
                self.buffer.append(formatFrame)
                if len(self.buffer) > self.T:
                    self.buffer.pop(0)

                if len(self.buffer) == self.T:
                    #  convert array (T, 63) to numpy array and add batch dimension
                    seq = np.array(self.buffer)[None, ...]   # shape (1, T, 63)
                    # extract prediction
                    prob = float(self.modelFinger.predict(seq, verbose=0)[0,0])
                    # print(f"Probabilidad de gesto: {prob:.3f}")

                    if prob > self.threshold:
                        # gesture detected
                        self.cursorTracker.click_cursor()
                        self.buffer.clear()
                # ==========


                # extract and format coordinates for dataset
                # coordinates = self.formatData.extract_scale_coordinates(self.latest_frame)
                # self.formatData.format_coordinates(7, 1, coordinates)

            # display frames in video
            cv2.imshow('frame', frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                # output format coordinates
                # self.formatData.get_coordinates()
                break

        # free resources
        cap.release()
        cv2.destroyAllWindows()
