import cv2
from posture_detector.detector import PoseDetector, PoseLandmarks
from posture_detector.deviation import Deviation
from posture_detector.logger import Logger


class BasePosture:
    """
    Wrapper for Mediapipe Pose Landmarks
    """
    def __init__(self, nose: float, mouth_right: float, mouth_left: float, left_shoulder: float, right_shoulder: float):
        self.nose = nose
        self.mouth_left = mouth_left
        self.mouth_right = mouth_right
        self.left_shoulder = left_shoulder
        self.right_shoulder = right_shoulder


class FrontPostureAnalyzer:
    """
    PostureWatcher is responsible for monitoring the posture of a user.
    It uses PoseDetector to compare the user's current posture to the base posture.
    """

    def __init__(self,
                 deviation_algorithm=2,
                 deviation_interval=5,
                 deviation_adjustment=5,
                 deviation_threshold=30,
                 deviation_buffer=3,
                 base_posture=None,
                 debug=True,):
        """
        Initializes the PostureWatcher.
        :param deviation_algorithm: The algorithm used to calculate the deviation.
        :param deviation_interval: The interval in seconds between checking for deviation
        :param deviation_adjustment: The amount of deviation to allow before triggering an alert
        :param deviation_threshold: The threshold at which a deviation should trigger an alert
        :param deviation_buffer: The number of consecutive deviations to allow before triggering an alert
        :param base_posture: The base posture to compare to
        :param debug: Whether to print debug messages
        """
        self.detector = PoseDetector()
        self.deviation = Deviation(threshold=deviation_threshold, max_buffer=deviation_buffer)

        self.fps = 30  # Default FPS

        self.cap = cv2.VideoCapture(0)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.last_fps_calc_timestamp = 0

        self.base_posture = base_posture
        self.deviation_algorithm = deviation_algorithm
        self.deviation_interval = deviation_interval
        self.deviation_adjustment = deviation_adjustment

        self.thread = None
        self.debug = debug
        self.logger = Logger('PW')

    def run(self,camera_index=0):
        """
        Finds a pose, compares it to the base posture, and notifies the user if the deviation is above the threshold.
        """
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("Error: Cannot access the webcam.")

        if not self.base_posture:
            self.set_base_posture()
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

    def stop(self):
        """
        Stops Posture Watcher and destroys allocated resources.
        """
        if self.cap:
            self.cap.release()

    def set_base_posture(self):
        _, img = self.cap.read()
        _,lm = self.detector.find_pose(img)
        if lm is not None:
            nose = lm[PoseLandmarks.NOSE]
            mouth_l = lm[9]
            mouth_r = lm[10]
            l_shoulder = lm[11]
            r_shoulder = lm[12]
            self.base_posture = BasePosture(nose, mouth_l, mouth_r, l_shoulder, r_shoulder)

    def process_frame(self):
        if not self.cap:
            raise Exception("Camera not started.")
        success, image = self.cap.read()
        if not success:
            return None, None

        # h, w = image.shape[:2]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        keypoints = self.detector.pose.process(image_rgb)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        posture_data = {"status": "Unknown", "deviation": None}

        if keypoints.pose_landmarks:
            # self.deviation.current_deviation = self._get_deviation_from_base_posture()
            # posture_data['deviation']= self.deviation.current_deviation

            cd = self._get_deviation_from_base_posture()
            # buffer = self.deviation.current_buffer

            if  cd < self.deviation.deviation_threshold:
                posture_data["status"] = "Good"
            else:
                posture_data["status"] = "Bad"

            # if self.deviation.has_deviated():
            #     self.logger.notify(f"Detected deviation from base posture by {cd}%", color='red', with_sound=True)
            # else:
            #     if cd < 25:
            #         self.logger.notify(f"✅ Great posture! {cd}% (Buf: {buffer})", color='green')
            #     elif cd < 35:
            #         self.logger.notify(f"⚠️ Improve your posture! {cd}% (Buf: {buffer})", color='yellow')
            #     else:
            #         self.logger.notify(f"️ Fix your posture! {cd}% (Buf: {buffer})", color='red')

            # if self.debug:
            #     self.logger.notify(f"Deviation buffer: {buffer}", color='white')

        return image_bgr, posture_data

    def _get_deviation_from_base_posture(self, algorithm_version: int = 1):
        """
        Calculates the deviation from the base posture as a percentage
        :param algorithm_version: The algorithm version to use (int).
                                   1: Uses body and face to calculate deviation
                                   2: Uses only face to calculate deviation
        :returns: float from 0-100, 100 being the most deviant from the base posture
        """
        if self.base_posture is None:
            return None

        _, img = self.cap.read()
        _, lm = self.detector.find_pose(img)
        deviation = 100

        if not lm:  # No pose found
            return deviation

        # Nose and mouth are used for both algorithms so its out here.
        # TODO: Make this more efficient and clean, this function is too cluttered
        nose = abs(self.base_posture.nose.x - lm[0].x) + abs(self.base_posture.nose.y - lm[0].y) + abs(
            self.base_posture.nose.z - lm[0].z)
        mouth_l = abs(self.base_posture.mouth_left.x - lm[9].x) + abs(
            self.base_posture.mouth_left.y - lm[9].y) + abs(self.base_posture.mouth_left.z - lm[9].z)
        mouth_r = abs(self.base_posture.mouth_right.x - lm[10].x) + abs(
            self.base_posture.mouth_right.y - lm[10].y) + abs(self.base_posture.mouth_right.z - lm[10].z)

        if algorithm_version == 1:
            """
            Algorithm 1: Utilities shoulders in addition to the face to track posture.
            """
            l_shoulder = abs(self.base_posture.left_shoulder.x - lm[11].x) + abs(self.base_posture.left_shoulder.y - lm[11].y) + \
                abs(self.base_posture.left_shoulder.z - lm[11].z)
            r_shoulder = abs(self.base_posture.right_shoulder.x - lm[12].x) + abs(self.base_posture.right_shoulder.y - lm[12].y) + \
                abs(self.base_posture.right_shoulder.z - lm[12].z)

            deviation = int(
                ((nose + mouth_l + mouth_r + l_shoulder + r_shoulder) / (self.base_posture.nose.x +
                 self.base_posture.mouth_left.x + self.base_posture.mouth_right.x + self.base_posture.left_shoulder.x +
                 self.base_posture.right_shoulder.x) * 100))
        elif algorithm_version == 2:
            """
            Algorithm 2: Utilities only the face to track posture.
            """
            deviation = int(
                ((nose + mouth_l + mouth_r) / (self.base_posture.nose.x + self.base_posture.mouth_left.x +
                                               self.base_posture.mouth_right.x) * 100))

        adjusted_deviation = 100 if deviation >= 100 else int(deviation - self.deviation_adjustment)
        return adjusted_deviation
