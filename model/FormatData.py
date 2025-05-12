import math

class FormatData:
    def __init__(self):
        self.coordinates = []
        self.index = 0

    def extract_coordinates(self, frame):
        coordinate = []
        for fm in frame.hand_landmarks[0]:
            coordinate.extend([fm.x, fm.y, fm.z])
        return coordinate

    def extract_center_coordinates(self, frame):
        originPoint = frame.hand_landmarks[0][0]
        coordinates = []
        for lm in frame.hand_landmarks[0]:
            coordinates.extend([
                lm.x - originPoint.x,
                lm.y - originPoint.y,
                lm.z - originPoint.z
            ])
        return coordinates

    def extract_scale_coordinates(self,frame):
        originPoint = frame.hand_landmarks[0][0]
        middlePoint = frame.hand_landmarks[0][12]

        centered = self.extract_center_coordinates(frame)
        groupCentered = list(zip(*(iter(centered),) * 3))

        euclideanDistance = self.euclidean_distance(originPoint, middlePoint)
        if euclideanDistance == 0:
            euclideanDistance = 1e-6

        coordinates = []
        for x,y,z in groupCentered:
            coordinates.extend([x / euclideanDistance, y / euclideanDistance, z / euclideanDistance])
        return coordinates

    def euclidean_distance(self, p1, p2):
        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2 +
            (p1.z - p2.z) ** 2
        )

    def format_coordinates(self, sequence, istrue, coordinates):
        formatCoordinate = [sequence ,self.index, istrue] + coordinates
        self.coordinates.append(formatCoordinate)
        self.index += 1

    def get_coordinates(self):
        for coord in self.coordinates:
            print(*coord, sep=", ")
