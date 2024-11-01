import cv2
import mediapipe as mp

# Initialize Mediapipe Pose module
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# Initialize Mediapipe drawing module
mp_drawing = mp.solutions.drawing_utils

def main():
    cap = cv2.VideoCapture(0)  # Open the camera

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while True:
        success, image = cap.read()  # Read a frame from the camera
        if not success:
            print("Error: Could not read frame.")
            break

        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and find pose landmarks
        results = pose.process(image_rgb)

        # Draw landmarks on the image
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Print landmark coordinates to the console
            print("Landmarks:")
            for id, lm in enumerate(results.pose_landmarks.landmark):
                pass
                # print(f"Landmark {id}: (x: {lm.x}, y: {lm.y}, z: {lm.z})")

        # Show the image with landmarks
        cv2.imshow('Pose Detection', image)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
