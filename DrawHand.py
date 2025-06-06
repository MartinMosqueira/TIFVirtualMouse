import cv2

class DrawHand:
    def __init__(self,
                 landmark_color=(159, 239, 0),
                 landmark_radius=10,
                 landmark_thickness=2):

        self.landmark_color = landmark_color
        self.landmark_radius = landmark_radius
        self.landmark_thickness = landmark_thickness

    def draw_landmark(self, landmark, frame, width, height, thickness=None):
        cx = int(landmark.x * width)
        cy = int(landmark.y * height)

        radiusExtern = self.landmark_radius

        if thickness is None:
            radiusIntern = radiusExtern - self.landmark_thickness - 4
            if radiusIntern < 1:
                radiusIntern = 1
            cv2.circle(frame,
                       (cx, cy),
                       radiusIntern,
                       self.landmark_color,
                       -1)

            cv2.circle(frame,
                       (cx, cy),
                       radiusExtern,
                       self.landmark_color,
                       self.landmark_thickness)
        else:
            cv2.circle(frame,
                       (cx, cy),
                       radiusExtern,
                       self.landmark_color,
                       thickness)

    def draw_landmarks_finger_tips(self, landmarksHand, frame, width, height):
        fingerTips = [4, 8, 16, 20]
        for fingerTip in fingerTips:
            landmark = landmarksHand[fingerTip]
            self.draw_landmark(landmark, frame, width, height)

    def draw_landmark_detected(self, frame, width, radius= None):
        offset_x = 10
        offset_y = 10

        cx = width - offset_x - radius
        cy = offset_y + radius

        if radius is None:
            radius = self.landmark_radius

        radiusIntern = radius - self.landmark_thickness
        if radiusIntern < 1:
            radiusIntern = 1
        cv2.circle(frame,
                   (cx, cy),
                   radiusIntern,
                   (0, 255, 255),
                   -1)
        cv2.circle(frame,
                     (cx, cy),
                     radius,
                     (0, 0, 0),
                     1)
