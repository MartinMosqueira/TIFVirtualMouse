class FormatData:
    def __init__(self):
        self.coordinates = []
        self.index = 0

    def extract_coordinates(self, frame):
        coordinate = []
        for fm in frame.hand_landmarks[0]:
            coordinate.extend([fm.x, fm.y, fm.z])
        return coordinate

    def format_coordinates(self, sequence, istrue, frame):
        formatCoordinate = [sequence ,self.index, istrue] + self.extract_coordinates(frame)
        self.coordinates.append(formatCoordinate)
        self.index += 1

    def get_coordinates(self):
        for coord in self.coordinates:
            print(*coord, sep=", ")

