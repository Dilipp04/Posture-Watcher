import cv2
import mediapipe as mp

class PoseLandmarks:
    NOSE = 0
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12

class PoseDetector:
    """
    PoseDetector is a wrapper for the Mediapipe Pose component.
    """
    def __init__(self):
        self.results = None
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
        self.pose_connections = self.mpPose.POSE_CONNECTIONS  # Get the pose connections

    def find_pose(self, img, draw=True):
        """
        Finds a pose in a given image and draws landmarks onto it.
        
        :img cv2.VideoCapture: The source image to look for pose landmarks in
        :draw boolean: Whether to draw landmarks on the image
        :returns: If landmarks are found, (img, landmarks). Otherwise, if no landmarks are found, 
                  (img, landmarks) is returned.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        self.results = self.pose.process(img_rgb)


        if not self.results.pose_landmarks:
            return

        self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.pose_connections)
        return img, self.results.pose_landmarks.landmark
