import cv2
import mediapipe as mp
import time
import numpy as np
from playsound import playsound
from tensorflow.keras.models import load_model
from training.FormatData import FormatData
from controller.AdaptiveCursor import AdaptiveCursor
from DrawHand import DrawHand

class HandTracker:
    def __init__(self, modelHand):
        self.modelHand = modelHand
        self.latest_frame = None

        self.modelFinger = load_model('model/gesture/gesture_lstm_multiclass.h5')
        # number of frames processed by model
        self.T = 30
        self.threshold = 0.9
        self.buffer = []

        # instance the class for move cursor
        self.cursorTracker = AdaptiveCursor(alpha_min=0.2, alpha_max=0.9, speed_sens=3.0)

        # instance the class for dataset
        self.formatData = FormatData()

        # instance the class for draw hand
        self.drawHand = DrawHand()

        # draw gesture detected
        self.highlight_until = 0.0
        self.highlight_duration = 0.3

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

    def run(self):
        # 0:extern camera
        # 1:intern camera
        cap = cv2.VideoCapture(0)

        counter = 0
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
                self.drawHand.draw_landmark(fingerMiddleTip, frame, width, height, thickness=-1)
                self.drawHand.draw_landmarks_finger_tips(self.latest_frame.hand_landmarks[0], frame, width, height)

                # ========== TEST MODEL CLICK GESTURE
                '''
                formatFrame = self.formatData.extract_align_coordinates(self.latest_frame)
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
                        self.cursorTracker.click_left_cursor()
                        self.buffer.clear()
                        self.highlight_until = time.time() + self.highlight_duration
                '''
                # ==========

                # ========== TEST MODEL MULTICLASS GESTURE

                formatFrame = self.formatData.extract_align_coordinates(self.latest_frame)
                self.buffer.append(formatFrame)
                if len(self.buffer) > self.T:
                    self.buffer.pop(0)
                    
                if len(self.buffer) == self.T:
                    #  convert array (T, 63) to numpy array and add batch dimension
                    seq = np.array(self.buffer)[None, ...]   # shape (1, T, 63)
                    # extract prediction
                    prob = self.modelFinger.predict(seq, verbose=0)[0]
                    predicted_class = np.argmax(prob)

                    confidence = prob[predicted_class]
                    if confidence > 0.7:
                        if predicted_class == 1:
                            # gesture detected click left
                            self.cursorTracker.click_left_cursor()
                            self.buffer.clear()
                            self.highlight_until = time.time() + self.highlight_duration
                            print('Click left')
                        elif predicted_class == 2:
                            # gesture detected click right
                            self.cursorTracker.click_right_cursor()
                            self.buffer.clear()
                            self.highlight_until = time.time() + self.highlight_duration
                            print('Click right')
                        elif predicted_class == 3:
                            # gesture detected scroll
                            self.cursorTracker.scroll_down_cursor()
                            self.buffer.clear()
                            self.highlight_until = time.time() + self.highlight_duration
                            print('Scroll down')

                # ==========

                should_highlight = time.time() < self.highlight_until
                if should_highlight:
                    self.drawHand.draw_landmark_detected(frame, width, radius=15)
                    playsound('sound/pop.mp3', block=False)


                # ========== extract and format coordinates for dataset

                #coordinates = self.formatData.extract_align_coordinates(self.latest_frame)
                #self.formatData.format_coordinates(300, 0, coordinates)
                #self.formatData.not_format_coordinates(coordinates)

                # ==========

            # display frames in video
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'): # or counter == 30
                # ========== write coordinates in file

                #self.formatData.write_file('training/data/gesture/gestures.csv')
                #self.formatData.write_file('training/example.csv')

                # ==========

                break
            counter += 1

        # free resources
        cap.release()
        cv2.destroyAllWindows()
