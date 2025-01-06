from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QStackedWidget
)
from PySide6.QtGui import QFont, QPixmap, QColor,QIcon
from PySide6.QtCore import Qt, QTimer, QTime
import sys
from test import SettingsUI

class PostureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Posture Monitor")
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_widget.setStyleSheet("background-color: #f3f4f6;")

        # Sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar, 1)

        # Content area with stacked widget
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area, 10)

        # Add tabs to the stacked widget
        self.add_home_tab()
        self.add_dashboard_tab()
        self.add_settings_tab()

        self.setCentralWidget(main_widget)

    def create_sidebar(self):
        # Sidebar container
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #013d54;border-radius: 10px;")
        sidebar_layout = QVBoxLayout(sidebar)

        # Logo
        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        logo.setPixmap(QPixmap("assets/logo-transparent1.png").scaled(100, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setStyleSheet("margin:20px 10px")
        sidebar_layout.addWidget(logo)

        # Navigation buttons
        nav_buttons = [
            ("Home", "assets/home_icon.svg"),
            ("Dashboard", "assets/dashboard_icon.svg"),
            ("Settings", "assets/settings_icon.svg")
        ]
        self.nav_button_dict = {}
        for text, icon_path in nav_buttons:
            button = QPushButton()
            button.setText(text)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QPixmap(icon_path).scaled(20, 20, Qt.KeepAspectRatio).size())
            button.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                    font-size: 16px;
                    text-align: left;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #005f73;
                }
                QPushButton:hover QIcon {
                    color: #000000; /* Change SVG icon color on hover */
                }
            """)
            sidebar_layout.addWidget(button)
            self.nav_button_dict[text] = button
        
        self.nav_button_dict["Home"].clicked.connect(lambda: self.content_area.setCurrentIndex(0))
        self.nav_button_dict["Dashboard"].clicked.connect(lambda: self.content_area.setCurrentIndex(1))
        self.nav_button_dict["Settings"].clicked.connect(lambda: self.content_area.setCurrentIndex(2))

        sidebar_layout.addStretch()
        return sidebar

    def add_home_tab(self):
        # Settings tab content
        home = QFrame()
        home_layout = QVBoxLayout(home)
        home.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")

        # Placeholder for image/video feed
        placeholder = QLabel()
        placeholder.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setText("Image/Video Feed")
        placeholder.setFixedHeight(400)
        home_layout.addWidget(placeholder)

        # Clock
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet("font-size: 24px; color: #333;")
        self.clock_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(self.clock_label)

        # Start/Stop buttons
        button_layout = QHBoxLayout()
        start_button = QPushButton("Start")
        start_button.setStyleSheet("background-color: #013d54; color: white; font-size: 18px; padding: 10px;")
        stop_button = QPushButton("Stop")
        stop_button.setStyleSheet("background-color: #013d54; color: white; font-size: 18px; padding: 10px;")
        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)
        home_layout.addLayout(button_layout)


        self.content_area.addWidget(home)

    def add_dashboard_tab(self):
        # Dashboard tab content
        dashboard = QFrame()
        dashboard_layout = QVBoxLayout(dashboard)
        dashboard.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        label = QLabel("Dashboard Page")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #333;")
        dashboard_layout.addWidget(label)

        self.content_area.addWidget(dashboard)

    def add_settings_tab(self):
        # Settings tab content
        settings = QFrame()
        settings_layout = QVBoxLayout(settings)
        settings.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")

        label = QLabel("Settings Page")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #333;")
        settings_layout.addWidget(label)

        self.content_area.addWidget(SettingsUI())



# if __name__ == "__main__":
def main():
    app = QApplication(sys.argv)
    window = PostureApp()
    window.showMaximized()
    sys.exit(app.exec())
