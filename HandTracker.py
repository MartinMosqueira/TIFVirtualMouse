import cv2
import mediapipe as mp
import time

class HandTracker:
    def __init__(self, model):
        self.model = model
        self.latest_frame = None

        #clases para configurar el modelo
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        #HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
        VisionRunningMode = mp.tasks.vision.RunningMode

        #Parametreos del modelo
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

    def run(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            #Capturamos los frames de la camara
            success, frame = cap.read()
            if not success:
                break

            height, width, _ = frame.shape

            #======== Convert the frame received from OpenCV to a MediaPipe’s Image object. ======

            #Convierte las frames BGR de OpenCV a RGB para el modelo
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #Creamos las imagenes en el formato que Mediapipe necesita RGB
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # ========

            #Necesitamos saber el tiempo en milisegundos de cada frame ya que es un stram de video
            # y no queremos que se muestren desordenados.
            timestamp = int(time.time() * 1000)
            self.detector.detect_async(mp_image, timestamp)

            # Dibujar los landmarks si están disponibles
            if self.latest_frame and self.latest_frame.hand_landmarks:
                for hand_landmarks in self.latest_frame.hand_landmarks:
                    for landmark in hand_landmarks:
                        cx, cy = int(landmark.x * width), int(landmark.y * height)
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            #Mostrar los frames en video
            cv2.imshow('frame', frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        #Liberar recursos
        cap.release()
        cv2.destroyAllWindows()
