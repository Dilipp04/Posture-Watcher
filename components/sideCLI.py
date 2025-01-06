import cv2
import math as m
import mediapipe as mp


# Calculate distance
def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


# Calculate angle
def findAngle(x1, y1, x2, y2):
    try:
        theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
        degree = theta * (180 / m.pi)
        return degree
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
            # Acquire the landmark coordinates
            l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
            r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
            l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
            l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
            l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
            l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

            # Calculate distance between left shoulder and right shoulder points
            offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

            # Check alignment
            if offset < 100:
                cv2.putText(image, str(int(offset)) + ' Aligned', (w - 150, 30), font, 0.9, green, 2)
            else:
                cv2.putText(image, str(int(offset)) + ' Not Aligned', (w - 150, 30), font, 0.9, red, 2)

            # Calculate angles
            neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
            torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

            # Draw landmarks.
            cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)

            # Let's take y - coordinate of P3 100px above x1,  for display elegance.
            # Although we are taking y = 0 while calculating angle between P1,P2,P3.
            cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
            cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
            cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)

            # Similarly, here we are taking y - coordinate 100px above x1. Note that
            # you can take any value for y, not necessarily 100 or 200 pixels.
            cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

            angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))


            # Determine posture
            if neck_inclination < 40 and torso_inclination < 10:
                bad_frames = 0
                good_frames += 1

                cv2.putText(image, f'Neck: {int(neck_inclination)}  Torso: {int(torso_inclination)}',
                            (10, 30), font, 0.9, green, 2)
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, green, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, green, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, green, 2)

                # Join landmarks.
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)
            else:
                good_frames = 0
                bad_frames += 1

                cv2.putText(image, f'Neck: {int(neck_inclination)}  Torso: {int(torso_inclination)}',
                            (10, 30), font, 0.9, red, 2)
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)

                # Join landmarks.
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

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
