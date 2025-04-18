import os
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, 
    QPushButton, QFrame, QSpacerItem, QSizePolicy ,QProgressBar
)
from PySide6.QtCore import Qt,QTimer ,QElapsedTimer ,QPropertyAnimation
from PySide6.QtGui import QFont, QPixmap,QImage 
from utilities.state import State

class Yoga(QMainWindow):
    def __init__(self, state: State):
        super().__init__()
        self.state = state

        self.model = load_model("utilities/model.h5")
        self.label_names = np.load("utilities/labels.npy")
        
        self.holistic = mp.solutions.pose.Pose()
        self.drawing = mp.solutions.drawing_utils
        
        self.cap = cv2.VideoCapture(0)

        self.setWindowTitle("Yoga Analyzer")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("background-color: white;color:#013e54;font-weight:bold")

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Top bar frame
        top_frame = QFrame()
        top_frame.setStyleSheet("background:white; border-radius: 0px;")
        top_frame.setMaximumHeight(70)
        top_layout = QHBoxLayout(top_frame)

        heading = QLabel("Yoga Analyzer")
        heading.setFont(QFont("Arial", 24, QFont.Bold))
        heading.setAlignment(Qt.AlignLeft)
        heading.setStyleSheet("color: black; padding-top:10px; ")
        top_layout.addWidget(heading)

        # Content frame
        content_frame = QFrame()
        content_frame.setStyleSheet("background: white; border-radius: 0px; ")
        content_layout = QHBoxLayout(content_frame)

        # Left frame (Camera Feed)
        left_frame = QFrame()
        left_frame.setStyleSheet("background: white; border-radius: 10px;")
        left_layout = QVBoxLayout(left_frame)

        self.camera_label = QLabel("Camera Feed")
        self.camera_label.setMinimumSize(640, 470)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("border: 5px solid black; border-radius: 10px;color: Gray;font-size:20px;text-align:center")
        left_layout.addWidget(self.camera_label, alignment=Qt.AlignCenter)

        left_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        self.timer_label = QLabel("00:00")
        self.timer_label.setFont(QFont("Arial", 16, QFont.Bold))
        left_layout.addWidget(self.timer_label,alignment=Qt.AlignCenter)

        self.status_label = QLabel("Waiting...")
        self.status_label.setFont(QFont("Arial", 16, QFont.Bold))
        left_layout.addWidget(self.status_label,alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_camera)
        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_camera)
        for btn in [start_button, stop_button]:
            btn.setStyleSheet("background: #013e54; color: white; padding: 10px; border-radius: 5px; font-weight: bold")
            btn.setFixedSize(200, 40)
        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)
        left_layout.addLayout(button_layout)

        # Right frame (Pose Selection)
        right_frame = QFrame()
        right_frame.setStyleSheet("background: white; border-radius: 10px;")
        right_frame.setMinimumWidth(300)
        right_frame.setMaximumWidth(500)
        right_layout = QVBoxLayout(right_frame)

        # Pose Dictionary (Pose Name -> Image Path)
        self.pose_images = {
            "tadasana": "assets/yogasan/tadasana.png",
            "Adho Mukha Svanasana": "assets/yogasan/adho_mukha_svanasana.png",
            "bhujangasana": "assets/yogasan/bhujangasana.png",
            "Chaturanga Dandasana": "assets/yogasan/chaturanga_dandasana.png",
            "pranamasana": "assets/yogasan/pranamasana.png",
            "Setu Bandhasana": "assets/yogasan/setu_bandhasana.png",
            "Sukhasan": "assets/yogasan/sukhasan.png",
            "trikonasana": "assets/yogasan/trikonasana.png",
            "utkatasana": "assets/yogasan/utkatasana.png",
            "Virabhadrasana I": "assets/yogasan/virabhadrasana1.png",
            "Virabhadrasana II": "assets/yogasan/virabhadrasana2.png",
            "Virabhadrasana III": "assets/yogasan/virabhadrasana3.png",
            "vrikshasana": "assets/yogasan/vrikshasana.png"
        }

        self.pose_dropdown = QComboBox()
        self.pose_dropdown.addItems(self.pose_images.keys())
        self.pose_dropdown.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
                color: #333;
                
            }
            QComboBox:hover {
                border: 1px solid #4CAF50;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url('assets/dropdown_arrow.svg');
                width: 20px;
                height: 20px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
                color: #333;
                selection-background-color: #4CAF50;
                selection-color: white;
            }
        """)
        self.pose_dropdown.setMinimumSize(200, 40)
        self.pose_dropdown.currentTextChanged.connect(self.update_pose)
        right_layout.addWidget(self.pose_dropdown, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        self.pose_image = QLabel()
        self.pose_image.setMinimumSize(300, 300)
        self.pose_image.setStyleSheet("border: 3px solid gray; border-radius: 10px; padding:2px")
        right_layout.addWidget(self.pose_image, alignment=Qt.AlignCenter)
        
        self.pose_name = QLabel("Tadasana")
        self.pose_name.setAlignment(Qt.AlignCenter)
        self.pose_name.setStyleSheet("font-size:25px; color: #2c3e50;")
        right_layout.addWidget(self.pose_name, alignment=Qt.AlignCenter)

        right_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.accuracy_progress_bar = QProgressBar()
        self.accuracy_progress_bar.setAlignment(Qt.AlignCenter)
        self.accuracy_progress_bar.setFormat("%p%")
        self.accuracy_progress_bar.setValue(0)
        self.accuracy_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ccc;
                border-radius: 10px;
                text-align: center;
                height: 30px;
                width:300px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 10px;
            }
        """)

        self.accuracy_anim = QPropertyAnimation(self.accuracy_progress_bar, b"value")
        self.accuracy_anim.setDuration(10)
        right_layout.addWidget(self.accuracy_progress_bar, alignment=Qt.AlignCenter)


        # Add frames to content layout
        content_layout.addWidget(left_frame)
        content_layout.addWidget(right_frame)

        # Add top frame and content frame to main layout
        main_layout.addWidget(top_frame)
        main_layout.addWidget(content_frame)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
        self.elapsed_time = 0  # Store elapsed seconds
        self.timer_running = False  # Track if timer is active
        
        # Create a QTimer that triggers every second
        self.elapsed_timer = QTimer()
        self.elapsed_timer.timeout.connect(self.update_timer)  # Connect to update function
        self.elapsed_timer.setInterval(1000)  # Set 1-second interval

        # Set default image
        self.update_pose("tadasana")

    
    def update_pose(self, pose):
        self.pose_name.setText(f"{pose}".title())
        
        # Set Image
        image_path = self.pose_images.get(pose)
        if image_path:
            pixmap = QPixmap(image_path)
            self.pose_image.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def in_frame(self, lst):
        if (
            lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and  
            lst[15].visibility > 0.6 and lst[16].visibility > 0.6
        ) or (
            (lst[28].visibility > 0.6 or lst[27].visibility > 0.6) and  
            (lst[15].visibility > 0.6 or lst[16].visibility > 0.6)  
        ) or (
            lst[11].visibility > 0.6 and lst[12].visibility > 0.6 and  
            lst[23].visibility > 0.6 and lst[24].visibility > 0.6 and  
            lst[14].visibility > 0.6 and lst[13].visibility > 0.6
        ) or (
            lst[19].visibility > 0.6 and lst[20].visibility > 0.6 and  
            lst[25].visibility > 0.6 and lst[26].visibility > 0.6  
        ):
            return True
        return False
    
    def start_camera(self):
        self.cap = cv2.VideoCapture(self.state.get_setting("camera"))
        self.camera_label.setText("Loading...")
        self.timer.start(30)
    
    def stop_camera(self):
        self.timer.stop()
        self.camera_label.clear()
        self.timer_running = False
        self.elapsed_time = 0
        self.timer_label.setText("00:00")
    
    def update_frame(self):
        os.system("cls")
        color = (255,255,255)
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)
        res = self.holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame = cv2.blur(frame, (4,4))
        
        if res.pose_landmarks and self.in_frame(res.pose_landmarks.landmark):
            lst = []
            for i in res.pose_landmarks.landmark:
                lst.append(i.x - res.pose_landmarks.landmark[0].x)
                lst.append(i.y - res.pose_landmarks.landmark[0].y)
            
            lst = np.array(lst).reshape(1, -1)
            p = self.model.predict(lst)
            pred = self.label_names[np.argmax(p)]
            accuracy = p[0][np.argmax(p)] * 100
            
            self.update_accuracy(int(accuracy))

            if pred == self.pose_dropdown.currentText() and accuracy > 80:
                status_text = f"Pose: {pred} {accuracy:.2f}%"
                color = (0, 255, 0)
                if not self.timer_running:
                    self.elapsed_timer.start()
                    self.timer_running = True
            else:
                status_text = "Pose Incorrect or Not Trained"
                color = (0, 0, 255)

                if pred != self.pose_dropdown.currentText() and accuracy > 70:
                    self.update_accuracy(0)


                if self.timer_running:
                    self.elapsed_timer.stop()
                    self.timer_running = False
            
            self.status_label.setText(f"{status_text}")
        else:
            self.status_label.setText("Ensure Full Body is Visible")
            self.update_accuracy(0)
            if self.timer_running:
                    self.elapsed_timer.stop()
                    self.timer_running = False
        
        self.timer_label.setText(f"{self.elapsed_time}s")
        


        self.drawing.draw_landmarks(frame, res.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS,
                                    connection_drawing_spec=self.drawing.DrawingSpec(color=color, thickness=6),
                                    landmark_drawing_spec=self.drawing.DrawingSpec(color=(255,255,255), circle_radius=3, thickness=3))
        
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        qimg = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaled(self.camera_label.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.camera_label.setPixmap(scaled_pixmap)

    def update_timer(self):
        """Increment the timer every second."""
        self.elapsed_time += 1
        self.timer_label.setText(f"{self.elapsed_time}s")
    
    def update_accuracy(self, accuracy):
        if accuracy >= 80:
            self.set_progress_bar_color("#4CAF50")  # Green
        elif accuracy >= 60:
            self.set_progress_bar_color("#FFA500")  # Orange
        else:
            self.set_progress_bar_color("#F44336")  # Red

        self.accuracy_anim.stop()
        self.accuracy_anim.setStartValue(self.accuracy_progress_bar.value())
        self.accuracy_anim.setEndValue(accuracy)
        self.accuracy_anim.start()

    def set_progress_bar_color(self, color: str):
        self.accuracy_progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #ccc;
                border-radius: 10px;
                text-align: center;
                height: 30px;
                width: 300px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 10px;
            }}
        """)
