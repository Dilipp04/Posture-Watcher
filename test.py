import cv2
import mediapipe as mp

def detect_standing_properly(landmarks):
    """Detects if the person is standing properly based on full-body posture alignment."""
    if landmarks:
        # Ensure at least 70% of the body is visible
        visible_landmarks = [lm for lm in landmarks if lm.visibility > 0.7]
        if len(visible_landmarks) < len(landmarks) * 0.7:
            return None  # Not enough landmarks visible

        # Extract relevant landmarks
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
        right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        
        # Calculate heights and alignments
        hip_height = (left_hip.y + right_hip.y) / 2
        ankle_height = (left_ankle.y + right_ankle.y) / 2
        shoulder_height = (left_shoulder.y + right_shoulder.y) / 2
        knee_height = (left_knee.y + right_knee.y) / 2
        foot_height = (left_foot.y + right_foot.y) / 2
        
        # Conditions for proper standing
        standing_properly = (
            hip_height < ankle_height - 0.2 and 
            abs(left_shoulder.y - right_shoulder.y) < 0.05 and  # Shoulders should be level
            abs(left_hip.y - right_hip.y) < 0.05 and  # Hips should be level
            abs(left_knee.y - right_knee.y) < 0.05 and  # Knees should be level
            abs(left_foot.y - right_foot.y) < 0.05 and  # Feet should be level
            nose.y < shoulder_height  # Head should be above shoulders
        )
        
        return standing_properly
    
    return False

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb_frame)
    
    if result.pose_landmarks:
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = result.pose_landmarks.landmark
        
        standing_status = detect_standing_properly(landmarks)
        
        if standing_status is None:
            cv2.putText(frame, "Body not fully visible", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif standing_status:
            cv2.putText(frame, "Proper Standing", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Improper Standing", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow("Posture Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
