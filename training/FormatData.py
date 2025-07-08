#************************** Class FormatData **************************
#
#   Implements everything related to data normalization.
#
import math
import numpy as np

class FormatData:
    def __init__(self):
        self.coordinates = []
        self.index = 1

        # exponential smoothing
        self.prev_aligned = None
        self.alpha = 0.7

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

    def extract_align_coordinates(self, frame):
        scaled_list = self.extract_scale_coordinates(frame)
        scaled_matrix = np.array(scaled_list).reshape(-1, 3) # shape (21, 3) for frame

        # scaling points
        p0  = scaled_matrix[0]    # wrist
        p5  = scaled_matrix[5]    # index finger base
        p9 = scaled_matrix[9]     # middle finger base (palm center)

        epsilon = 1e-6
        #======= Orthonormal vectors

        # wrist → palm center
        v0 = p9 - p0
        # normalize X
        norm_v0 = np.linalg.norm(v0)
        if norm_v0 < epsilon:
            norm_v0 = epsilon
        X = v0 / norm_v0

        # wrist → index finger base
        v1 = p5 - p0
        # project v1 onto v0 to make it perpendicular
        proj = v1 - np.dot(v1, X) * X
        # normalize Y
        norm_v1 = np.linalg.norm(proj)
        if norm_v1 < epsilon:
            norm_v1 = epsilon
        Y = proj / norm_v1

        # normalize Z
        Z = np.cross(X, Y)

        #========

        # change-of-basis matrix
        R = np.stack([X, Y, Z], axis=1)

        # project the points onto the new basis
        aligned = scaled_matrix.dot(R)

        # --- SMOOTHING ---
        smoothed = self.smooth_coordinate(aligned)

        # --- ZERO-CENTERING OF Z ---
        z_mean = smoothed[:, 2].mean()
        smoothed[:, 2] -= z_mean

        return smoothed.flatten().tolist()

    def smooth_coordinate(self, coordinate):
        if self.prev_aligned is None:
            smoothed = coordinate
        else:
            smoothed = self.alpha * coordinate + (1 - self.alpha) * self.prev_aligned
        
        self.prev_aligned = smoothed
        return smoothed

    def format_coordinates(self, sequence, istrue, coordinates):
        formatCoordinate = [sequence ,self.index, istrue] + coordinates
        self.coordinates.append(formatCoordinate)
        self.index += 1

    def not_format_coordinates(self, coordinates):
        self.coordinates.append(coordinates)

    def get_coordinates(self):
        for coord in self.coordinates:
            print(*coord, sep=", ")

    def write_file(self, filename):
        with open(filename, "a") as f:
            for coord in self.coordinates:
                line = ", ".join(map(str, coord))
                f.write(line + "\n")
