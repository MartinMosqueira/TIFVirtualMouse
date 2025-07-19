import cv2
import time
import numpy as np
import mediapipe as mp
import tensorflow as tf
from playsound import playsound
from training.FormatData import FormatData
from DrawHand import DrawHand
from ResourcePaths import resource_path


class HandTracker:
    def __init__(self, model_hand, cursor_controller):
        # config app
        self.enable_sound = True
        self.show_camera = True
        self.camera = 0

        self.cursor_controller = cursor_controller
        self.model_hand = model_hand
        self.format_data = FormatData()
        self.draw_hand = DrawHand()

        # manage frames
        self.buffer = []
        self.latest_frame = None

        # config models gesture
        self.model_gestures = tf.lite.Interpreter(resource_path('model/gesture/gesture_lstm_multiclass.tflite'))
        self.model_finger = tf.lite.Interpreter(resource_path('model/gesture/gesture_lstm.tflite'))
        self.model_gestures.allocate_tensors()
        self.model_finger.allocate_tensors()
        self.input_model_gestures = self.model_gestures.get_input_details()[0]
        self.input_model_finger = self.model_finger.get_input_details()[0]
        self.output_model_gestures = self.model_gestures.get_output_details()[0]
        self.output_model_finger = self.model_finger.get_output_details()[0]
        self.T = 30
        self.threshold = 0.9

        # state of gesture
        self.highlight_until = 0.0
        self.highlight_duration = 0.3

        # class for config model
        base_options = mp.tasks.BaseOptions
        hand_landmarker = mp.tasks.vision.HandLandmarker
        hand_landmarker_options = mp.tasks.vision.HandLandmarkerOptions
        # HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
        vision_running_mode = mp.tasks.vision.RunningMode

        # params model
        options = hand_landmarker_options(
            base_options=base_options(model_asset_path=model_hand),
            running_mode=vision_running_mode.LIVE_STREAM,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            num_hands=1,
            result_callback=self.output_frame)

        self.detector = hand_landmarker.create_from_options(options)

    def output_frame(self, result, output_image: mp.Image, timestamp_ms: int):
        self.latest_frame = result

    def run(self):
        # 0:extern camera
        # 1:intern camera
        cap = cv2.VideoCapture(int(self.camera))

        while cap.isOpened():
            # capture the frames from the camera.
            success, frame = cap.read()
            if not success:
                break

            # resolution frame
            height, width, _ = frame.shape

            # ======== Convert the frame received from OpenCV to a MediaPipe’s Image object.

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
                fingermiddle_tip = self.latest_frame.hand_landmarks[0][12]

                self.cursor_controller.move(fingermiddle_tip.x, fingermiddle_tip.y)
                self.draw_hand.draw_landmark(fingermiddle_tip, frame, width, height, thickness=-1)
                self.draw_hand.draw_landmarks_finger_tips(self.latest_frame.hand_landmarks[0], frame, width, height)

                # ========== TEST MODELS GESTURE

                format_frame = self.format_data.extract_align_coordinates(self.latest_frame)
                self.buffer.append(format_frame)
                if len(self.buffer) > self.T:
                    self.buffer.pop(0)

                if len(self.buffer) == self.T:
                    #  convert array (T, 63) to numpy array and add batch dimension
                    seq = np.array(self.buffer)[None, ...]  # shape (1, T, 63)

                    # ============ BINARY MODEL PREDICTION ============
                    convert_frames = seq.astype(np.float32)
                    self.model_finger.set_tensor(self.input_model_finger['index'], convert_frames)
                    self.model_finger.invoke()
                    output_model_finger = self.model_finger.get_tensor(self.output_model_finger['index'])
                    prob_click = float(output_model_finger[0, 0])
                    if prob_click > self.threshold:
                        if self.enable_sound: playsound(resource_path('assets/sound/pop.mp3'), block=False)
                        self.cursor_controller.click_left_cursor()
                        self.buffer.clear()
                        self.highlight_until = time.time() + self.highlight_duration
                        print('Click left')

                    # ============ MULTICLASS MODEL PREDICTION ============
                    else:
                        self.model_gestures.set_tensor(self.input_model_gestures['index'], convert_frames)
                        self.model_gestures.invoke()
                        output_model_gestures = self.model_gestures.get_tensor(self.output_model_gestures['index'])
                        prediction = int(np.argmax(output_model_gestures))
                        confidence = float(np.max(output_model_gestures))

                        if confidence > self.threshold:
                            if prediction == 1:
                                self.cursor_controller.click_left_cursor()
                                print('Click left')
                            elif prediction == 2:
                                self.cursor_controller.click_right_cursor()
                                print('Click right')
                            elif prediction == 3:
                                self.cursor_controller.scroll_down_cursor()
                                print('Scroll down')

                            if self.enable_sound: playsound(resource_path('assets/sound/pop.mp3'), block=False)
                            self.buffer.clear()
                            self.highlight_until = time.time() + self.highlight_duration

                # ==========

                should_highlight = time.time() < self.highlight_until
                if should_highlight:
                    self.draw_hand.draw_landmark_detected(frame, width, radius=15)

            # display frames in video
            cv2.imshow('Visionic', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # free resources
        cap.release()
        cv2.destroyAllWindows()
