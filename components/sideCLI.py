import cv2
import math as m
import mediapipe as mp

# Calculate distance
def findDistance(x1, y1, x2, y2):
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Calculate angle
def findAngle(x1, y1, x2, y2):
    try:
        theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
        return theta * (180 / m.pi)
    except ValueError:
        return 0  # Handle math domain error when input is invalid

# Function to send alert when bad posture is detected
def sendWarning():
    print("Warning: Bad posture detected! Please adjust your posture.")

# ==================== CONSTANTS and INITIALIZATIONS ==================== #
# Initialize frame counters
good_frames = 0
bad_frames = 0

# Font type
font = cv2.FONT_HERSHEY_SIMPLEX

# Colors
blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
yellow = (0, 255, 255)
pink = (255, 0, 255)

# Initialize MediaPipe Pose class
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
# ======================================================================= #

if __name__ == "__main__":
    # Open webcam input (0 for default webcam)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access the webcam.")
        exit()

    # Get webcam properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while cap.isOpened():
        # Capture frames from the webcam
        success, image = cap.read()
        if not success:
            print("Failed to capture frame. Exiting...")
            break

        # Get height and width
        h, w = image.shape[:2]

        # Convert the BGR image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image
        keypoints = pose.process(image)

        # Convert the image back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Use lm and lmPose as representative of the following methods
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark

        if lm:
            # Acquire the landmark coordinates for both sides
            l_shldr_x, l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w), int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            r_shldr_x, r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w), int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
            l_ear_x, l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].x * w), int(lm.landmark[lmPose.LEFT_EAR].y * h)
            r_ear_x, r_ear_y = int(lm.landmark[lmPose.RIGHT_EAR].x * w), int(lm.landmark[lmPose.RIGHT_EAR].y * h)
            l_hip_x, l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].x * w), int(lm.landmark[lmPose.LEFT_HIP].y * h)
            r_hip_x, r_hip_y = int(lm.landmark[lmPose.RIGHT_HIP].x * w), int(lm.landmark[lmPose.RIGHT_HIP].y * h)

            # Decide which side to use based on the visibility of landmarks (dynamic side selection)
            use_left_side = lm.landmark[lmPose.LEFT_SHOULDER].visibility > lm.landmark[lmPose.RIGHT_SHOULDER].visibility

            if use_left_side:
                shldr_x, shldr_y, ear_x, ear_y, hip_x, hip_y = l_shldr_x, l_shldr_y, l_ear_x, l_ear_y, l_hip_x, l_hip_y
            else:
                shldr_x, shldr_y, ear_x, ear_y, hip_x, hip_y = r_shldr_x, r_shldr_y, r_ear_x, r_ear_y, r_hip_x, r_hip_y

            # Calculate distance between shoulders
            offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

            # Check alignment
            if offset < 100:
                cv2.putText(image, str(int(offset)) + ' Aligned', (w - 150, 30), font, 0.9, green, 2)
            else:
                cv2.putText(image, str(int(offset)) + ' Not Aligned', (w - 150, 30), font, 0.9, red, 2)

            # Calculate angles
            neck_inclination = findAngle(shldr_x, shldr_y, ear_x, ear_y)
            torso_inclination = findAngle(hip_x, hip_y, shldr_x, shldr_y)

            # Draw landmarks and lines
            cv2.circle(image, (shldr_x, shldr_y), 7, yellow, -1)
            cv2.circle(image, (ear_x, ear_y), 7, yellow, -1)
            cv2.circle(image, (hip_x, hip_y), 7, yellow, -1)
            cv2.line(image, (shldr_x, shldr_y), (ear_x, ear_y), green if neck_inclination < 40 else red, 4)
            cv2.line(image, (hip_x, hip_y), (shldr_x, shldr_y), green if torso_inclination < 10 else red, 4)

            # Determine posture
            if neck_inclination < 40 and torso_inclination < 10:
                bad_frames = 0
                good_frames += 1

                cv2.putText(image, 'Good Posture', (10, 30), font, 0.9, green, 2)
            else:
                good_frames = 0
                bad_frames += 1

                cv2.putText(image, 'Bad Posture', (10, 30), font, 0.9, red, 2)

            # Calculate time in a posture
            good_time = (1 / fps) * good_frames
            bad_time = (1 / fps) * bad_frames

            if good_time > 0:
                cv2.putText(image, f'Good Posture Time: {round(good_time, 1)}s', (10, h - 20), font, 0.9, green, 2)
            else:
                cv2.putText(image, f'Bad Posture Time: {round(bad_time, 1)}s', (10, h - 20), font, 0.9, red, 2)

            # Send warning for bad posture
            if bad_time > 180:
                sendWarning()

        # Display the output
        cv2.imshow('Posture Detection', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
