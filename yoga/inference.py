import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model 


def inFrame(lst):
	if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility>0.6 and lst[16].visibility>0.6:
		return True 
	return False

model  = load_model("yoga/model.h5")
label = np.load("yoga/labels.npy")



holistic = mp.solutions.pose
holis = holistic.Pose()
drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


while True:
	lst = []

	_, frm = cap.read()

	window = np.zeros((940,940,3), dtype="uint8")

	frm = cv2.flip(frm, 1)

	res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

	frm = cv2.blur(frm, (4,4))
	if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
		for i in res.pose_landmarks.landmark:
			lst.append(i.x - res.pose_landmarks.landmark[0].x)
			lst.append(i.y - res.pose_landmarks.landmark[0].y)

		lst = np.array(lst).reshape(1,-1)

		p = model.predict(lst)
		pred = label[np.argmax(p)]

		if p[0][np.argmax(p)] > 0.75:
			cv2.putText(window, pred , (180,180),cv2.FONT_ITALIC, 1.3, (0,255,0),2)

		else:
			cv2.putText(window, "Asana is either wrong not trained" , (100,180),cv2.FONT_ITALIC, 1.8, (0,0,255),3)

	else: 
		cv2.putText(frm, "Make Sure Full body visible", (100,450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255),3)

		
	drawing.draw_landmarks(frm, res.pose_landmarks, holistic.POSE_CONNECTIONS,
							connection_drawing_spec=drawing.DrawingSpec(color=(255,255,255), thickness=6 ),
							 landmark_drawing_spec=drawing.DrawingSpec(color=(0,0,255), circle_radius=3, thickness=3))


	window[420:900, 170:810, :] = cv2.resize(frm, (640, 480))

	cv2.imshow("window", window)

	if cv2.waitKey(1) == 27:
		cv2.destroyAllWindows()
		cap.release()
		break



# import sys
# import cv2
# import numpy as np
# import mediapipe as mp
# from keras.models import load_model
# from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QComboBox
# from PySide6.QtGui import QImage, QPixmap
# from PySide6.QtCore import QTimer

# class PoseDetectionApp(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Load model and labels
#         self.model = load_model("model.h5")
#         self.labels = np.load("labels.npy")
#         self.pose_options = list(self.labels)  # Convert to list for dropdown
#         self.selected_pose = self.pose_options[0]  # Default selected pose

#         # Initialize MediaPipe Pose
#         self.mp_pose = mp.solutions.pose
#         self.pose = self.mp_pose.Pose()
#         self.mp_drawing = mp.solutions.drawing_utils

#         # UI Setup
#         self.setWindowTitle("Yoga Pose Detection App")
#         self.setGeometry(100, 100, 900, 700)

#         self.video_label = QLabel(self)
#         self.video_label.setFixedSize(800, 500)

#         self.pose_label = QLabel("Pose: Waiting...", self)
#         self.pose_label.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")

#         self.accuracy_label = QLabel("Accuracy: 0%", self)
#         self.accuracy_label.setStyleSheet("font-size: 18px; font-weight: bold; color: blue;")

#         self.pose_dropdown = QComboBox(self)
#         self.pose_dropdown.addItems(self.pose_options)
#         self.pose_dropdown.currentTextChanged.connect(self.update_selected_pose)

#         self.start_button = QPushButton("Start Camera", self)
#         self.start_button.clicked.connect(self.start_camera)

#         layout = QVBoxLayout()
#         layout.addWidget(self.video_label)
#         layout.addWidget(self.pose_dropdown)
#         layout.addWidget(self.pose_label)
#         layout.addWidget(self.accuracy_label)
#         layout.addWidget(self.start_button)
#         self.setLayout(layout)

#         # Camera setup
#         self.cap = cv2.VideoCapture(0)
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_frame)

#     def start_camera(self):
#         self.timer.start(30)  # Update every 30ms

#     def update_selected_pose(self, pose):
#         self.selected_pose = pose

#     def inFrame(self, landmarks):
#         return (landmarks[28].visibility > 0.6 and landmarks[27].visibility > 0.6 
#                 and landmarks[15].visibility > 0.6 and landmarks[16].visibility > 0.6)

#     def update_frame(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             print("Camera feed not available")
#             return
        
#         frame = cv2.flip(frame, 1)
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = self.pose.process(rgb_frame)
    
#         if results.pose_landmarks and self.inFrame(results.pose_landmarks.landmark):
#             self.mp_drawing.draw_landmarks(
#                 frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
#                 self.mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=6),
#                 self.mp_drawing.DrawingSpec(color=(0, 0, 255), circle_radius=3, thickness=3)
#             )
    
#             # Extract landmarks for classification
#             landmarks = np.array([[lm.x - results.pose_landmarks.landmark[0].x, 
#                                    lm.y - results.pose_landmarks.landmark[0].y] 
#                                   for lm in results.pose_landmarks.landmark]).flatten().reshape(1, -1)
    
#             print(f"Landmarks shape: {landmarks.shape}")  # Debugging line
    
#             prediction = self.model.predict(landmarks)
#             predicted_pose = self.labels[np.argmax(prediction)]
#             confidence = prediction[0][np.argmax(prediction)]
    
#             print(f"Predicted Pose: {predicted_pose}, Confidence: {confidence}")  # Debugging line
    
#             if confidence > 0.75:
#                 self.pose_label.setText(f"Pose: {predicted_pose} ({confidence:.2%})")
#             else:
#                 self.pose_label.setText("Asana is either wrong or not trained")
#         else:
#             self.pose_label.setText("Make sure full body is visible")
    
#         # Convert frame to QImage
#         height, width, channel = frame.shape
#         bytes_per_line = 3 * width
#         q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
#         self.video_label.setPixmap(QPixmap.fromImage(q_img))
    
#         def closeEvent(self, event):
#             self.cap.release()
#             self.timer.stop()
#             event.accept()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = PoseDetectionApp()
#     window.show()
#     sys.exit(app.exec())
